
# Multi‑Model Image & Video Worker (RunPod Serverless)
[![Runpod](https://api.runpod.io/badge/asciifarm/runpod-multimodel-serverless)](https://console.runpod.io/hub/asciifarm/runpod-multimodel-serverless)

Serverless **multi‑model** worker for RunPod Hub and private endpoints.

Supports:
- **Stable Diffusion 3 Medium** – text‑to‑image
- **Stable Video Diffusion XT 1.1** – image‑to‑video

## Features
- Single Hub tool with **WORKER** selector
- True serverless (scale‑to‑zero, pay‑per‑second)
- Optimized cold‑start with HuggingFace cache on volume
- Async jobs via `/run` + `/status`

## Models
| WORKER | Task |
|------|------|
| `sd3_medium` | Text → Image |
| `svd_xt_1_1` | Image → Video |

## Usage
Select the model using the **WORKER** environment variable (Hub UI preset).

## Notes
- First run on a fresh volume downloads model weights.
- Subsequent runs reuse cache for faster startup.
