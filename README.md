<div align="center">

<h1>FF Controller</h1>
A service that supports experiments using CUDA and FFmpeg.<br/><br/>

<picture><img src="https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=FFFFFF" alt="..."></picture>
<picture><img src="https://img.shields.io/badge/-CUDA-76B900?style=flat-square&logo=nvidia&logoColor=FFFFFF" alt="..."></picture>
<picture><img src="https://img.shields.io/badge/-Python3-3776AB?style=flat-square&logo=python&logoColor=FFFFFF" alt="..."></picture>
<picture><img src="https://img.shields.io/badge/-Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=FFFFFF" alt="..."></picture>
<picture><img src="https://img.shields.io/badge/FFMPEG-007808?style=flat-square&logo=ffmpeg&logoColor=FFFFFF" alt="..."></picture>

</div>

## Acknowledgment

This repository is intended solely for development purposes and not for deployment. The deployment repository is managed under the authority of the [DT-DL Lab]() at Dong-A University.

## Demo

<div align="center">

![Demo](https://github.com/user-attachments/assets/0f14420c-a12b-4ba0-a715-c6431ad9adb5)

</div>

## Description

A Docker image with CUDA and FFmpeg pre-installed is provided, along with a service that simplifies handling FFmpeg-related processes.

## Function

- Environment with CUDA and FFmpeg support
- Automatic restart of FFmpeg processes upon abnormal termination
- Process restart in case of network-related issues

## Install

Modify the NVIDIA CUDA image in the Dockerfile, adjust the ports and GPU information in the docker-compose.yml file, review the rtsp-simple-server.yml configuration, and then run the following command: ```docker compose up```
