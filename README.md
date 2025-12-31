# RunPod Serverless Multi-Model (Monorepo)

Monorepo pronto per GitHub per worker RunPod **serverless** con focus su **cold-start minimo** e **NO image build** (runtime install + cache su volume).

Contiene 2 worker separati:
- `sd3_medium` (Stable Diffusion 3 Medium) - text-to-image
- `svd_xt_1_1` (Stable Video Diffusion Img2Vid XT 1.1) - image-to-video

## Perché "NO build, solo runtime"
Invece di buildare un container pesante (CUDA+PyTorch), usi un'immagine base RunPod già pronta (es. `runpod/pytorch:...`) e in `dockerArgs`:
1) cloni la repo
2) installi requirements del worker
3) avvii `handler.py`

Il download dei pesi viene cache-ato su `/workspace` (volume RunPod), quindi:
- primo cold start: scarica i pesi
- cold start successivi sullo stesso volume: riusa cache (molto più veloce)

## Struttura
- `apps/<worker>/handler.py` : entrypoint RunPod serverless
- `apps/<worker>/download_weights.py` : warmup/cache pesi (idempotente)
- `apps/<worker>/.runpod/` : template + metadata
- `scripts/runtime_bootstrap.sh` : bootstrap unico (clone + deps + run)

## Endpoints RunPod
RunPod serverless espone tipicamente:
- `/run` (async) -> ritorna `id`
- `/status/<id>` -> polling
- `/runsync` (sync) -> attende risultato

## Note cold start
Per ridurre il tempo:
- usa volume e cache HF su `/workspace/.cache/huggingface`
- scarica pesi in bootstrap (prima del primo job)
- evita di installare dipendenze non necessarie
- pin versioni e preferisci wheels
