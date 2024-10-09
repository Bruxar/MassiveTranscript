import pandas as pd
import os
import flet as ft
from app.download_handler import download_audio_from_youtube, get_video_duration
from app.transcription_handler import transcribe_audio

# Función para procesar el Excel
def process_excel(file_path, url_column, transcript_column, page, progress_bar, log_area):
    # Leer el archivo Excel subido por el usuario
    df = pd.read_excel(file_path)

    # Verificar si la columna de transcripción existe, si no, crearla
    if transcript_column not in df.columns:
        df[transcript_column] = None  # Crear la columna de transcripción vacía

    total_videos = len(df)  # Obtener el total de videos para la barra de progreso
    processed_videos = 0  # Contador para la barra de progreso

    # Procesar cada URL en el archivo
    for index, row in df.iterrows():
        url = row[url_column]
        audio_output_dir = './content/audio'

        # Obtener la duración del video
        duration = get_video_duration(url)

        # Verificar si la duración supera los 2 minutos (120 segundos)
        if duration and duration > 120:
            df.at[index, transcript_column] = 'El video excede los 2 minutos'
            log_area.controls.append(ft.Text(f"Video en {url} excede los 2 minutos, omitiendo transcripción."))
            page.update()
            continue

        # Descargar y procesar el video
        success = download_audio_from_youtube(url, audio_output_dir)
        if success:
            audio_file = os.path.join(audio_output_dir, os.listdir(audio_output_dir)[-1])

            transcript = transcribe_audio(audio_file)
            if transcript:
                df.at[index, transcript_column] = transcript
                log_area.controls.append(ft.Text(f"Transcripción completada para {url}."))
            else:
                df.at[index, transcript_column] = 'Error en transcripción'
                log_area.controls.append(ft.Text(f"Error en transcripción para {url}."))
            
            # Eliminar el archivo de audio
            os.remove(audio_file)
        else:
            df.at[index, transcript_column] = 'Error en descarga'
            log_area.controls.append(ft.Text(f"Error en la descarga del video {url}."))
        
        # Actualizar la barra de progreso
        processed_videos += 1
        progress_bar.value = processed_videos / total_videos
        page.update()

    # Guardar el DataFrame actualizado en el Excel
    df.to_excel(file_path, index=False)
    log_area.controls.append(ft.Text("Procesamiento completado."))
    page.update()
