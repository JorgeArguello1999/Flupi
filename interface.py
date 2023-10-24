import pygame
import os

# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Visor de Galería")

# Directorio con las imágenes
image_directory = "./me"
image_files = os.listdir(image_directory)
current_image = 0

# Cargamos la primera imagen
current_image_surface = pygame.image.load(os.path.join(image_directory, image_files[current_image]))
current_image_rect = current_image_surface.get_rect()
current_image_rect.center = (screen_width // 2, screen_height // 2)

# Colores
white = (255, 255, 255)
font = pygame.font.Font(None, 36)

# Función para cargar la siguiente imagen
def load_next_image():
    global current_image
    current_image = (current_image + 1) % len(image_files)
    return pygame.image.load(os.path.join(image_directory, image_files[current_image]))

# Función para cargar la imagen anterior
def load_previous_image():
    global current_image
    current_image = (current_image - 1) % len(image_files)
    return pygame.image.load(os.path.join(image_directory, image_files[current_image]))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_image_surface = load_previous_image()
            elif event.key == pygame.K_RIGHT:
                current_image_surface = load_next_image()

    # Dibuja la imagen actual
    screen.fill(white)
    screen.blit(current_image_surface, current_image_rect)

    # Dibuja botones
    left_button = font.render("<", True, (0, 0, 0))
    right_button = font.render(">", True, (0, 0, 0))
    screen.blit(left_button, (50, screen_height // 2 - 20))
    screen.blit(right_button, (screen_width - 80, screen_height // 2 - 20))

    pygame.display.flip()

# Finaliza Pygame
pygame.quit()
