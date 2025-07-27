# 🎵 ClearVoice Audio Processor

A user-friendly GUI application for speech enhancement, separation, and target speaker extraction using the ClearVoice library and MossFormer2 models.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)

## ⚠️ Important Notice

**This repository was primarily built with AI assistance** as a quick solution to finish some batch processing of audio files I needed to do. While the code has been tested, the functionality is not guaranteed to work perfectly in all environments or use cases. This is an experimental project and should be used accordingly.

**🤖 AI-Generated Code Disclaimer:**
- Code may contain bugs or edge cases not fully tested
- Functionality may vary across different systems
- Performance and reliability are not guaranteed
- Built quickly for a specific batch processing need

**We welcome community contributions!** If you encounter issues, have suggestions, or want to improve the code, please:
- 🐛 Report bugs via [Issues](../../issues)
- 🔧 Submit fixes and improvements via Pull Requests
- 💡 Share suggestions and feature requests
- 📚 Help improve documentation

Your contributions help make this tool better for everyone!

## ✨ Features

- **🎯 Multiple Audio Processing Tasks**
  - Speech Enhancement (noise reduction)
  - Speech Separation (isolating speakers)
  - Target Speaker Extraction

- **🖱️ Intuitive GUI Interface**
  - Drag & drop file support
  - Batch processing capabilities
  - Real-time processing log
  - Progress tracking

- **📁 Flexible File Handling**
  - Support for multiple audio formats (WAV, MP3, OGG, MP4)
  - Batch processing of folders
  - Custom output directory selection

- **⚡ Advanced Features**
  - Multi-threaded processing for responsive UI
  - File list management (add, remove, clear)
  - Auto-close option after processing
  - Real-time status updates

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Windows, macOS, or Linux

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ClearVoice
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📋 Requirements

The application requires the following Python packages:

- `tkinterdnd2` - For drag and drop functionality
- `clearvoice` - Core audio processing library
- Standard library modules (included with Python):
  - `tkinter` - GUI framework
  - `threading` - Multi-threading support
  - `os` - Operating system interface

## 🎮 Usage

### Basic Workflow

1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Add Audio Files**
   - Drag and drop files/folders into the drop area, OR
   - Click the drop area to browse and select files

3. **Configure Settings**
   - Choose processing task from dropdown:
     - `speech_enhancement` - Remove background noise
     - `speech_separation` - Separate multiple speakers
     - `target_speaker_extraction` - Extract specific speaker
   - Select output folder for processed files

4. **Start Processing**
   - Click "🚀 Start Processing" button
   - Monitor progress in the log window
   - Processed files will be saved to the output directory

### Supported Audio Formats

- **WAV** (.wav) - Recommended for best quality
- **MP3** (.mp3) - Compressed audio format
- **OGG** (.ogg) - Open-source audio format
- **MP4** (.mp4) - Video files (audio will be extracted)

### File Naming Convention

Processed files are automatically renamed with the model name:
```
original_filename_MossFormer2_SE_48K.wav
```

## 🔧 Available Models

| Task | Model | Description |
|------|-------|-------------|
| Speech Enhancement | `MossFormer2_SE_48K` | Removes background noise (48kHz) |
| Speech Separation | `MossFormer2_SS_16K` | Separates multiple speakers (16kHz) |
| Target Speaker Extraction | `AV_MossFormer2_TSE_16K` | Extracts specific speaker (16kHz) |

## 🏗️ Project Structure

```
ClearVoice/
├── main.py                     # Main GUI application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── checkpoints/                # Model checkpoints directory
    └── MossFormer2_SE_48K/
        ├── last_best_checkpoint
        ├── last_best_checkpoint.pt
        └── README.md
```

## 🎨 GUI Features

### Main Interface Components

- **📁 Input Files Section**
  - Drag & drop area for easy file addition
  - File list with selection capabilities
  - File count display
  - Remove selected/clear all buttons

- **⚙️ Configuration Section**
  - Processing task selection dropdown
  - Output folder selection
  - Browse button for folder selection

- **🚀 Processing Section**
  - Start processing button
  - Auto-close option checkbox
  - Status indicator
  - Progress bar

- **📋 Processing Log**
  - Real-time processing updates
  - Success/error message display
  - Scrollable text area

### Keyboard Shortcuts

- **Ctrl+A** - Select all files in list
- **Delete** - Remove selected files
- **Escape** - Clear selection

## 🔬 Technical Details

### Architecture

- **GUI Framework**: Tkinter with custom styling
- **Drag & Drop**: tkinterdnd2 library
- **Audio Processing**: ClearVoice library with MossFormer2 models
- **Threading**: Separate thread for audio processing to maintain UI responsiveness

### Performance Considerations

- Multi-threaded processing prevents UI freezing
- Batch processing for efficiency
- Memory-efficient file handling
- Progress tracking for long operations

## 🐛 Troubleshooting

### Common Issues

1. **Import Error: tkinterdnd2**
   ```bash
   pip install tkinterdnd2
   ```

2. **Import Error: clearvoice**
   ```bash
   pip install clearvoice
   ```

3. **Model Download Issues**
   - Ensure stable internet connection
   - Models are downloaded automatically on first use
   - Check firewall settings if download fails

4. **Audio Format Not Supported**
   - Convert audio to WAV format for best compatibility
   - Ensure file is not corrupted

### Error Messages

- **"No files selected"** - Add audio files before processing
- **"No output folder selected"** - Choose an output directory
- **"Processing Error"** - Check audio file format and integrity

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ClearVoice](https://github.com/modelscope/ClearerVoice-Studio) - Core audio processing library
- [MossFormer2](https://github.com/modelscope/ClearerVoice-Studio) - State-of-the-art audio processing models
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) - Drag and drop functionality

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](../../issues)
3. Create a new [Issue](../../issues/new) with detailed information

---

**Made with ❤️ for the audio processing community**
