import pygame
import os

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Carrousel de Imágenes")

# Directorio con las imágenes
image_directory = "./me/"

# Obtener una lista de las imágenes en el directorio
image_files = [f for f in os.listdir(image_directory) if f.endswith(".jpeg")]
image_index = 0  
print(image_files)

# Cargar imágenes
images = [pygame.image.load(os.path.join(image_directory, file)) for file in image_files]

# Colores
yellow = (255, 255, 0)
black = (000, 000, 000)

# Fuente para los botones
font = pygame.font.Font(None, 36)

# Función para dibujar botones redondos
def draw_round_button(x, y, radius, text, color):
    pygame.draw.circle(screen, yellow, (x, y), radius)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                image_index = (image_index - 1) % len(images)
            elif event.key == pygame.K_RIGHT:
                image_index = (image_index + 1) % len(images)

    # Dibujar elementos en la pantalla
    screen.fill(yellow)  # Fondo amarillo
    current_image = images[image_index]
    screen.blit(current_image, (0, 0))

    # Dibujar botones redondos
    draw_round_button(50, 300, 30, "<", black)
    draw_round_button(750, 300, 30, ">", black)

    pygame.display.flip()

# Finalizar Pygame
pygame.quit()