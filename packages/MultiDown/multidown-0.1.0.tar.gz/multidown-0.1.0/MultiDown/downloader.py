import yt_dlp
import ffmpeg

def download_media(url, format_, quality):
    options = {}
    if format_ == "mp3":
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    else:
        options = {
            'format': f"bestvideo[height<={quality}]+bestaudio/best",
            'outtmpl': '%(title)s.%(ext)s'
        }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        return "✅ Download completed."
    except Exception as e:
        return f"❌ Error: {str(e)}"
