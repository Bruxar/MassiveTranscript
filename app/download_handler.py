import yt_dlp as youtube_dl
import os

# Función para obtener la duración del video en segundos
def get_video_duration(youtube_url):
    ydl_opts = {
        'skip_download': True,  # No descarga el video, solo obtiene la información
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(youtube_url, download=False)
            duration = info_dict.get('duration', None)  # Duración en segundos
            return duration
        except Exception as e:
            print(f"Error al obtener la duración del video {youtube_url}: {e}")
            return None

# Función para descargar el audio desde un video de YouTube
def download_audio_from_youtube(youtube_url, output_dir='./content/audio'):
    # Asegurarse de que la carpeta exista
    os.makedirs(output_dir, exist_ok=True)
    
    # Opciones de descarga de yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Plantilla para el nombre del archivo
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return True  # Retornar éxito si se descarga correctamente
    except Exception as e:
        print(f"Error al descargar {youtube_url}: {e}")
        return False  # Retornar fallo si hay un error
