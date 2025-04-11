import os, sys
from PIL import Image
import numpy as np
import torch

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from accelerate import Accelerator
from uno.flux.pipeline import UNOPipeline, preprocess_ref
from uno.flux.util import (
    load_ae,
    load_clip,
    load_flow_model_only_lora,
    load_t5,
)

def load_model(model_type, device='cpu', lora_rank=512):
    # if 'schnell' in model_type:
    clip = load_clip(device)
    t5 = load_t5(device, max_length=512)
    vae = load_ae(model_type, device=device)
    model = load_flow_model_only_lora(
        model_type, device=device, lora_rank=lora_rank
    )
    return [model, model_type], [clip, t5], vae
    
def sample(ref_images, **kwargs):
    kwargs['rh_hook'](0)
    model, model_type = kwargs['uno_model']
    clip, t5 = kwargs['uno_clip']
    vae = kwargs['uno_vae']
    pipeline = UNOPipeline(
        model_type,
        'cuda',
        True,
        True,
        lora_rank=512,
    )
    pipeline.model = model
    pipeline.clip = clip
    pipeline.t5 = t5
    pipeline.ae = vae

    count = len(ref_images)
    ref_size = 512 if count == 1 else 320
    ref_imgs = []
    for image in ref_images:
        i = 255. * image.cpu().numpy()
        ref_image = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        ref_image = preprocess_ref(ref_image, ref_size)
        ref_imgs.append(ref_image)

    image_gen = pipeline(
        prompt = kwargs['prompt'],
        width = kwargs['width'],
        height = kwargs['height'],
        guidance = kwargs['guidance'],
        num_steps = kwargs['num_steps'],
        seed = kwargs['seed'],
        ref_imgs = ref_imgs,
        pe = kwargs['pe'],
        rh_hook = kwargs['rh_hook'],
    )
    image_gen.save('x.png')

    image_gen = torch.from_numpy(np.array(image_gen).astype(np.float32) / 255.0)[None,]

    return image_gen
