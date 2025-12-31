
# Multi-Model Serverless Worker (RunPod Hub)
[![Runpod](https://api.runpod.io/badge/asciifarm/runpod-multimodel-serverless)](https://console.runpod.io/hub/asciifarm/runpod-multimodel-serverless)

Monorepo serverless **Hub-style**, modellato sul progetto ufficiale `worker-sdxl-turbo`.

## Modelli supportati
- **sd3_medium** – Stable Diffusion 3 Medium (text-to-image)
- **svd_xt_1_1** – Stable Video Diffusion XT 1.1 (image-to-video)

## Come funziona
- Dockerfile **GPU completo**, buildato UNA VOLTA dal RunPod Hub
- Nessun `git clone` a runtime
- Worker serverless avviato on-demand (pay-per-second)
- Selezione modello via variabile `WORKER`
