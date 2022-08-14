import cv2
import glob
import os
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet

from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact

def REenhance(
    input: str = None,
    output: str = None,
    model: int =1,
    out_scale: float = 4,
    suffix: str = 'enhanced',
    tile: int = 0,
    tile_pad: int = 10,
    pre_pad: int = 0,
    ext: str = 'auto'
    ):

    srmodel = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    netscale = 4

    if model == 1:
        model_name = 'satesr_net_g'
    elif model == 0:
        model_name = 'RealESRGAN_x4plus'
        from gfpgan import GFPGANer
        face_enhancer = GFPGANer(
            model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
            upscale=out_scale,
            arch='clean',
            channel_multiplier=2,
            bg_upsampler=upsampler)
    else:
        raise Exception('invalid model selection, try 1 (default) for satesr model or 0 for realesrgan model.')

    model_path = os.path.join('models', model_name + '.pth')
    if not os.path.isfile(model_path):
        raise ValueError(f'Model {model_name} does not exist.')
    
    if torch.cuda.is_available():
        fp16 = True
        print('GPU mode')
    else:
        fp16 = False
        print('CPU mode, image processing might be slow')
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        model=srmodel,
        tile=tile,
        tile_pad=tile_pad,
        pre_pad=pre_pad,
        half= fp16)
    
    os.makedirs(output, exist_ok=True)

    if os.path.isfile(input):
        paths = [input]
    else:
        paths = sorted(glob.glob(os.path.join(input, '*')))

    for idx, path in enumerate(paths):
        imgname, extension = os.path.splitext(os.path.basename(path))
        print('Upsampling',imgname,',','total number of file(s):',idx+1)

        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if len(img.shape) == 3 and img.shape[2] == 4:
            img_mode = 'RGBA'
        else:
            img_mode = None

        try:
            if model==0:
                _, _, sroutput = face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
            else:
                sroutput, _ = upsampler.enhance(img, outscale=out_scale)
        except RuntimeError as error:
            print('Error', error)
            print('If you encounter CUDA out of memory, try to set tile with a smaller number.')
        else:
            if ext == 'auto':
                extension = extension[1:]
            else:
                extension = ext
            if img_mode == 'RGBA':  # RGBA images should be saved in png format
                extension = 'png'
            if suffix == '':
                save_path = os.path.join(output, f'{imgname}.{extension}')
            else:
                save_path = os.path.join(output, f'{imgname}_{suffix}.{extension}')
            cv2.imwrite(save_path, sroutput)
            
    print('Finshed, enhanced image(s) saved in',output)