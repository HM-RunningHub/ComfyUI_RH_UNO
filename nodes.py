import sys
import importlib
import comfy.utils

class Kiki_UNO_Loadmodel:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_type": (["flux-schnell", "flux-dev", 'flux-dev-fp8', 'flux-schnell-fp8'], ),
            }
        }

    RETURN_TYPES = ("UNO_MODEL", "UNO_CLIP", "UNO_VAE")
    RETURN_NAMES = ("uno_model", "uno_clip", 'uno_vae')
    FUNCTION = "run"
    TITLE = 'RunningHub UNO Loadmodel'

    CATEGORY = "Runninghub/UNO"

    def run(self, model_type):
        lib_name = 'ComfyUI_RH_UNO.exec'
        if lib_name in sys.modules:
            importlib.reload(sys.modules[lib_name])
        import ComfyUI_RH_UNO.exec as uexec
        model, clip, vae = uexec.load_model(model_type)
        return (model, clip, vae)
    
class Kiki_UNO_Sampler:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "uno_model" : ("UNO_MODEL", ),
                "uno_clip" : ("UNO_CLIP", ),
                "uno_vae" : ("UNO_VAE", ),
                "prompt": ("STRING", {"multiline": True}),
                "width": ("INT", {"default": 704, "min": 256, "max": 2048, "step": 16}),
                "height": ("INT", {"default": 704, "min": 256, "max": 2048, "step": 16}),
                "guidance": ("FLOAT", {"default": 4.0, "min": 0.0, "max": 10.0, "step": 0.1}),
                "num_steps": ("INT", {"default": 4, "min": 1, "max": 100}),
                "seed": ("INT", {"default": 3407}),
                "pe": (["d", "h", "w", "o"], {"default": "d"}),
            },
            "optional": {
                "ref_images": ("IMAGE", ),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image_out",)
    CATEGORY = "examples"
    FUNCTION = "run"

    TITLE = 'RunningHub UNO Sampler'
    OUTPUT_NODE = True

    # def run(self, uno_model, uno_clip, uno_vae, prompt, width, height, guidance, num_steps, seed, pe):
    def run(self, ref_images=None, **kwargs):
        self.pbar = comfy.utils.ProgressBar(kwargs['num_steps'])
        lib_name = 'ComfyUI_RH_UNO.exec'
        if lib_name in sys.modules:
            importlib.reload(sys.modules[lib_name])
        import ComfyUI_RH_UNO.exec as uexec
        kwargs['rh_hook'] = self.update
        image = uexec.sample(ref_images, **kwargs)
        return (image, )
    
    def update(self, in_progress):
        self.pbar.update(in_progress)

    
NODE_CLASS_MAPPINGS = {
    "RunningHub_UNO_Loadmodel": Kiki_UNO_Loadmodel,
    "RunningHub_UNO_Sampler": Kiki_UNO_Sampler,
}