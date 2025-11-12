import pygame


import sys
import os
from Compilador import analizador_lexico, analizador_sintactico, generador_codigo

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 1024, 720
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Compilador de Cuentos")

# Verifica si la imagen existe y carga la imagen de fondo
imagen_path = 'logocompy.png'
if not os.path.isfile(imagen_path):
    print(f"Error: La imagen {imagen_path} no existe.")
else:
    fondo = pygame.image.load(imagen_path)  # Cargar la imagen de fondo
    # Calcular las coordenadas para centrar la imagen
    fondo_rect = fondo.get_rect(center=(ANCHO//2, ALTO//2))

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (50, 50, 50)
AZUL_ELEGANTE = (30, 144, 255)  # Cambiado a celeste
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Fuente
fuente = pygame.font.Font(None, 24)

# Variables
codigo_fuente = ""
lineas_codigo = []
mensaje = ""

# Botones
boton_ejecutar = pygame.Rect(800, 650, 140, 40)
boton_salir = pygame.Rect(650, 650, 140, 40)

# Área de resultado y variables de scroll
area_resultado = pygame.Rect(10, 400, 1004, 240)
scroll_pos = 0
scroll_speed = 1  # Velocidad de scroll ajustada para las flechas del teclado

# Bucle principal
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                lineas_codigo.append(codigo_fuente)
                codigo_fuente = ""
            elif evento.key == pygame.K_BACKSPACE:
                codigo_fuente = codigo_fuente[:-1]
            elif evento.key == pygame.K_UP:
                scroll_pos = max(0, scroll_pos - scroll_speed)
            elif evento.key == pygame.K_DOWN:
                scroll_pos = min(len(lineas_codigo) - 1, scroll_pos + scroll_speed)
            else:
                codigo_fuente += evento.unicode
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_ejecutar.collidepoint(evento.pos):
                try:
                    codigo = "\n".join(lineas_codigo)
                    tokens = analizador_lexico(codigo)
                    arbol, variables = analizador_sintactico(tokens)
                    codigo_ejecutable = generador_codigo(arbol, variables)
                    # Convertir lista de líneas en un solo string con saltos de línea
                    mensaje = "\n".join(codigo_ejecutable)
                    # Actualizar lineas_mensaje para mostrar correctamente en el área de resultado
                    lineas_mensaje = mensaje.splitlines()
                    scroll_pos = 0  # Reiniciar la posición de scroll al ejecutar
                except Exception as e:
                    mensaje = str(e)
            elif boton_salir.collidepoint(evento.pos):
                ejecutando = False

    # Dibujar en pantalla
    ventana.fill(BLANCO)  # Llena la pantalla con color blanco antes de dibujar el fondo
    if 'fondo' in locals():
        ventana.blit(fondo, fondo_rect.topleft)  # Dibujar la imagen de fondo centrada

    # Renderizar líneas de código
    y = 10
    for linea in lineas_codigo:
        texto = fuente.render(linea, True, NEGRO)
        ventana.blit(texto, (10, y))
        y += 30

    # Renderizar código en proceso de escritura
    texto = fuente.render(codigo_fuente, True, NEGRO)
    ventana.blit(texto, (10, y))

    # Dibujar botón ejecutar
    pygame.draw.rect(ventana, AZUL_ELEGANTE, boton_ejecutar)
    texto_boton_ejecutar = fuente.render("Ejecutar", True, BLANCO)
    ventana.blit(texto_boton_ejecutar, (boton_ejecutar.x + 20, boton_ejecutar.y + 10))

    # Dibujar botón salir
    pygame.draw.rect(ventana, ROJO, boton_salir)
    texto_boton_salir = fuente.render("Salir", True, BLANCO)
    ventana.blit(texto_boton_salir, (boton_salir.x + 50, boton_salir.y + 10))

    # Dibujar área de resultado
    pygame.draw.rect(ventana, GRIS_OSCURO, area_resultado)

    # Mostrar mensaje en el área de resultado
    if mensaje:
        # Dividir el mensaje en líneas para renderizar cada una con un salto de línea
        lineas_mensaje = mensaje.splitlines()
        visible_lines = int(area_resultado.height / 24)  # Calcular cuántas líneas caben en el área
        start_line = max(0, len(lineas_mensaje) - visible_lines)  # Determinar la primera línea visible
        y = area_resultado.y + 20

        for linea in lineas_mensaje[start_line:]:
            if y < area_resultado.y + area_resultado.height:
                texto_mensaje = fuente.render(linea, True, BLANCO)
                ventana.blit(texto_mensaje, (area_resultado.x + 20, y))
                y += 24  # Espaciado entre líneas

    # Control de scroll
    if mensaje and len(lineas_mensaje) > visible_lines:
        # Dibujar la barra de scroll en celeste
        barra_scroll_height = visible_lines * area_resultado.height // len(lineas_mensaje)
        barra_scroll_y = area_resultado.y + scroll_pos * (area_resultado.height - barra_scroll_height) // (len(lineas_mensaje) - visible_lines)
        pygame.draw.rect(ventana, AZUL_ELEGANTE, (area_resultado.x + area_resultado.width - 10, area_resultado.y,
                                               10, area_resultado.height))
        pygame.draw.rect(ventana, AZUL_ELEGANTE, (area_resultado.x + area_resultado.width - 10, barra_scroll_y,
                                               10, barra_scroll_height))

    pygame.display.flip()

pygame.quit()
sys.exit()
