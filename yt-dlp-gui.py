import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import json
import re
from datetime import datetime, timedelta
import shutil
import yt_dlp

# Translation Dictionary
translations = {
    'en': {
        'title': "YouTube Video Downloader",
        'link_label': "YouTube Link:",
        'folder_button': "Select Folder",
        'path_label_default': "No folder selected yet",
        'download_button': "Download Video",
        'message_downloading': "Video is downloading, please wait...",
        'message_success_title': "Success",
        'message_success_body': "Video downloaded successfully!",
        'error_title': "Error",
        'error_no_link': "Please enter a YouTube link.",
        'error_no_folder': "Please select download folder.",
        'error_download': "An error occurred during download: ",
        'theme_menu': "Theme",
        'light_theme': "Light Theme",
        'dark_theme': "Dark Theme",
        'download_progress': "Downloading:",
        'download_speed': "Speed:",
        'download_eta': "ETA:",
        'download_size': "Size:"
    },
    'tr': {
        'title': "YouTube Video İndirici",
        'link_label': "YouTube Linki:",
        'folder_button': "Klasör Seç",
        'path_label_default': "Henüz klasör seçilmedi",
        'download_button': "Videoyu İndir",
        'message_downloading': "Video indiriliyor, lütfen bekleyin...",
        'message_success_title': "Başarılı",
        'message_success_body': "Video başarıyla indirildi!",
        'error_title': "Hata",
        'error_no_link': "Lütfen bir YouTube linki girin.",
        'error_no_folder': "Lütfen indirme klasörünü seçin.",
        'error_download': "İndirme sırasında bir sorun oluştu: ",
        'theme_menu': "Tema",
        'light_theme': "Açık Tema",
        'dark_theme': "Karanlık Tema",
        'download_progress': "İndiriliyor:",
        'download_speed': "Hız:",
        'download_eta': "Kalan:",
        'download_size': "Boyut:"
    },
    'ar': {
        'title': "مُنزِّل فيديوهات يوتيوب",
        'link_label': "رابط يوتيوب:",
        'folder_button': "اختيار مجلّد",
        'path_label_default': "لم يتم اختيار مجلد بعد",
        'download_button': "تحميل الفيديو",
        'message_downloading': "يتم تحميل الفيديو، يرجى الانتظار...",
        'message_success_title': "نجاح",
        'message_success_body': "تم تحميل الفيديو بنجاح!",
        'error_title': "خطأ",
        'error_no_link': "الرجاء إدخال رابط يوتيوب.",
        'error_no_folder': "الرجاء اختيار مجلد التحميل.",
        'error_download': "حدثت مشكلة أثناء التحميل: ",
        'theme_menu': "السمة",
        'light_theme': "السمة الفاتحة",
        'dark_theme': "السمة الداكنة",
        'download_progress': "التحميل:",
        'download_speed': "السرعة:",
        'download_eta': "الوقت المتبقي:",
        'download_size': "الحجم:"
    }
}

# Default language and theme
current_lang = 'en'
current_theme = 'dark'

# Theme colors
themes = {
    'light': {
        'bg': '#ffffff',
        'fg': '#000000',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'button_bg': '#f0f0f0',
        'button_fg': '#000000',
        'button_active_bg': '#e0e0e0',
        'frame_bg': '#ffffff',
        'message_fg': '#0066cc'
    },
    'dark': {
        'bg': '#2b2b2b',
        'fg': '#ffffff',
        'entry_bg': '#404040',
        'entry_fg': '#ffffff',
        'button_bg': '#404040',
        'button_fg': '#ffffff',
        'button_active_bg': '#505050',
        'frame_bg': '#2b2b2b',
        'message_fg': '#4da6ff'
    }
}

def get_config_path():
    """Get the configuration file path in ~/.config/yt-dlp-gui folder."""
    config_dir = os.path.expanduser("~/.config/yt-dlp-gui")
    
    try:
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
    except:
        import tempfile
        config_dir = tempfile.gettempdir()
    
    return os.path.join(config_dir, "config.json")

def get_cookies_path():
    """Get the cookies file path for YouTube authentication."""
    config_dir = os.path.expanduser("~/.config/yt-dlp-gui")
    try:
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
    except:
        pass
    return os.path.join(config_dir, "cookies.txt")

def load_config():
    """Load configuration from config file."""
    config_file = get_config_path()
    default_config = {
        'language': 'en',
        'theme': 'dark'
    }
    
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config
    except:
        pass
    
    return default_config

def save_config(language=None, theme=None):
    """Save configuration to config file."""
    config_file = get_config_path()
    config = load_config()
    
    if language is not None:
        config['language'] = language
    if theme is not None:
        config['theme'] = theme
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    except:
        pass

def get_ffmpeg_path():
    """Find ffmpeg in system PATH."""
    ffmpeg_path = shutil.which('ffmpeg')
    return ffmpeg_path if ffmpeg_path else 'ffmpeg'

def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []
    
    # Check ffmpeg
    if not shutil.which('ffmpeg'):
        missing.append('ffmpeg')
    
    if missing:
        msg = "Missing dependencies:\n\n"
        msg += "\n".join(f"- {dep}" for dep in missing)
        msg += "\n\nPlease install:\n"
        msg += "Ubuntu/Debian: sudo apt install " + " ".join(missing) + "\n"
        msg += "Fedora/RHEL: sudo dnf install " + " ".join(missing)
        messagebox.showerror("Missing Dependencies", msg)
        return False
    return True

def apply_theme():
    """Applies the current theme to all widgets."""
    theme = themes[current_theme]
    
    root.configure(bg=theme['bg'])
    frame.configure(bg=theme['frame_bg'])
    
    link_label.configure(bg=theme['frame_bg'], fg=theme['fg'])
    path_label.configure(bg=theme['frame_bg'], fg=theme['fg'])
    message_label.configure(bg=theme['frame_bg'], fg=theme['message_fg'])
    progress_label.configure(bg=theme['frame_bg'], fg=theme['message_fg'])
    
    link_entry.configure(bg=theme['entry_bg'], fg=theme['entry_fg'], 
                        insertbackground=theme['entry_fg'])
    
    folder_button.configure(bg=theme['button_bg'], fg=theme['button_fg'],
                           activebackground=theme['button_active_bg'])
    indir_button.configure(bg=theme['button_bg'], fg=theme['button_fg'],
                          activebackground=theme['button_active_bg'])
    
    style = ttk.Style()
    if current_theme == 'dark':
        style.theme_use('clam')
        style.configure("TProgressbar",
                       background='#4da6ff',
                       troughcolor=theme['entry_bg'],
                       borderwidth=1,
                       lightcolor=theme['entry_bg'],
                       darkcolor=theme['entry_bg'])
    else:
        style.theme_use('default')
        style.configure("TProgressbar",
                       background='#0066cc',
                       troughcolor='#f0f0f0')

def set_theme(theme):
    """Changes the application theme."""
    global current_theme
    current_theme = theme
    save_config(theme=theme)
    apply_theme()

def set_language(lang):
    """Changes the application language and updates the interface."""
    global current_lang
    current_lang = lang
    save_config(language=lang)
    update_interface()

def update_interface():
    """Updates all interface texts according to current language."""
    t = translations[current_lang]
    root.title(t['title'])
    link_label.config(text=t['link_label'])
    folder_button.config(text=t['folder_button'])
    if not download_path:
        path_label.config(text=t['path_label_default'])
    indir_button.config(text=t['download_button'])
    message_label.config(text="")
    
    theme_menu_label = t['theme_menu']
    for i in range(menu_bar.index("end") + 1):
        try:
            if menu_bar.entrycget(i, "label") in ["Theme", "Tema", "السمة"]:
                menu_bar.entryconfig(i, label=theme_menu_label)
                break
        except:
            continue

def klasor_sec():
    """Allows user to select download folder."""
    global download_path
    download_path = filedialog.askdirectory()
    if download_path:
        path_label.config(text=f"Folder: {download_path}")
        message_label.config(text="")

def update_progress_bar(progress_text, progress_value=0):
    """Update progress bar and progress label."""
    progress_label.config(text=progress_text)
    progress_bar['value'] = progress_value
    root.update_idletasks()

def progress_hook(d):
    """Progress hook for yt-dlp."""
    t = translations[current_lang]
    
    if d['status'] == 'downloading':
        try:
            # Get percentage
            if 'total_bytes' in d and d['total_bytes'] > 0:
                percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate'] > 0:
                percentage = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            else:
                percentage = 0
            
            # Get speed
            speed = d.get('speed', 0)
            if speed:
                if speed > 1024 * 1024:
                    speed_str = f"{speed / (1024 * 1024):.2f} MiB/s"
                elif speed > 1024:
                    speed_str = f"{speed / 1024:.2f} KiB/s"
                else:
                    speed_str = f"{speed:.2f} B/s"
            else:
                speed_str = "Unknown"
            
            # Get ETA
            eta = d.get('eta', 0)
            if eta:
                eta_str = f"{eta}s"
            else:
                eta_str = "Unknown"
            
            # Update progress
            progress_text = f"{t['download_progress']} {percentage:.1f}%"
            if speed_str != "Unknown":
                progress_text += f" | {t['download_speed']} {speed_str}"
            if eta_str != "Unknown":
                progress_text += f" | {t['download_eta']} {eta_str}"
            
            update_progress_bar(progress_text, percentage)
            
        except Exception as e:
            pass
    
    elif d['status'] == 'finished':
        update_progress_bar(f"{t['download_progress']} 100% - Finalizing...", 100)

def run_download(link):
    """Runs download process using yt-dlp library."""
    t = translations[current_lang]
    
    try:
        output_template = os.path.join(download_path, "%(title)s.%(ext)s")
        
        update_progress_bar(t['message_downloading'], 0)
        
        # Get ffmpeg path
        ffmpeg_location = get_ffmpeg_path()
        
        ydl_opts = {
            'format': 'best[height<=1080]/best',
            'outtmpl': output_template,
            'progress_hooks': [progress_hook],
            'merge_output_format': 'mp4',
            'nocheckcertificate': True,
            # Bot algılamasını aşmak için
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            'cookiefile': None,  # Cookie dosyası kullanımı (isteğe bağlı)
            # Ek header'lar
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            }
        }
        
        # Add ffmpeg location if found
        if ffmpeg_location:
            ydl_opts['ffmpeg_location'] = ffmpeg_location
        
        # Add cookies if file exists (helps with bot detection)
        cookies_file = get_cookies_path()
        if os.path.exists(cookies_file):
            ydl_opts['cookiefile'] = cookies_file
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            
            update_progress_bar("Download completed successfully!", 100)
            messagebox.showinfo(t['message_success_title'], t['message_success_body'])
            
        except Exception as e:
            # Try alternative format if first attempt fails
            update_progress_bar("Trying alternative format...", 0)
            
            ydl_opts['format'] = 'worst[height>=480]/worst'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            
            update_progress_bar("Download completed successfully!", 100)
            messagebox.showinfo(t['message_success_title'], t['message_success_body'])
        
    except Exception as e:
        update_progress_bar("Download failed!", 0)
        messagebox.showerror(t['error_title'], f"{t['error_download']}{e}")
    
    indir_button.config(state=tk.NORMAL)
    root.after(3000, lambda: update_progress_bar("", 0))

def indir_video():
    """Function that starts the download process."""
    t = translations[current_lang]
    global download_path
    video_link = link_entry.get()
    
    if not video_link:
        messagebox.showerror(t['error_title'], t['error_no_link'])
        return

    if not download_path:
        messagebox.showerror(t['error_title'], t['error_no_folder'])
        return

    indir_button.config(state=tk.DISABLED)
    message_label.config(text=t['message_downloading'])
    
    download_thread = threading.Thread(target=run_download, args=(video_link,))
    download_thread.daemon = True
    download_thread.start()

# GUI Setup
root = tk.Tk()
root.title(translations[current_lang]['title'])
root.geometry("550x350")

# Check dependencies before continuing
if not check_dependencies():
    root.destroy()
    exit(1)

download_path = ""

# Create main frame
frame = tk.Frame(root, padx=15, pady=15)
frame.pack(padx=15, pady=15, fill="both", expand=True)

# Create widgets
link_label = tk.Label(frame, text=translations[current_lang]['link_label'], font=("Arial", 10))
link_label.grid(row=0, column=0, pady=8, sticky="W")

link_entry = tk.Entry(frame, width=45, font=("Arial", 10))
link_entry.grid(row=0, column=1, pady=8, padx=(10, 0))

folder_button = tk.Button(frame, text=translations[current_lang]['folder_button'], 
                         command=klasor_sec, font=("Arial", 10), relief="raised", bd=2)
folder_button.grid(row=1, column=0, pady=8, sticky="W")

path_label = tk.Label(frame, text=translations[current_lang]['path_label_default'], 
                     font=("Arial", 9))
path_label.grid(row=1, column=1, pady=8, sticky="W", padx=(10, 0))

indir_button = tk.Button(frame, text=translations[current_lang]['download_button'], 
                        command=indir_video, font=("Arial", 11, "bold"), 
                        relief="raised", bd=2, height=2)
indir_button.grid(row=2, column=0, columnspan=2, pady=15)

# Progress bar
progress_bar = ttk.Progressbar(frame, length=400, mode='determinate', maximum=100)
progress_bar.grid(row=3, column=0, columnspan=2, pady=8, sticky="ew")

# Progress label
progress_label = tk.Label(frame, text="", font=("Arial", 9))
progress_label.grid(row=4, column=0, columnspan=2, pady=5)

message_label = tk.Label(frame, text="", font=("Arial", 9))
message_label.grid(row=5, column=0, columnspan=2, pady=8)

# Create menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Language menu
lang_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Language / Dil / اللغة", menu=lang_menu)
lang_menu.add_command(label="English", command=lambda: set_language('en'))
lang_menu.add_command(label="Türkçe", command=lambda: set_language('tr'))
lang_menu.add_command(label="العربية", command=lambda: set_language('ar'))

# Theme menu
theme_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label=translations[current_lang]['theme_menu'], menu=theme_menu)
theme_menu.add_command(label=translations[current_lang]['light_theme'], 
                      command=lambda: set_theme('light'))
theme_menu.add_command(label=translations[current_lang]['dark_theme'], 
                      command=lambda: set_theme('dark'))

# Load config and apply saved settings
try:
    config = load_config()
    saved_lang = config.get('language', 'en')
    saved_theme = config.get('theme', 'dark')
    
    if saved_lang != current_lang:
        current_lang = saved_lang
    if saved_theme != current_theme:
        current_theme = saved_theme
except:
    pass

# Apply initial theme and language
apply_theme()
update_interface()

root.mainloop()