# OpenClaw Recipes

This directory contains Lemonade Server recipes intended to work well with OpenClaw.

## Selection Goals

- Prefer models with strong instruction following and tool-use potential.
- Include multimodal options for image-aware workflows when the model family supports it.
- Keep recipes simple and consistent with Lemonade's `llamacpp` backend.
- Include smaller VRAM-friendly options alongside higher-capability defaults.
- Use `ctx_size: 32768` for larger-capability defaults and `ctx_size: 16384` for lower-VRAM options.

## Higher-Capability Models

- `GLM-4.7-Flash-GGUF`
- `Gemma-4-26B-A4B`
- `Qwen3.5-35B-A3B-Q4_K_M`
- `Qwen3-Coder-30B-A3B-Instruct-GGUF`
- `Qwen3-VL-30B-A3B-Instruct-GGUF`
- `gpt-oss-20b-GGUF`

## Lower-VRAM Options

- `Qwen3-8B-GGUF`
- `Qwen3-VL-8B-Instruct-GGUF`
- `Qwen2.5-Coder-7B-Instruct-128K-GGUF`
- `Qwen2.5-VL-7B-Instruct-GGUF`
- `gemma-3-4b-it-GGUF`

These lower-VRAM options were chosen because they stay at 8B or below while still offering a reasonable balance of chat quality, coding utility, tool-use compatibility, or multimodal support.
