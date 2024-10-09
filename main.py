import flet as ft
from app.process_videos import process_excel

# Crear la interfaz gráfica
def main(page: ft.Page):
    page.title = "Transcriptor de Videos"
    page.window_width = 700
    page.window_height = 600

    # Inputs para subir Excel y configurar las columnas
    url_column_input = ft.TextField(label="Nombre de la columna de URLs", value="URL")
    transcript_column_input = ft.TextField(label="Nombre de la columna de transcripción", value="Transcripción")
    
    # Variables globales para almacenar la ruta del archivo Excel y el archivo de salida
    excel_file_path = None
    save_file_path = None  # Ruta para guardar el archivo de salida

    # Barra de progreso
    progress_bar = ft.ProgressBar(width=500, value=0, visible=False)

    # Mensaje de estado (inicialmente oculto)
    status_message = ft.Row(controls=[], visible=False)  # Se cambia a Row para añadir iconos y textos

    # Área de mensajes y progreso con estilo de TextField, con expand para ocupar el espacio disponible
    log_area = ft.Container(
        content=ft.Column(scroll=ft.ScrollMode.AUTO),
        padding=ft.padding.all(10),
        expand=True,  # Para que el área de log ocupe el espacio disponible
        width=page.window_width,
        border_radius=ft.border_radius.all(10),
        bgcolor=ft.colors.GREY_100,  # Color de fondo similar a un TextField
        border=ft.border.all(1, ft.colors.GREY)  # Bordes para diferenciarlo
    )

    # Botones
    upload_button = ft.ElevatedButton(
        text="Subir Excel",
        icon=ft.icons.UPLOAD_FILE,  # Ícono de subir archivo
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )

    save_button = ft.ElevatedButton(
        text="Seleccionar archivo de salida",
        icon=ft.icons.SAVE,  # Ícono de guardar archivo
        disabled=True,  # Inicialmente desactivado
        on_click=lambda _: file_saver.save_file(file_name="transcripciones.xlsx")
    )

    process_button = ft.ElevatedButton(
        text="Procesar Videos",
        icon=ft.icons.VIDEO_CALL,  # Ícono de video
        disabled=True,  # Inicialmente desactivado
        on_click=lambda e: start_processing()
    )

    # Función para actualizar la ruta del archivo al cargar un Excel
    def file_uploaded(e):
        nonlocal excel_file_path
        if e.files:
            excel_file_path = e.files[0].path
            log_area.content.controls.append(ft.Text(f"Archivo cargado: {e.files[0].name}"))
            page.update()

            # Habilitar el botón para seleccionar archivo de salida
            save_button.disabled = False
            page.update()

    # Función para seleccionar la ubicación y nombre del archivo donde se guardará el Excel
    def file_save(e):
        nonlocal save_file_path
        if e.path:
            save_file_path = e.path
            log_area.content.controls.append(ft.Text(f"Archivo de salida seleccionado: {save_file_path}"))
            page.update()

            # Habilitar el botón para procesar videos
            process_button.disabled = False
            page.update()

    # Botón para iniciar el procesamiento
    def start_processing():
        # Resetear barra de progreso, mensaje de estado y log
        progress_bar.value = 0
        progress_bar.visible = True
        status_message.controls.clear()
        status_message.controls.append(ft.Text("Descargando y transcribiendo... Esto tomará un tiempo."))
        status_message.visible = True
        log_area.content.controls.clear()
        page.update()

        # Desactivar todos los botones durante el procesamiento
        upload_button.disabled = True
        save_button.disabled = True
        process_button.disabled = True
        page.update()

        # Procesar el archivo cargado y guardar el resultado en la ubicación seleccionada
        process_excel(
            excel_file_path,  # Usar la ruta del archivo subido
            url_column_input.value, 
            transcript_column_input.value,
            page,
            progress_bar,  # Pasar la barra de progreso
            log_area.content,  # Pasar el área de log para los mensajes
            save_file_path  # Ruta para guardar el nuevo archivo Excel
        )

        # Cambiar el mensaje de estado una vez completado con ícono y salto de línea
        status_message.controls.clear()  # Limpiar controles previos
        status_message.controls.append(
            ft.Icon(name=ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN)  # Añadir icono
        )
        status_message.controls.append(
            ft.Text(f"Archivo Excel guardado en:\n{save_file_path}", color=ft.colors.GREEN)  # Añadir texto
        )
        status_message.visible = True
        page.update()

        # Rehabilitar los botones después de que el proceso haya terminado
        upload_button.disabled = False
        save_button.disabled = False
        process_button.disabled = False
        page.update()

    # File picker para cargar archivo
    file_picker = ft.FilePicker(on_result=file_uploaded)

    # File picker para seleccionar el archivo donde guardar el Excel generado
    file_saver = ft.FilePicker(on_result=file_save)

    page.overlay.append(file_picker)
    page.overlay.append(file_saver)

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
        status_message,  # Mensaje de estado con ícono y texto
        progress_bar,    # Barra de progreso
        log_area         # Área de mensajes con estilo de TextField y expand para ocupar el espacio
    )

ft.app(target=main)