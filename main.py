import flet as ft
from app.process_videos import process_excel

# Crear la interfaz gráfica
def main(page: ft.Page):
    page.title = "Transcriptor de Videos"
    page.window.width = 500
    page.window.height = 600

    # Inputs para subir Excel y configurar las columnas
    url_column_input = ft.TextField(label="Nombre de la columna de URLs", value="URL")
    transcript_column_input = ft.TextField(label="Nombre de la columna de transcripción", value="Transcripción")
    
    # Variable global para almacenar la ruta del archivo Excel cargado
    excel_file_path = None

    # Barra de progreso
    progress_bar = ft.ProgressBar(width=500, value=0)

    # Área de mensajes y progreso
    log_area = ft.Column(scroll=ft.ScrollMode.AUTO)

    # Función para actualizar la ruta del archivo al cargar un Excel
    def file_uploaded(e):
        nonlocal excel_file_path
        if e.files:
            excel_file_path = e.files[0].path
            log_area.controls.append(ft.Text(f"Archivo cargado: {e.files[0].name}"))
            page.update()

    # Botón para iniciar el procesamiento
    def start_processing(e):
        # Resetear barra de progreso y log
        progress_bar.value = 0
        log_area.controls.clear()
        page.update()

        process_excel(
            excel_file_path,  # Usar la ruta del archivo subido
            url_column_input.value, 
            transcript_column_input.value,
            page,
            progress_bar,  # Pasar la barra de progreso
            log_area       # Pasar el área de log para los mensajes
        )
        page.update()

    process_button = ft.ElevatedButton(
        text="Procesar Videos",
        icon=ft.icons.VIDEO_CALL,  # Ícono de video
        on_click=start_processing
    )

    # File picker
    file_picker = ft.FilePicker(on_result=file_uploaded)

    page.overlay.append(file_picker)

    # Botón para abrir el file picker
    upload_button = ft.ElevatedButton(
        text="Subir Excel",
        icon=ft.icons.UPLOAD_FILE,  # Ícono de subir archivo
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )

    # Colocar ambos botones en la misma fila (Row)
    button_row = ft.Row(
        controls=[upload_button, process_button],
        alignment=ft.MainAxisAlignment.START  # Alinear al principio
    )

    # Agregar los elementos a la página
    page.add(
        url_column_input,
        transcript_column_input,
        button_row,
        progress_bar,  # Barra de progreso
        log_area       # Área de mensajes
    )

ft.app(target=main)
