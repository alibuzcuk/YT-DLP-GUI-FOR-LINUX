#!/bin/bash

# YT-Downloader AppImage Build Script
# Bu script programı tek AppImage dosyası olarak derler

set -e  # Hata olursa dur

APP_NAME="YT-DLP-GUI"
PYTHON_VERSION="3.11"  # Uyumlu Python versiyonu

echo "========================================="
echo "YT-DLP-GUI AppImage Builder"
echo "========================================="

# 1. Gerekli paketleri kontrol et
echo ""
echo "[1/8] Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı. Lütfen kurun: sudo apt install python3"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 bulunamadı. Lütfen kurun: sudo apt install python3-pip"
    exit 1
fi

echo "✅ Dependencies OK"

# 2. Python paketlerini kur
echo ""
echo "[2/8] Installing Python packages..."
pip3 install --user pyinstaller yt-dlp 2>/dev/null || pip3 install pyinstaller yt-dlp

# 3. ffmpeg statik binary indir
echo ""
echo "[3/8] Downloading ffmpeg static binary..."

if [ ! -d "ffmpeg-static" ]; then
    wget -q --show-progress https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
    tar xf ffmpeg-release-amd64-static.tar.xz
    mv ffmpeg-*-amd64-static ffmpeg-static
    rm ffmpeg-release-amd64-static.tar.xz
    echo "✅ ffmpeg downloaded"
else
    echo "✅ ffmpeg already exists"
fi

# 4. appimagetool indir
echo ""
echo "[4/8] Downloading appimagetool..."

if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    wget -q --show-progress https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
    echo "✅ appimagetool downloaded"
else
    echo "✅ appimagetool already exists"
fi

# 5. PyInstaller ile derle
echo ""
echo "[5/8] Building with PyInstaller..."

# Eski build dosyalarını temizle
rm -rf build dist *.spec

pyinstaller --onefile \
    --windowed \
    --add-binary "ffmpeg-static/ffmpeg:." \
    --add-binary "ffmpeg-static/ffprobe:." \
    --name "$APP_NAME" \
    --hidden-import=tkinter \
    --hidden-import=_tkinter \
    yt-dlp-gui.py

echo "✅ PyInstaller build complete"

# 6. AppDir yapısı oluştur
echo ""
echo "[6/8] Creating AppDir structure..."

APP_DIR="${APP_NAME}.AppDir"
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR/usr/bin"
mkdir -p "$APP_DIR/usr/share/applications"
mkdir -p "$APP_DIR/usr/share/icons/hicolor/256x256/apps"

# Binary'yi kopyala
cp "dist/$APP_NAME" "$APP_DIR/usr/bin/"
chmod +x "$APP_DIR/usr/bin/$APP_NAME"

# Desktop dosyası oluştur
cat > "$APP_DIR/$APP_NAME.desktop" <<EOF
[Desktop Entry]
Name=YT-DLP-GUI
Comment=Download YouTube videos easily
Exec=$APP_NAME
Icon=yt-dlp-gui
Type=Application
Categories=Network;AudioVideo;
Terminal=false
EOF

# AppRun scripti oluştur (DÜZELTME: APP_NAME kullan)
cat > "$APP_DIR/AppRun" <<EOF
#!/bin/bash
SELF=\$(readlink -f "\$0")
HERE=\${SELF%/*}
export PATH="\${HERE}/usr/bin:\${PATH}"
export LD_LIBRARY_PATH="\${HERE}/usr/lib:\${LD_LIBRARY_PATH}"
cd "\${HERE}/usr/bin"
exec "\${HERE}/usr/bin/$APP_NAME" "\$@"
EOF

chmod +x "$APP_DIR/AppRun"

# Logo dosyasını kopyala (eğer varsa) veya basit ikon oluştur
if [ -f "yt-dlp-gui.svg" ]; then
    cp "yt-dlp-gui.svg" "$APP_DIR/yt-dlp-gui.svg"
    cp "yt-dlp-gui.svg" "$APP_DIR/.DirIcon"
    echo "✅ Logo copied"
else
    # Basit bir ikon oluştur
    cat > "$APP_DIR/yt-dlp-gui.svg" <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
  <!-- Arka plan gradient -->
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF0000;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#CC0000;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="playGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#FFFFFF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#F0F0F0;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="arrowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#4CAF50;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#45a049;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
      <feOffset dx="0" dy="2" result="offsetblur"/>
      <feComponentTransfer>
        <feFuncA type="linear" slope="0.3"/>
      </feComponentTransfer>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="256" height="256" fill="url(#bgGrad)" rx="45"/>
  <g filter="url(#shadow)">
    <rect x="48" y="68" width="160" height="100" fill="url(#playGrad)" rx="12"/>
    <polygon points="100,88 100,148 160,118" fill="#FF0000"/>
  </g>
  <g filter="url(#shadow)">
    <rect x="115" y="170" width="26" height="45" fill="url(#arrowGrad)" rx="4"/>
    <polygon points="128,215 100,190 156,190" fill="url(#arrowGrad)"/>
  </g>
  <g opacity="0.3">
    <line x1="90" y1="195" x2="70" y2="195" stroke="white" stroke-width="3" stroke-linecap="round"/>
    <line x1="166" y1="195" x2="186" y2="195" stroke="white" stroke-width="3" stroke-linecap="round"/>
    <line x1="90" y1="205" x2="75" y2="205" stroke="white" stroke-width="2" stroke-linecap="round"/>
    <line x1="166" y1="205" x2="181" y2="205" stroke="white" stroke-width="2" stroke-linecap="round"/>
  </g>
</svg>
EOF
    cp "$APP_DIR/yt-dlp-gui.svg" "$APP_DIR/.DirIcon"
    echo "✅ Default logo created"
fi

echo "✅ AppDir structure created"

# 7. AppImage oluştur
echo ""
echo "[7/8] Creating AppImage..."

ARCH=x86_64 ./appimagetool-x86_64.AppImage "$APP_DIR" "$APP_NAME-x86_64.AppImage"

echo "✅ AppImage created"

# 8. Temizlik
echo ""
echo "[8/8] Cleaning up..."
rm -rf build "$APP_DIR" *.spec

echo ""
echo "========================================="
echo "✅ BUILD SUCCESSFUL!"
echo "========================================="
echo ""
echo "AppImage dosyanız: $APP_NAME-x86_64.AppImage"
echo ""
echo "Çalıştırmak için:"
echo "  chmod +x $APP_NAME-x86_64.AppImage"
echo "  ./$APP_NAME-x86_64.AppImage"
echo ""
echo "Not: AppImage'i istediğiniz yere taşıyabilirsiniz!"
echo "========================================"