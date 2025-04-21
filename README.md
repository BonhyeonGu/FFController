<div align="center">

<h1>FF Controller</h1>
A service that supports experiments using CUDA and FFmpeg.<br/><br/>

<picture><img src="https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=FFFFFF" alt="..."></picture>
<picture><img src="https://img.shields.io/badge/-CUDA-76B900?style=flat-square&logo=nvidia&logoColor=FFFFFF" alt="..."></picture>
<picture><img src="https://img.shields.io/badge/-Python3-3776AB?style=flat-square&logo=python&logoColor=FFFFFF" alt="..."></picture>
<picture><img src="https://img.shields.io/badge/-Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=FFFFFF" alt="..."></picture>
<picture><img src="https://img.shields.io/badge/-FFMPEG-007808?style=flat-square&logo=ffmpeg&logoColor=FFFFFF" alt="..."></picture>

</div>

## Acknowledgment

This repository is intended solely for development purposes and not for deployment. The deployment repository is managed under the authority of the [AIDT Lab](https://aidtlab-dau.github.io/) at Dong-A University.

## Demo

<div align="center">

![Demo](https://github.com/user-attachments/assets/0f14420c-a12b-4ba0-a715-c6431ad9adb5)  
![Demo](https://github.com/user-attachments/assets/8bdd13ef-c9aa-49dd-b311-df92b803e459)


</div>

## Description

A Docker image with CUDA and FFmpeg pre-installed is provided, along with a service that simplifies handling FFmpeg-related processes.

## Function

- Environment with CUDA and FFmpeg support
- Automatic restart of FFmpeg processes upon abnormal termination
- Process restart in case of network-related issues
- Monitoring running FFmpeg commands and deleting additional ones(ing)

## Install

Modify the NVIDIA CUDA image in the Dockerfile, adjust the ports and GPU information in the docker-compose.yml file, review the rtsp-simple-server.yml configuration, and then run the following command: ```docker compose up```

<br/><br/>
---
<details>
  <summary><strong>Experiment based on the number of ffmpeg and encoders/decoders</strong></summary>
  <br/>Creating separate processes for each session resulted in significantly higher performance<br/>
  than opening multiple sessions with a single ffmpeg process. Therefore, we will fix it so that each process has only one session.<br/><br/>

  Each test condition is listed in the format:<br/>
**Preset, Resolution, Frame rate, Number of sessions**<br/>

All values in the table represent **average FPS (Frames Per Second)** under the specified condition.<br/>

---

### Test: 5, 1280x960, 15 FPS, 12 sessions

| Metric                  | RTX A6000 | A16    |
|-------------------------|-----------|--------|
| Avg. Encoder Usage (%) | 71.59     | 51.12  |
| Avg. Decoder Usage (%) | 8.77      | 4.89   |
| Avg. Frame Rate (FPS)  | 21.59     | 17.77  |

---

### Test: 5, 1280x960, 15 FPS, 3 sessions

| Metric                  | RTX A6000 | A16    |
|-------------------------|-----------|--------|
| Avg. Encoder Usage (%) | 12.59     | 11.19  |
| Avg. Decoder Usage (%) | 1.21      | 1.00   |
| Avg. Frame Rate (FPS)  | 18.81     | 16.93  |

---

### Test: 5, 3820x2160, 15 FPS, 3 sessions

| Metric                  | RTX A6000 | A16    |
|-------------------------|-----------|--------|
| Avg. Encoder Usage (%) | 57.58     | 51.15  |
| Avg. Decoder Usage (%) | 4.32      | 3.52   |
| Avg. Frame Rate (FPS)  | 9.12      | 7.92   |

---

### Test: 5, 3820x2160, 15 FPS, 10 sessions

| Metric                  | RTX A6000 | A16    |
|-------------------------|-----------|--------|
| Avg. Encoder Usage (%) | 65.23     | 35.04  |
| Avg. Decoder Usage (%) | 16.79     | 7.92   |
| Avg. Frame Rate (FPS)  | 11.42     | 6.40   |

---
---

### Streaming Performance: 4K (3820x2160), 15 FPS, 3 Sessions

Each test varies by the number of **active presets**.  
All values represent **average performance metrics** (FPS or percentage usage).

---

### Test: 5 Presets

| Metric                  | RTX A6000 | A16    |
|-------------------------|-----------|--------|
| Avg. Encoder Usage (%) | 57.58     | 51.15  |
| Avg. Decoder Usage (%) | 4.32      | 3.52   |
| Avg. Frame Rate (FPS)  | 9.12      | 7.92   |

---

### Test: 4 Presets

| Metric                  | RTX A6000 | A16    |
|-------------------------|-----------|--------|
| Avg. Encoder Usage (%) | 45.33     | 39.48  |
| Avg. Decoder Usage (%) | 4.41      | 3.44   |
| Avg. Frame Rate (FPS)  | 9.15      | 9.31   |

---

### Test: 3 Presets

| Metric                  | RTX A6000 | A16    |
|-------------------------|-----------|--------|
| Avg. Encoder Usage (%) | 33.03     | 27.60  |
| Avg. Decoder Usage (%) | 4.35      | 3.53   |
| Avg. Frame Rate (FPS)  | 10.24     | 9.77   |

---
---
Therefore, further investigation is needed to determine whether increasing the number of encoders provides a tangible advantage.
</details>
