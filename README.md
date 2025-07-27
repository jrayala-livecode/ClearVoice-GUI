# 🎵 ClearVoice Audio Processor

GUI application for speech enhancement, separation, and target speaker extraction using ClearVoice library and MossFormer2 models.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)

## ⚠️ Important Notice

**AI-generated code for quick batch audio processing.** Functionality not guaranteed - built fast for a specific need. PRs and bug reports welcome!

## ✨ Features

- Speech Enhancement, Separation, Target Speaker Extraction
- Drag & drop GUI with batch processing
- Multi-threaded processing, progress tracking
- Supports WAV, MP3, OGG, MP4 formats

## 🚀 Quick Start

```bash
git clone <repository-url>
cd ClearVoice
pip install -r requirements.txt
python main.py
```

## Requirements

- `tkinterdnd2` - Drag and drop
- `clearvoice` - Audio processing

## Usage

1. Drag audio files into the app
2. Select processing task (enhancement/separation/extraction)
3. Choose output folder
4. Click "Start Processing"

## Available Models

| Task | Model | Sample Rate |
|------|-------|-------------|
| Speech Enhancement | `MossFormer2_SE_48K` | 48kHz |
| Speech Separation | `MossFormer2_SS_16K` | 16kHz |
| Target Speaker Extraction | `AV_MossFormer2_TSE_16K` | 16kHz |

## Troubleshooting

Common fixes:
- `pip install tkinterdnd2 clearvoice` for import errors
- Ensure stable internet for model downloads
- Use WAV format for best compatibility

## 🙏 Acknowledgments

- [ClearVoice](https://github.com/modelscope/ClearerVoice-Studio) - Core audio processing library
- [MossFormer2](https://github.com/modelscope/ClearerVoice-Studio) - Audio processing models
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) - Drag and drop functionality

---

**Made with ❤️ and AI assistance**
