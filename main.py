import flet as ft
from app.process_videos import process_excel

# Crear la interfaz gráfica
def main(page: ft.Page):
    page.title = "Transcriptor de Videos"
    page.window.width = 800
    page.window.height = 600

    # Inputs para subir Excel y configurar las columnas
    url_column_input = ft.TextField(label="Nombre de la columna de URLs", value="URL")
    transcript_column_input = ft.TextField(label="Nombre de la columna de transcripción", value="Transcripción")
    
    # Variables globales para almacenar la ruta del archivo Excel y el archivo de salida
    excel_file_path = None
    save_file_path = None  # Ruta para guardar el archivo de salida

    # Barra de progreso
    progress_bar = ft.ProgressBar(width=500, value=0, visible=False)

    # Área de mensajes y progreso
    log_area = ft.Column(scroll=ft.ScrollMode.AUTO)

    # Función para actualizar la ruta del archivo al cargar un Excel
    def file_uploaded(e):
        nonlocal excel_file_path
        if e.files:
            excel_file_path = e.files[0].path
            log_area.controls.append(ft.Text(f"Archivo cargado: {e.files[0].name}"))
            page.update()

    # Función para seleccionar la ubicación y nombre del archivo donde se guardará el Excel
    def file_save(e):
        nonlocal save_file_path
        if e.path:
            save_file_path = e.path
            log_area.controls.append(ft.Text(f"Archivo de salida seleccionado: {save_file_path}"))
            page.update()

    # Botón para iniciar el procesamiento
    def start_processing(e):
        # Resetear barra de progreso y log
        progress_bar.value = 0
        progress_bar.visible = True
        log_area.controls.clear()
        page.update()

        # Validar que el usuario haya seleccionado una ubicación de guardado
        if save_file_path is None:
            log_area.controls.append(ft.Text("Por favor, selecciona un archivo para guardar la salida."))
            page.update()
            return

        # Procesar el archivo cargado y guardar el resultado en la ubicación seleccionada
        process_excel(
            excel_file_path,  # Usar la ruta del archivo subido
            url_column_input.value, 
            transcript_column_input.value,
            page,
            progress_bar,  # Pasar la barra de progreso
            log_area,      # Pasar el área de log para los mensajes
            save_file_path  # Ruta para guardar el nuevo archivo Excel
        )
        page.update()

    process_button = ft.ElevatedButton(
        text="Procesar Videos",
        icon=ft.icons.VIDEO_CALL,  # Ícono de video
        on_click=start_processing
    )

    # File picker para cargar archivo
    file_picker = ft.FilePicker(on_result=file_uploaded)

    # File picker para seleccionar el archivo donde guardar el Excel generado
    file_saver = ft.FilePicker(on_result=file_save)

    page.overlay.append(file_picker)
    page.overlay.append(file_saver)

    # Botón para abrir el file picker para cargar Excel
    upload_button = ft.ElevatedButton(
        text="Subir Excel",
        icon=ft.icons.UPLOAD_FILE,  # Ícono de subir archivo
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )

    # Botón para seleccionar el archivo de salida
    save_button = ft.ElevatedButton(
        text="Seleccionar archivo de salida",
        icon=ft.icons.SAVE,  # Ícono de guardar archivo
        on_click=lambda _: file_saver.save_file(file_name="transcripciones.xlsx")
    )

    # Colocar ambos botones en la misma fila (Row)
    button_row = ft.Row(
        controls=[upload_button, save_button, process_button],
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
