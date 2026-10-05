# NaSuno Production Deployment Guide

## 1. Overview

NaSuno can be deployed as:
1. **A Standalone CLI Tool**: On developer workstations or audio engineering rigs.
2. **A Containerized Batch Worker**: In Docker or Kubernetes to process high-volume audio catalogs.
3. **An Embedded Python Library**: Directly integrated into digital audio workstation (DAW) backends or web APIs.

---

## 2. Docker Deployment

### 2.1 Building the Production Image

The repository includes a multi-stage `Dockerfile` with system dependencies (`libsndfile1`, `ffmpeg`) and an unprivileged `nasuno` user:

```bash
docker build -t nasuno:2.0.0 .
```

### 2.2 Running Single File Processing

Mount your local audio directory into `/data`:

```bash
docker run --rm -v $(pwd)/audio_files:/data nasuno:2.0.0 \
  clean /data/track.mp3 /data/track_cleaned.mp3 --level moderate
```

### 2.3 Running Batch Directory Processing

```bash
docker run --rm -v $(pwd)/audio_files:/data nasuno:2.0.0 \
  clean --directory /data/input_dir /data/output_dir --level aggressive
```

### 2.4 Using Docker Compose

A pre-configured `docker-compose.yml` is provided for containerized workflows:

```bash
# Start processing via docker compose
docker compose up
```

---

## 3. Resource Sizing & Capacity Planning

| Workload Type          | Audio Duration | Memory Required | Recommended CPU Cores |
| ---------------------- | -------------- | --------------- | --------------------- |
| Single Song (Standard) | 3 - 5 minutes  | < 256 MB        | 1 Core                |
| Long Album / DJ Set    | 60 - 90 mins   | < 512 MB (RAM)  | 2 Cores               |
| High-Volume Batch      | 1,000+ tracks  | 2 GB - 4 GB     | 4 - 8 Cores           |

NaSuno dynamically utilizes chunked streaming for large files to keep memory usage constant regardless of track length.

---

## 4. Kubernetes Batch Processing Pattern

For large-scale audio catalog sanitization, deploy NaSuno as a Kubernetes `Job` or `CronJob` with persistent volume claims (PVC) for audio storage:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: nasuno-catalog-cleaner
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: nasuno
          image: nasuno:2.0.0
          command: ["nasuno", "clean", "--directory", "/mnt/audio/in", "/mnt/audio/out", "--level", "moderate"]
          envFrom:
            - configMapRef:
                name: nasuno-config
          volumeMounts:
            - name: audio-storage
              mountPath: /mnt/audio
          resources:
            requests:
              memory: "512Mi"
              cpu: "1000m"
            limits:
              memory: "2Gi"
              cpu: "4000m"
      restartPolicy: OnFailure
      volumes:
        - name: audio-storage
          persistentVolumeClaim:
            claimName: audio-pvc
```

---

## 5. Production Health Checks & Verification

After processing audio in production environments, automated verification should ensure:
1. Output file exists and has non-zero byte size.
2. Signal-to-Noise Ratio (SNR) relative to input remains above 15 dB.
3. No DC offsets, NaNs, or clipping occurred during processing.

These checks can be performed programmatically via `nasuno.evaluation.comparison.quick_compare`:

```python
from nasuno.evaluation.comparison import quick_compare

results = quick_compare("original.wav", "cleaned.wav")
assert results["snr_db"] > 15.0
assert not results["has_clipping"]
```
