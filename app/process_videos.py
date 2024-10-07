import pandas as pd
import os
from app.download_handler import download_audio_from_youtube, get_video_duration
from app.transcription_handler import transcribe_audio

# Cargar el archivo Excel con las URLs
def process_excel(file_path='./data/mock_video_urls.xlsx'):
    df = pd.read_excel(file_path)

    for index, row in df.iterrows():
        url = row['URL']
        audio_output_dir = './content/audio'

        # Obtener la duración del video
        duration = get_video_duration(url)
        
        # Verificar si la duración supera los 2 minutos (120 segundos)
        if duration and duration > 120:
            df.at[index, 'Transcripción'] = 'El video excede los 2 minutos'
            print(f"Video en {url} excede los 2 minutos, omitiendo transcripción.")
            continue  # Saltar este video y continuar con los demás

        # Si el video es de menos de 2 minutos, proceder con la descarga y transcripción
        success = download_audio_from_youtube(url, audio_output_dir)
        if success:
            audio_file = os.path.join(audio_output_dir, os.listdir(audio_output_dir)[-1])  # Tomar el último archivo descargado
            
            # Transcribir el audio
            transcript = transcribe_audio(audio_file)

            if transcript:
                df.at[index, 'Transcripción'] = transcript  # Guardar la transcripción en el DataFrame
            else:
                df.at[index, 'Transcripción'] = 'Error en transcripción'

            # Eliminar el archivo de audio para optimizar el espacio
            try:
                os.remove(audio_file)
                print(f"Archivo {audio_file} eliminado.")
            except Exception as e:
                print(f"Error al eliminar {audio_file}: {e}")
        else:
            df.at[index, 'Transcripción'] = 'URL inválida o error en descarga'

    # Guardar el DataFrame actualizado en el Excel
    df.to_excel(file_path, index=False)
