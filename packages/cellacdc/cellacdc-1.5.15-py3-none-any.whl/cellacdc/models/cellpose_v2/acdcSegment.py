import os
import pathlib

import numpy as np

import skimage.exposure
import skimage.filters
import skimage.measure

from cellpose import models
from cellacdc import printl, myutils

class AvailableModels:
    major_version = myutils.get_cellpose_major_version()
    if major_version == 3:
        from ..cellpose_v3 import CELLPOSE_V3_MODELS
        values = CELLPOSE_V3_MODELS
    else:
        from . import CELLPOSE_V2_MODELS
        values = CELLPOSE_V2_MODELS

class Model:
    def __init__(
            self, 
            model_type: AvailableModels='cyto', 
            net_avg=False, 
            gpu=False,
            device='None',
            directml_gpu=False,
        ):
        if device == 'None':
            device = None
        
        major_version = myutils.get_cellpose_major_version()
        print(f'Initializing Cellpose v{major_version}...')

        if directml_gpu:
            from cellacdc.models.cellpose_v2._directML import init_directML
            directml_gpu = init_directML()

        if directml_gpu and gpu:
            printl(
                """
                gpu is preferable to directml_gpu, but doesn't work with non NVIDIA GPUs.
                Since directml_gpu and set to True, the gpu argument will be ignored.
                """
            )
            gpu = False

        if major_version == 3:
            if model_type=='cyto3':
                self.model = models.Cellpose(
                    gpu=gpu, model_type=model_type, device=device
                )
            else:
                diam_mean = 17.0 if model_type=="nuclei" else 30.0
                self.model = models.CellposeModel(
                    gpu=gpu, 
                    diam_mean=diam_mean,
                    model_type=model_type
                )
        else:
            if model_type=='cyto':
                self.model = models.Cellpose(
                    gpu=gpu, net_avg=net_avg, model_type=model_type
                )
            else:
                self.model = models.CellposeModel(
                    gpu=gpu, net_avg=net_avg, model_type=model_type
                )
        
        if directml_gpu:
            from cellacdc.models.cellpose_v2._directML import setup_directML
            setup_directML(self)

            from cellacdc.core import fix_sparse_directML
            fix_sparse_directML()

        self.is_rgb = False
        
    def setupLogger(self, logger):
        models.models_logger = logger
    
    def setLoggerPropagation(self, propagate:bool):
        models.models_logger.propagate = propagate

    def setLoggerLevel(self, level:str):
        import logging
        if level == 'error':
            models.models_logger.setLevel(logging.ERROR)
    
    def closeLogger(self):
        handlers = models.models_logger.handlers[:]
        for handler in handlers:
            handler.close()
            models.models_logger.removeHandler(handler)
    
    def _eval(self, image, **kwargs):        
        return self.model.eval(image, **kwargs)[0]
    
    def second_ch_img_to_stack(self, first_ch_data, second_ch_data):
        # The 'cyto' model can work with a second channel (e.g., nucleus).
        # However, it needs to be encoded into one of the RGB channels
        # Here we put the first channel in the 'red' channel and the 
        # second channel in the 'green' channel. We then pass
        # `channels = [1,2]` to the segment method
        rgb_stack = np.zeros((*first_ch_data.shape, 3), dtype=first_ch_data.dtype)
        
        R_slice = [slice(None)]*(rgb_stack.ndim)
        R_slice[-1] = 0
        R_slice = tuple(R_slice)
        rgb_stack[R_slice] = first_ch_data

        G_slice = [slice(None)]*(rgb_stack.ndim)
        G_slice[-1] = 1
        G_slice = tuple(G_slice)

        rgb_stack[G_slice] = second_ch_data
        
        self.is_rgb = True

        return rgb_stack
    
    def _get_eval_kwargs(
            self, image,
            diameter=0.0,
            flow_threshold=0.4,
            cellprob_threshold=0.0,
            stitch_threshold=0.0,
            min_size=15,
            anisotropy=0.0,
            normalize=True,
            resample=True,
            segment_3D_volume=False,
            **kwargs
        ):
        isRGB = image.shape[-1] == 3 or image.shape[-1] == 4
        isZstack = (image.ndim==3 and not isRGB) or (image.ndim==4)

        if anisotropy == 0 or not isZstack:
            anisotropy = 1.0
        
        do_3D = segment_3D_volume
        if not isZstack:
            stitch_threshold = 0.0
            segment_3D_volume = False
            do_3D = False
        
        if stitch_threshold > 0:
            do_3D = False

        if flow_threshold==0.0 or isZstack:
            flow_threshold = None

        channels = [0,0] if not isRGB else [1,2]

        eval_kwargs = {
            'channels': channels,
            'diameter': diameter,
            'flow_threshold': flow_threshold,
            'cellprob_threshold': cellprob_threshold,
            'stitch_threshold': stitch_threshold,
            'min_size': min_size,
            'normalize': normalize,
            'do_3D': do_3D,
            'anisotropy': anisotropy,
            'resample': resample
        }
        
        return eval_kwargs, isZstack

    def segment(
            self, image,
            diameter=0.0,
            flow_threshold=0.4,
            cellprob_threshold=0.0,
            stitch_threshold=0.0,
            min_size=15,
            anisotropy=0.0,
            normalize=True,
            resample=True,
            segment_3D_volume=False            
        ):
        """_summary_

        Parameters
        ----------
        image : (Y, X) or (Z, Y, X) numpy.ndarray
            Input image. Either 2D or 3D z-stack.
        diameter : float, optional
            Average diameter (in pixels) of the obejcts of interest. 
            Default is 0.0
        flow_threshold : float, optional
            Flow error threshold (all cells with errors below threshold are 
            kept) (not used for 3D). Default is 0.4
        cellprob_threshold : float, optional
            All pixels with value above threshold will be part of an object. 
            Decrease this value to find more and larger masks. Default is 0.0
        stitch_threshold : float, optional
            If `stitch_threshold` is greater than 0.0 and `segment_3D_volume` 
            is True, masks are stitched in 3D to return volume segmentation. 
            Default is 0.0
        min_size : int, optional
            Minimum number of pixels per mask, you can turn off this filter 
            with `min_size = -1`. Default is 15
        anisotropy : float, optional
            For 3D segmentation, optional rescaling factor (e.g. set to 2.0 if 
            Z is sampled half as dense as X or Y). Default is 0.0
        normalize : bool, optional
            If True, normalize image using the other parameters. 
            Default is True
        resample : bool, optional
            Run dynamics at original image size (will be slower but create 
            more accurate boundaries). Default is True
        segment_3D_volume : bool, optional
            If True and input `image` is a 3D z-stack the entire z-stack 
            is passed to cellpose model. If False, Cell-ACDC will force one 
            z-slice at the time. Best results with 3D data are obtained by 
            passing the entire z-stack, but with a `stitch_threshold` greater 
            than 0 (e.g., 0.4). This way cellpose will internally segment 
            slice-by-slice and it will merge the resulting z-slice masks 
            belonging to the same object. 
            Default is False

        Returns
        -------
        np.ndarray of ints
            Segmentations masks array

        Raises
        ------
        TypeError
            `stitch_threshold` must be 0 when segmenting slice-by-slice.
        """        
        # Preprocess image
        # image = image/image.max()
        # image = skimage.filters.gaussian(image, sigma=1)
        # image = skimage.exposure.equalize_adapthist(image)
        eval_kwargs, isZstack = self._get_eval_kwargs(
            image,
            diameter=diameter,
            flow_threshold=flow_threshold,
            cellprob_threshold=cellprob_threshold,
            stitch_threshold=stitch_threshold,
            min_size=min_size,
            anisotropy=anisotropy,
            normalize=normalize,
            resample=resample,
            segment_3D_volume=segment_3D_volume            
        )

        if not segment_3D_volume and isZstack and stitch_threshold>0:
            raise TypeError(
                "`stitch_threshold` must be 0 when segmenting slice-by-slice. "
                "Alternatively, set `segment_3D_volume = True`."
            )

        # Run cellpose eval
        if not segment_3D_volume and isZstack:
            labels = np.zeros(image.shape, dtype=np.uint32)
            for i, _img in enumerate(image):
                _img = _initialize_image(_img, self.is_rgb)
                input_img = _img.astype(np.float32)
                lab = self._eval(input_img, **eval_kwargs)
                labels[i] = lab
            labels = skimage.measure.label(labels>0)
        else:
            image = _initialize_image(image, self.is_rgb)  
            input_img = image.astype(np.float32)
            labels = self._eval(input_img, **eval_kwargs)
        return labels

    def segment3DT(self, video_data, signals=None, **kwargs):
        eval_kwargs, isZstack = self._get_eval_kwargs(video_data[0], **kwargs)
        if not kwargs['segment_3D_volume'] and isZstack:
            # Passing entire 4D video and segmenting slice-by-slice is 
            # not possible --> iterate each frame and run normal segment
            labels = np.zeros(video_data.shape, dtype=np.uint32)
            for i, image in enumerate(video_data):
                lab = self.segment(image, **kwargs)
                labels[i] = lab
        else:
            eval_kwargs['channels'] = [eval_kwargs['channels']]*len(video_data)
            images = [
                _initialize_image(image, self.is_rgb)[0].astype(np.float32) 
                for image in video_data
            ]
            labels = np.array(self._eval(images, **eval_kwargs))
        return labels        
    
def _initialize_image(image, is_rgb=False):        
    # See cellpose.gui.io._initialize_images
    if image.ndim > 3 and not is_rgb:
        raise TypeError(
            f'Image is 4D with shape {image.shape}.'
            'Only 2D or 3D images are supported by cellpose in Cell-ACDC'
        )
        # # make tiff Z x channels x W x H
        # if image.shape[0]<4:
        #     # tiff is channels x Z x W x H
        #     image = np.transpose(image, (1,0,2,3))
        # elif image.shape[-1]<4:
        #     # tiff is Z x W x H x channels
        #     image = np.transpose(image, (0,3,1,2))
        # # fill in with blank channels to make 3 channels
        # if image.shape[1] < 3:
        #     shape = image.shape
        #     shape_to_concat = (shape[0], 3-shape[1], shape[2], shape[3])
        #     to_concat = np.zeros(shape_to_concat, dtype=np.uint8)
        #     image = np.concatenate((image, to_concat), axis=1)
        # image = np.transpose(image, (0,2,3,1))
    elif image.ndim==3:
        # if image.shape[0] < 5:
        #     # Move first axis to last since we interpret this as RGB channels
        #     image = np.transpose(image, (1,2,0))
        if image.shape[-1] < 3:
            shape = image.shape
            shape_to_concat = (shape[0], shape[1], 3-shape[2])
            to_concat = np.zeros(shape_to_concat,dtype=type(image[0,0,0]))
            image = np.concatenate((image, to_concat), axis=-1)
            image = image[np.newaxis,...]
        elif image.shape[-1]<5 and image.shape[-1]>2:
            image = image[:,:,:3]
            image = image[np.newaxis,...]
    else:
        image = image[np.newaxis,...]    
    
    img_min = image.min() 
    img_max = image.max()
    image = image.astype(np.float32)
    image -= img_min
    if img_max > img_min + 1e-3:
        image /= (img_max - img_min)
    image *= 255
    if image.ndim < 4:
        image = image[:,:,:,np.newaxis]
    
    return image

def url_help():
    return 'https://cellpose.readthedocs.io/en/latest/api.html'
