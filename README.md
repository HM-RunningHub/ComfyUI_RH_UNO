# [中文版说明](README_CN.md).

# UNO (Unity and Novel Output) for ComfyUI

This repository hosts the ComfyUI implementation of UNO (Unity and Novel Output), supporting FLUX models. This implementation includes several new features and optimizations.
That can run the full version with 24GB VRAM, as well as quickly run the FP8 version.

## Online Access
You can also access RunningHub online to use this plugin and model for free.
https://www.runninghub.ai/post/1910316871583789058

## Features

- **Updated to match author's latest version**
  - Support for `flux-dev-fp8` and `flux-schnell-fp8`
  - Note: `flux-schnell-fp8` offers lower consistency but much faster generation (4 steps)
- **Memory optimization** through block swapping
  - Run BF16 models on 24GB GPUs 
  - Support for both `flux-dev` and `flux-schnell` in BF16 mode on 24GB GPUs 
- **Progress bar** to display denoising progress in real-time
- **Local model loading** configured via `config.json`

## Model Configuration

### Directory Structure

Models are configured in the root `config.json` file. The default structure expected is:
```
ComfyUI/models
    flux/
        FLUX.1-schnell/   ###download from https://huggingface.co/black-forest-labs/FLUX.1-schnell
            text_encoder/
            tokenizer/
            text_encoder_2/
            tokenizer_2/
    unet/
        flux1-schnell.sft
        flux1-dev.sft
    vae/
        ae.safetensors
    UNO/
        dit_lora.safetensors
```

### Text Encoder and CLIP Configuration

For T5 and CLIP models, there are two organization options:

1. **Single directory** (XLabs-AI/xflux_text_encoders style):
   - Set `"t5-in-one": 1` or `"clip-in-one": 1`
   - Text encoder and tokenizer are in the same folder

2. **Official structure** (separate directories):
   - Set `"t5-in-one": 0` or `"clip-in-one": 0`
   - Point `"t5"` or `"clip"` to the parent directory
   - Child directories must follow official naming conventions:
     - CLIP: `text_encoder` and `tokenizer`
     - T5: `text_encoder_2` and `tokenizer_2`

### Other Model Paths

- **VAE**: 
  - Default: `comfyui/models/vae/`
  - Configure with `"vae_base"` in config.json

- **FLUX Models**:
  - Default: `comfyui/models/unet/`
  - Configure with `"model_base"` in config.json
  - Note: The author believes current FP8 FLUX models have issues, so BF16 models are used in both modes

- **DIT-LoRA Models**:
  - Default: `comfyui/models/UNO/`
  - Configure with `"lora_base"` in config.json
## Example
![image](https://github.com/user-attachments/assets/ebb4da62-880b-4365-b1b0-921a432f0679)


## Acknowledgments

Thanks to the original author. Visit the official repository at: https://github.com/bytedance/UNO
