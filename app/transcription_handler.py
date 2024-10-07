import whisper
import os

# Función para transcribir un archivo de audio usando Whisper
def transcribe_audio(audio_file):
    model = whisper.load_model("small")  # Carga el modelo Whisper
    try:
        result = model.transcribe(audio_file)
        return result['text']  # Retorna la transcripción
    except Exception as e:
        print(f"Error al transcribir {audio_file}: {e}")
        return None  # Retorna None si hay un error