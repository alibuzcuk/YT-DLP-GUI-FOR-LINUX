# YT-DLP-GUI 🎥⬇️

![yt_downloader_logo](https://github.com/user-attachments/assets/c245fcbb-44fa-49cb-8288-66e9a91771ca)<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">

## ✨ Features

- 🎨 **Modern GUI** - Clean and intuitive interface with dark/light theme support
- 🌍 **Multi-language** - English, Turkish (Türkçe), and Arabic (العربية)
- 📊 **Real-time Progress** - Live download progress with speed and ETA
- 🎬 **High Quality** - Downloads up to 1080p with automatic format selection
- 📦 **Portable AppImage** - Single file, no installation required
- 🔧 **Built-in ffmpeg** - No external dependencies needed
- 🎯 **Smart Bot Detection Bypass** - Advanced anti-bot measures
- 💾 **Persistent Settings** - Remembers your language and theme preferences

## 🚀 Quick Start

### Download & Run

1. Download the latest release: `YT-DLP-GUI-x86_64.AppImage`
2. Make it executable:
```bash
chmod +x YT-DLP-GUI-x86_64.AppImage
```
3. Run it:
```bash
./YT-DLP-GUI-x86_64.AppImage
```

That's it! No installation, no dependencies!

## 🛠️ Build From Source

### Prerequisites
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-tk

# Fedora/RHEL
sudo dnf install python3 python3-pip python3-tkinter
```

### Build AppImage
```bash
# Clone the repository
git clone https://github.com/yourusername/yt-dlp-gui.git
cd yt-dlp-gui

# Run build script
chmod +x build.sh
./build.sh
```

The script will automatically:
- ✅ Install Python dependencies (yt-dlp, pyinstaller)
- ✅ Download static ffmpeg binary
- ✅ Build the application with PyInstaller
- ✅ Create portable AppImage

## 📖 Usage

1. **Select Download Folder** - Click "Select Folder" button
2. **Paste YouTube Link** - Enter video URL
3. **Download** - Click "Download Video" button
4. **Wait** - Watch real-time progress with speed and ETA

### Features

#### 🎨 Themes
- **Light Theme** - For daytime use
- **Dark Theme** - Easy on the eyes (default)

#### 🌍 Languages
- **English** - Full English interface
- **Türkçe** - Turkish translation
- **العربية** - Arabic with RTL support

## 🔧 Configuration

Settings are automatically saved in `~/.config/yt-dlp-gui/config.json`

### Bot Detection Bypass

If YouTube blocks downloads, add cookies:

```bash
# 1. Install browser extension: "Get cookies.txt"
# 2. Export YouTube cookies
# 3. Save to:
cp cookies.txt ~/.config/yt-dlp-gui/cookies.txt
```

## 📦 Technical Details

### Built With
- **Python 3.11+** - Core application
- **Tkinter** - GUI framework
- **yt-dlp** - YouTube download engine
- **ffmpeg** - Video/audio processing
- **PyInstaller** - Application packaging

### Format Selection
- Primary: Best quality up to 1080p MP4
- Fallback: Alternative formats if primary fails
- Auto-merge: Video + audio → single MP4 file

### Anti-Bot Features
- Android player client emulation
- Realistic browser headers
- Cookie-based authentication support
- Dynamic user-agent rotation

## 🐛 Troubleshooting

### "Bot detected" error
```bash
# Update yt-dlp
pip install --upgrade yt-dlp

# Add cookies (see Configuration section)
```

### "No module named tkinter"
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Download fails
- Check internet connection
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Try different video (some may be region-blocked)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### To Do
- [ ] Playlist support
- [ ] Audio-only download option
- [ ] Custom quality selection
- [ ] Download queue
- [ ] Video preview
- [ ] Subtitle download

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful YouTube downloader
- [ffmpeg](https://ffmpeg.org/) - Multimedia processing
- [PyInstaller](https://pyinstaller.org/) - Application bundling

## ⚠️ Disclaimer

This tool is for personal use only. Please respect copyright laws and YouTube's Terms of Service. Download only videos you have permission to download.

## 📞 Support

- 🐛 Report bugs: [GitHub Issues](https://github.com/yourusername/yt-dlp-gui/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/yt-dlp-gui/discussions)
- ⭐ Star this project if you find it useful!

---

**Made with ❤️ for the Linux community**
