# Payload-Crypt

A small security research repository focused on download-and-execute behavior and PowerShell command obfuscation in a controlled lab environment.

> This project is intended for malware analysis, detection engineering, and defensive testing only.  
> Do not use it against systems you do not own or do not have explicit permission to test.

## Overview

This repository contains sample files and scripts that simulate a simple file delivery workflow and obfuscated PowerShell command patterns commonly seen in endpoint investigations.

The main components are:

- `simple_service.py` — a minimal HTTP server that serves a chosen file as a download.
- `work_sample.txt` — a sample keystroke payload demonstrating a scripted download-and-launch workflow.
- `powershell_iwr_obfuscation.txt` — examples of obfuscated `Invoke-WebRequest`-style command construction.
- `rc4.EXE` — a related sample from the repository used in encryption/decryption research. For more information, check the repository: https://github.com/hwxrqz/payload-crypt/tree/master

## Repository Goals

This project is meant to help with:

- understanding file-delivery patterns in incident response
- studying obfuscated PowerShell command lines
- building detections for suspicious download-and-execute behavior
- testing sandbox, EDR, and SIEM analytics in a safe lab

## Files

### `simple_service.py`
A simple Python HTTP server that serves one file for download with a `Content-Disposition: attachment` header.

Intended use in a lab:
- host a sample file locally
- verify how tools and defenses react to a controlled download source

### `work_sample.txt`
A scripted input sample that demonstrates a sequence of keystrokes used to open PowerShell, fetch a file, run it, and close the window. Useful with Flipper Zero's BadUSB

### `powershell_iwr_obfuscation.txt`
A set of obfuscated PowerShell examples showing how a URL can be assembled dynamically to evade simple string-based detection. Can be used in `work_sample.txt`

## Setup

### Requirements
- Python 3.8+
- A local lab environment
- Windows test VM for PowerShell analysis

### Run the HTTP server

```bash
python3 simple_service.py <path-to-file>
