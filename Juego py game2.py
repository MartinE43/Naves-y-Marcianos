import pygame
import random

# Inicializar PyGame
pygame.init()

# Configuraciones de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Naves y Marcianos")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# FPS y reloj
FPS = 60
clock = pygame.time.Clock()

# Cargar imágenes RECORDAR GUARDAR LAS IMAGENES CON LAS MISMAS EXTENSIONES Y NOMBRES EN EL ERCHIVO DE MAIN

nave_img = pygame.image.load("nave.png")
marciano_img = pygame.image.load("marciano.png")
galaxia_img = pygame.image.load("galaxia.jpg")

# Escalar imágenes al tamaño adecuado
nave_img = pygame.transform.scale(nave_img, (50, 50))
marciano_img = pygame.transform.scale(marciano_img, (50, 50))
galaxia_img = pygame.transform.scale(galaxia_img, (WIDTH, HEIGHT))

# Puntuación y niveles
score = 0
level = 1

# Función para el menú principal
def main_menu():
    run = True
    while run:
        screen.blit(galaxia_img, (0, 0))  # Fondo de galaxia
        font = pygame.font.SysFont('Arial', 36)
        title_text = font.render("Naves y Marcianos", True, WHITE)
        start_text = font.render("Presiona cualquier tecla para comenzar", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                game_loop()
    
    pygame.quit()

# Función para el loop del juego principal
def game_loop():
    global score, level
    run = True
    player = pygame.Rect(WIDTH // 2, HEIGHT - 60, 50, 50)
    player_speed = 5
    enemies = [create_enemy() for _ in range(5)]
    bullets = []
    enemy_speed = 3

    while run:
        screen.blit(galaxia_img, (0, 0))  # Fondo de galaxia

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(create_bullet(player.x + 20, player.y))  # Disparo desde el centro de la nave

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - 50:
            player.x += player_speed
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.y < HEIGHT - 50:
            player.y += player_speed

        # Dibujar jugador (nave)
        screen.blit(nave_img, (player.x, player.y))

        # Mover y dibujar enemigos (marcianos)
        for enemy in enemies:
            move_enemy(enemy, enemy_speed)
            screen.blit(marciano_img, (enemy.x, enemy.y))

            # Verificar colisiones entre el jugador y los enemigos
            if player.colliderect(enemy):
                game_over()

        # Mover y dibujar balas
        for bullet in bullets[:]:
            bullet.y -= 10
            if bullet.y < 0:
                bullets.remove(bullet)
            pygame.draw.rect(screen, WHITE, bullet)

            # Verificar si una bala colisiona con un enemigo
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 10

        # Crear nuevos enemigos si son destruidos
        if len(enemies) == 0:
            level += 1
            enemy_speed += 1  # Aumenta la velocidad de los enemigos con el nivel
            enemies = [create_enemy() for _ in range(5 + level)]  # Más enemigos por nivel

        # Mostrar puntuación y nivel
        show_score_level()

        pygame.display.update()
        clock.tick(FPS)

# Función para crear enemigos (marcianos)
def create_enemy():
    x = random.randint(0, WIDTH - 50)
    y = random.randint(-100, -50)  # Aparecen fuera de la pantalla
    return pygame.Rect(x, y, 50, 50)

# Función para mover enemigos
def move_enemy(enemy, speed):
    enemy.y += speed
    if enemy.y > HEIGHT:
        enemy.y = random.randint(-100, -50)
        enemy.x = random.randint(0, WIDTH - 50)

# Función para crear una bala
def create_bullet(x, y):
    return pygame.Rect(x, y, 10, 20)

# Mostrar la puntuación y el nivel en la pantalla
def show_score_level():
    font = pygame.font.SysFont('Arial', 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

# Función para mostrar la pantalla de Game Over
def game_over():
    font = pygame.font.SysFont('Arial', 36)
    game_over_text = font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)
    main_menu()

# Iniciar el juego desde el menú principal
main_menu()
