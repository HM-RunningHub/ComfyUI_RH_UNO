# UNO (Unity and Novel Output) for ComfyUI

UNO (Unity and Novel Output) 的 ComfyUI 实现，支持 FLUX满血模型。
它可以在 24GB VRAM 上运行完整版本，并且能够快速运行 FP8 版本。

## 在线访问
您还可以在线访问 RunningHub 免费使用此插件和模型。
https://www.runninghub.cn/post/1910316871583789058

## 功能特性

- **更新至作者的最新版本**
  - 支持 `flux-dev-fp8` 和 `flux-schnell-fp8`
  - 注意：`flux-schnell-fp8` 提供较低的一致性但生成速度更快（4 步）
- **内存优化**通过块交换
  - 通过swap block，支持在24g gpu上跑bf16的flux-dev和flux-schnell
- **进度条**
  - 实时显示去噪进度
- **本地模型加载**
  - 不强行去hugginface下载模型，对CN环境更友好  

## 模型配置

### 目录结构

模型在根目录的 `config.json` 文件中配置。预期的默认结构为：
```
ComfyUI/models
  flux/
    FLUX.1-schnell/
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

### 文本编码器和 CLIP 配置

对于 T5 和 CLIP 模型，有两种组织选项：

1. **单一目录** (XLabs-AI/xflux_text_encoders 风格)：
   - 设置 `"t5-in-one": 1` 或 `"clip-in-one": 1`
   - 文本编码器和分词器在同一个文件夹中

2. **官方结构** (单独的目录)：
   - 设置 `"t5-in-one": 0` 或 `"clip-in-one": 0`
   - 将 `"t5"` 或 `"clip"` 指向父目录
   - 子目录必须遵循官方命名约定：
     - CLIP：`text_encoder` 和 `tokenizer`
     - T5：`text_encoder_2` 和 `tokenizer_2`

### 其他模型路径

- **VAE**：
  - 默认：`comfyui/models/vae/`
  - 通过 config.json 中的 `"vae_base"` 配置

- **FLUX 模型**：
  - 默认：`comfyui/models/unet/`
  - 通过 config.json 中的 `"model_base"` 配置
  - 注意：作者认为当前的 FP8 FLUX 模型存在问题，因此在两种模式下都使用 BF16 模型

- **DIT-LoRA 模型**：
  - 默认：`comfyui/models/UNO/`
  - 通过 config.json 中的 `"lora_base"` 配置

## 致谢

感谢原作者。访问官方仓库：https://github.com/bytedance/UNO
