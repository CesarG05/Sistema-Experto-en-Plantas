import customtkinter as ctk  # Importa la biblioteca CustomTkinter
from tkinter import filedialog, messagebox  # Para seleccionar archivos
from PIL import Image # Usamos Pillow para manejar las imágenes
from customtkinter import CTkImage
import pandas as pd

# Archivos de Base de Hechos y Explicaciones
ruta_archivo_plantas = 'Base de Hechos/Base_Hechos_Plantas.csv'   # Ruta del archivo de plantas
ruta_archivo_explicaciones = 'Base de Hechos/Base_Hechos_Explicaciones.csv'  # Ruta del archivo de explicaciones

# Colores y Tipo de letra
color_primario = "white"
color_verde_claro = "#78c03f"
tipo_letra = "Comic Sans MS"

# Crear la ventana principal
ventana = ctk.CTk(fg_color=color_primario)  # Se crea una instancia de la ventana principal usando CustomTkinter
ventana.title("Sistema Experto - Identificación de Plantas")

# Definir el tamaño de la ventana
ancho_ventana = 1300
alto_ventana = 900

# Centrar ventana en pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
x = (ancho_pantalla // 2) - (ancho_ventana // 2)
y = (alto_pantalla // 2) - (alto_ventana // 2)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
ctk.set_appearance_mode("light")

# Crear los dos frames (principal y estático)
frame_principal = ctk.CTkFrame(ventana, height=alto_ventana, fg_color="transparent")
frame_estatico = ctk.CTkFrame(ventana, width=300, height=alto_ventana, fg_color="transparent")
#frame_principal.pack_propagate(False)
frame_estatico.pack_propagate(False)
frame_principal.pack(side="left", fill="both", expand=True)
frame_estatico.pack(side="right", fill="y")


# Función para cargar los archivos de la base de hechos (archivos CSV)
def cargar_datos_csv(ruta_archivo):
    return pd.read_csv(ruta_archivo)


# Función para obtener el nombre de la planta basado en las características
def obtener_planta(forma_hoja, color_hoja, color_flor, textura_hoja, frutos):
    # Cargar el CSV
    df = cargar_datos_csv(ruta_archivo_plantas)

    # Filtrar los datos según las características
    planta = df[(df['Forma Hoja'] == forma_hoja) &
                (df['Color Hoja'] == color_hoja) &
                (df['Color Flor'] == color_flor) &
                (df['Textura Hoja'] == textura_hoja) &
                (df['Frutos'] == frutos)]

    # Verificar si se encontró una planta y si el nombre de la planta no es nulo o vacío
    if not planta.empty:
        nombre_planta = planta['Planta'].values[0]
        if pd.isna(nombre_planta) or nombre_planta == '' or nombre_planta.lower() == 'null':
            return "No hay planta asignada para estas características"
        else:
            return nombre_planta
    else:
        return "Planta no encontrada"


# Función para obtener la explicación de la planta basado en su nombre
def obtener_explicacion_planta(nombre_planta):
    # Cargar el archivo CSV con las explicaciones de las plantas
    df_explicaciones = cargar_datos_csv(ruta_archivo_explicaciones)

    # Buscar la planta en el archivo de explicaciones
    fila_explicacion = df_explicaciones[df_explicaciones['Planta'] == nombre_planta]

    # Verificar si se encontró la explicación
    if not fila_explicacion.empty:
        explicacion = fila_explicacion['Explicacion'].values[0]
        return explicacion
    else:
        return "Descripción no encontrada para esta planta."


# Función que ejecuta frame_respuesta despues de obtener la la planta
def analizar_respuetas(forma_hoja, color_hoja, color_flor, textura_hoja, frutos):
    # Obtiene el nombre de la plnanta
    nombre_planta = obtener_planta(forma_hoja, color_hoja, color_flor, textura_hoja, frutos)
    # Ejecuta el frame respuesta
    frame_respuesta(nombre_planta, forma_hoja, color_hoja, color_flor, textura_hoja, frutos)


# Funcion para agregar conocimiento
def guardar_respuestas(planta, explicacion, forma_hoja, color_hoja, color_flor, textura_hoja, frutos):
    # Cargar el CSV de plantas
    df_plantas = pd.read_csv(ruta_archivo_plantas)  # Suponiendo que tienes esta función

    # Filtrar los datos según las características
    fila_planta = df_plantas[(df_plantas['Forma Hoja'] == forma_hoja) &
                             (df_plantas['Color Hoja'] == color_hoja) &
                             (df_plantas['Color Flor'] == color_flor) &
                             (df_plantas['Textura Hoja'] == textura_hoja) &
                             (df_plantas['Frutos'] == frutos)].copy()

    # Verificar si se encontró alguna fila que coincida
    if not fila_planta.empty:
        # Agregar el nombre de la planta a la columna correspondiente
        fila_planta['Planta'] = planta

        # Actualizar el DataFrame original con la nueva columna
        df_plantas.update(fila_planta)

    # Guardar los cambios en el archivo (sobrescribir)
    df_plantas.to_csv(ruta_archivo_plantas, index=False)

    # Cargar el CSV de explicaciones
    df_explicaciones = cargar_datos_csv(ruta_archivo_explicaciones)

    # Crear la nueva fila
    nueva_explicacion = [planta, explicacion]

    # Agregar la nueva fila al DataFrame
    df_explicaciones.loc[len(df_explicaciones)] = nueva_explicacion

    # Guardar el archivo CSV con la nueva fila
    df_explicaciones.to_csv(ruta_archivo_explicaciones, index=False)

    messagebox.showwarning("Mensaje", "Guardado Exitoso.")
    frame_colsultas()


# Función para cargar y mostrar la imágen
def subir_Imagen():
    # Abrir un cuadro de diálogo para seleccionar el archivo de imagen
    archivo_imagen = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])

    if archivo_imagen:
        # Redimensionar la imagen
        imagen_redimensionada = redimensionar_imagen(archivo_imagen, 350, 250)

        # Actualizar la etiqueta de la imagen
        etiqueta_imagen.configure(image=imagen_redimensionada, text="")  # Eliminamos el texto al mostrar la imagen
        etiqueta_imagen.image = imagen_redimensionada  # Necesario para evitar que la imagen se borre


# Función para redimensionar imágenes
def redimensionar_imagen(ruta_imagen, ancho, alto):
    imagen_original = Image.open(ruta_imagen)
    return CTkImage(light_image=imagen_original, size=(ancho, alto))


# Frame para relizar consultas
def frame_colsultas():
    # Limpiar el frame existente
    for widget in frame_principal.winfo_children():
        widget.destroy()

    frame_principal.configure(fg_color="transparent")

    def frame_cargaImagen():
        # Frame principal para cargar la imagen
        frame_imagen = ctk.CTkFrame(frame_principal, width=1000, height=300)
        frame_imagen.pack_propagate(False)
        frame_imagen.pack(side="top", fill="x", padx=10, pady=(10, 5))

        # Subframe izquierdo (para título y botón)
        frame_izquierdo = ctk.CTkFrame(frame_imagen, fg_color="transparent")
        frame_izquierdo.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        etiqueta_titulo = ctk.CTkLabel(frame_izquierdo, text="Inserte la imagen su planta", font=(tipo_letra, 22, "bold"))
        etiqueta_titulo.pack(side="top", pady=(10, 5), anchor="center")

        boton_cargar_imagen = ctk.CTkButton(frame_izquierdo, text="Subir Imagen",font=(tipo_letra, 18), height=40, width=200, command=lambda: subir_Imagen())
        boton_cargar_imagen.pack(side="top", pady=(80, 10), anchor="center")

        # Subframe derecho (para la etiqueta de imagen)
        frame_derecho = ctk.CTkFrame(frame_imagen, fg_color=color_verde_claro)
        frame_derecho.pack(side="right", fill="both", expand=True, padx=20, pady=10)

        global etiqueta_imagen  # Definir la etiqueta de imagen globalmente
        etiqueta_imagen = ctk.CTkLabel(frame_derecho, text="Ninguna imagen seleccionada", font=(tipo_letra, 18), width=350, height=250)
        etiqueta_imagen.pack(expand=True, anchor="center")

    def frame_preguntas():
        # Frame principal para describir la planta
        frame_descripcion = ctk.CTkFrame(frame_principal, width=1000, height=580, fg_color=color_verde_claro)
        frame_descripcion.pack_propagate(False)
        frame_descripcion.pack(side="bottom", fill="x", padx=10, pady=(5, 10))

        # Titulo Frame Descripcion
        etiqueta_titulo2 = ctk.CTkLabel(frame_descripcion, text="Describa su Planta", font=(tipo_letra, 22, "bold"))
        etiqueta_titulo2.pack(side="top", pady=(10, 5), anchor="center")

        # Subframe izquierdo (para preguntas)
        frame_preg = ctk.CTkFrame(frame_descripcion, fg_color="transparent")
        frame_preg.pack(side="left", fill="both", expand=True)

        # Subframe derecho (para imagenes de referencia)
        frame_img = ctk.CTkFrame(frame_descripcion, fg_color="transparent")
        frame_img.pack(side="right", fill="both", expand=True)

        # Pregunta 1
        pregunta1 = ctk.CTkLabel(frame_preg, text="1. ¿Cuál es la forma de las hojas?", font=(tipo_letra, 20), text_color="black")
        pregunta1.pack(pady=(20,0))
        respuestas1 = ctk.CTkComboBox(frame_preg, values=["ovaladas", "lanceoladas", "corazonadas", "alargadas y estrecha"], state="readonly", width=200)
        respuestas1.pack(pady=(0,30))

        # Imagen Forma Hojas
        imagen_redimensionada = redimensionar_imagen("img/Formas_Hoja.png", 400, 80)
        hoja_formas = ctk.CTkLabel(frame_img, image=imagen_redimensionada, text="")
        hoja_formas.pack(pady=(10,0))

        # Pregunta 2
        pregunta2 = ctk.CTkLabel(frame_preg, text="2. ¿Cuál es el color de sus hojas?", font=(tipo_letra, 20), text_color="black")
        pregunta2.pack()
        respuestas2 = ctk.CTkComboBox(frame_preg, values=["verde oscuro", "verde claro", "amarillento"], state="readonly", width=200)
        respuestas2.pack(pady=(0,30))

        # Imagen Color Hoja
        imagen_redimensionada = redimensionar_imagen("img/Colores_Hoja.png", 400, 80)
        hoja_color = ctk.CTkLabel(frame_img, image=imagen_redimensionada, text="")
        hoja_color.pack(pady=(5,0))

        # Pregunta 3
        pregunta3 = ctk.CTkLabel(frame_preg, text="3. Cantidad de colores en las flores de la planta", font=(tipo_letra, 20), text_color="black")
        pregunta3.pack()
        respuestas3 = ctk.CTkComboBox(frame_preg, values=["un solo color", "colores variantes", "sin flores visibles"], state="readonly", width=200)
        respuestas3.pack(pady=(0,30))

        # Imagen Color Flores
        imagen_redimensionada = redimensionar_imagen("img/Colores_Flor.png", 400, 80)
        flores = ctk.CTkLabel(frame_img, image=imagen_redimensionada, text="")
        flores.pack(pady=(5,0))

        # Pregunta 4
        pregunta4 = ctk.CTkLabel(frame_preg, text="4. ¿Cuál es la textura de las hojas?", font=(tipo_letra, 20), text_color="black")
        pregunta4.pack()
        respuestas4 = ctk.CTkComboBox(frame_preg, values=["lisa", "rugosa", "vellosa", "espinosa"], state="readonly", width=200)
        respuestas4.pack(pady=(0,30))

        # Imagen Textura Hoja
        imagen_redimensionada = redimensionar_imagen("img/Texturas_Hoja.png", 400, 80)
        hoja_textura = ctk.CTkLabel(frame_img, image=imagen_redimensionada, text="")
        hoja_textura.pack(pady=(5,0))

        # Pregunta 5
        pregunta5 = ctk.CTkLabel(frame_preg, text="5. ¿La planta tiene frutos visibles o no?", font=(tipo_letra, 20), text_color="black")
        pregunta5.pack()
        respuestas5 = ctk.CTkComboBox(frame_preg, values=["frutos visibles", "frutos no visibles"], state="readonly", width=200)
        respuestas5.pack(pady=(0,30))

        # Imagen Frutos
        imagen_redimensionada = redimensionar_imagen("img/Frutos.png", 400, 80)
        frutos_img = ctk.CTkLabel(frame_img, image=imagen_redimensionada, text="")
        frutos_img.pack(pady=(5,0))

        def obtener_respuestas():
            # Obtener las respuestas de los ComboBox
            forma_hoja = respuestas1.get()
            color_hoja = respuestas2.get()
            color_flor= respuestas3.get()
            textura_hoja = respuestas4.get()
            frutos = respuestas5.get()

            # Validar si alguna de las respuestas está vacía
            if not forma_hoja or not color_hoja or not color_flor or not textura_hoja or not frutos:
                # Si alguna respuesta está vacía, mostrar un mensaje de advertencia
                messagebox.showwarning("Advertencia", "Por favor, seleccione una opción en todas las preguntas.")
            else:
                analizar_respuetas(forma_hoja, color_hoja, color_flor, textura_hoja, frutos)

        # Botón analizar
        boton_analizar = ctk.CTkButton(frame_preg, text="Analizar", font=(tipo_letra, 18), height=40, width=200, command=lambda: obtener_respuestas())
        boton_analizar.pack(side="bottom", pady=(0,20))

    frame_cargaImagen()
    frame_preguntas()


# Función agregar componentes del frame estático
def componentes_estatica():
    # Redimensionar la imagen
    imagen_redimensionada = redimensionar_imagen("img/Jardinero.png", 400, 700)
    # Crear un Label y asignar la imagen
    imagen_animada = ctk.CTkLabel(frame_estatico, image=imagen_redimensionada, text="")
    imagen_animada.pack(side="bottom")

    nombre_SE = ctk.CTkLabel(frame_estatico, text="Experto\n en \nPlantas", font=(tipo_letra, 40, "bold"),justify="center", text_color=color_verde_claro)
    nombre_SE.pack(side="top", pady=(40, 0))

# Función para visualizar el frame respuesta
def frame_respuesta(planta, forma_hoja, color_hoja, color_flor, textura_hoja, frutos):
    # Limpiar el frame existente
    for widget in frame_principal.winfo_children():
        widget.destroy()

    frame_principal.configure(fg_color=color_verde_claro)

    label_titulo= ctk.CTkLabel(frame_principal, text="LA PLANTA ES:", font=(tipo_letra, 30))
    label_titulo.pack(pady=(40,20))

    label_respuesta_planta = ctk.CTkLabel(frame_principal, text=planta, font=(tipo_letra, 40, "bold"), wraplength=900)
    label_respuesta_planta.pack(pady=(0,40))

    # Subframe botones
    frame_btn = ctk.CTkFrame(frame_principal, fg_color="transparent", height=180, width=1000)
    frame_btn.pack(side="bottom")
    frame_btn.pack_propagate(False)

    boton_consulta = ctk.CTkButton(frame_btn, text="Nueva consulta", font=(tipo_letra, 18), height=40, width=200, command=lambda: frame_colsultas())
    boton_consulta.pack(side="right", padx=100)


    if planta != "Planta no encontrada" and planta != "No hay planta asignada para estas características":
        frame_expli = ctk.CTkFrame(frame_principal, fg_color="transparent")
        boton_explicacion = ctk.CTkButton(frame_btn,text="Explicación", font=(tipo_letra, 18), height=40, width=200, command=lambda: mostrar_explicacion(planta))
        boton_explicacion.pack(side="left", padx=100)
    else :
        boton_agregar = ctk.CTkButton(frame_btn, text="Agregar Conocimiento", font=(tipo_letra, 18), height=40, width=200, command=lambda: frame_experto(forma_hoja, color_hoja, color_flor, textura_hoja, frutos))
        boton_agregar.pack(side="left", padx=100)

    def mostrar_explicacion(nombre_planta):
        # Obtiene la explicacion de la plnanta
        explicacion = obtener_explicacion_planta(nombre_planta)

        for widget in frame_expli.winfo_children():
            widget.destroy()

        frame_expli.pack()

        titulo_exp = ctk.CTkLabel(frame_expli, text="-- EXPLICACIÓN --", font=(tipo_letra, 30))
        titulo_exp.pack(pady=(0, 20))

        explicacion_planta = ctk.CTkLabel(frame_expli, text=explicacion, font=(tipo_letra, 30, "bold"), wraplength=600)
        explicacion_planta.pack(pady=(0, 20))


# Función para visualizar el frame experto
def frame_experto(forma_hoja, color_hoja, color_flor, textura_hoja, frutos):
    # Limpiar el frame existente
    for widget in frame_principal.winfo_children():
        widget.destroy()

    frame_principal.configure(fg_color=color_verde_claro)

    respuestas_seleccionadas = (
        f"Forma de Hojas:  {forma_hoja} "
        f"\nColor de Hojas:  {color_hoja} "
        f"\nColor de Flores:  {color_flor} "
        f"\nTextura de Hojas:  {textura_hoja} "
        f"\nFrutos:  {frutos}"
    )

    titulo_resp = ctk.CTkLabel(frame_principal, text="-- Características de la Planta Descrita --", font=(tipo_letra, 22, "bold"))
    titulo_resp.pack(pady=(40,10))
    frame_resp= ctk.CTkFrame(frame_principal, fg_color="white")
    frame_resp.pack()
    etiqueta_respuestas = ctk.CTkLabel(frame_resp, text=respuestas_seleccionadas, font=(tipo_letra, 20))
    etiqueta_respuestas.pack(pady=15, padx=30)

    titulo_planta = ctk.CTkLabel(frame_principal, text="-- Nombre de la Planta --", font=(tipo_letra, 22, "bold"))
    titulo_planta.pack(pady=(50,10))
    nombre_planta = ctk.CTkEntry(frame_principal, placeholder_text="Escribe aquí el nombre de la planta...", font=(tipo_letra, 15), width=400, height=40)
    nombre_planta.pack(pady=10)

    titulo_exp = ctk.CTkLabel(frame_principal, text="-- Explicación de la Planta --", font=(tipo_letra, 22, "bold"))
    titulo_exp.pack(pady=(50,10))
    explicacion_planta = ctk.CTkTextbox(frame_principal, font=(tipo_letra, 15),width=600, height=150)
    explicacion_planta.pack(pady=10)

    # Subframe botones
    frame_btn = ctk.CTkFrame(frame_principal, fg_color="transparent", height=180, width=1000)
    frame_btn.pack(side="bottom")
    frame_btn.pack_propagate(False)

    boton_guardar = ctk.CTkButton(frame_btn, text="Guardar", font=(tipo_letra, 18), height=40, width=200, command=lambda: obtener_respuesta())
    boton_guardar.pack(side="right", padx=100)

    boton_colsulta = ctk.CTkButton(frame_btn, text="Regresar a consultar", font=(tipo_letra, 18), height=40, width=200, command=lambda: confirmar_accion())
    boton_colsulta.pack(side="left", padx=100)

    def obtener_respuesta():
        # Para obtener las respuestas ingresadas:
        planta = nombre_planta.get()
        explicacion = explicacion_planta.get("1.0", "end")

        # Validar si alguna de las respuestas está vacía
        if not planta or not explicacion.strip():
            # Si alguna respuesta está vacía, mostrar un mensaje de advertencia
            messagebox.showwarning("Advertencia", "Por favor, llene todos los campos.")
        else:
            guardar_respuestas(planta, explicacion, forma_hoja, color_hoja, color_flor, textura_hoja, frutos)

    def confirmar_accion():
        respuesta = messagebox.askyesno("Confirmación", "Si regresa la operación se canselará.\n¿Está seguro de regresar?")
        if respuesta:
            frame_colsultas()


# Llamado de frames
frame_colsultas()
componentes_estatica()

ventana.mainloop()