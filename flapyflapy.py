import pygame
import random
import logging

# Configuração do logging
logging.basicConfig(filename='game_errors.log', level=logging.ERROR)

# Inicializa o Pygame
pygame.init()
pygame.mixer.init()  # Inicializa o mixer para reprodução de áudio

# Configurações da tela
WIDTH, HEIGHT = 1024, 768  # Aumentando a resolução
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bolsonaro vs Canos Lula")

# Cores
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)

# Dimensões do jogador
bird_x, bird_y = 50, HEIGHT // 2
bird_y_change = 0
gravity = 0.5  # Adiciona um valor de gravidade
difficulty = "fácil"

# Função para desenhar o personagem principal (círculo com boné)
def draw_bolsonaro(x, y):
    pygame.draw.circle(screen, (0, 0, 255), (x + 25, y + 25), 25)  # Círculo azul
    pygame.draw.rect(screen, (0, 0, 0), (x + 10, y - 10, 30, 10))  # Boné

# Função para desenhar os canos (Lula)
def draw_pipes(pipe_x, pipe_height, gap):
    pygame.draw.rect(screen, ORANGE, (pipe_x, 0, 70, pipe_height))  # Cano superior
    pygame.draw.rect(screen, ORANGE, (pipe_x, pipe_height + gap, 70, HEIGHT))  # Cano inferior

# Função para exibir a logo
def show_logo():
    font = pygame.font.SysFont(None, 75)
    screen.fill(BLACK)
    logo_text = font.render("MAGOFITNESS GAMING", True, WHITE)
    screen.blit(logo_text, (WIDTH // 2 - logo_text.get_width() // 2, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(2000)  # Espera 2 segundos

# Função para exibir a mensagem de desenvolvedor
def show_developer_info():
    font = pygame.font.SysFont(None, 50)
    screen.fill(BLACK)
    info_text = font.render("Desenvolvido por Victor Bruno da Fonseca Muniz", True, WHITE)
    screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Espera 2 segundos

# Função para exibir o menu
def show_menu():
    global difficulty
    font = pygame.font.SysFont(None, 55)
    
    while True:
        screen.fill(BLACK)
        menu_font = pygame.font.SysFont(None, 50)

        new_game_text = menu_font.render("1. Novo Jogo", True, WHITE)
        continue_text = menu_font.render("2. Continuar", True, WHITE)
        difficulty_text = menu_font.render(f"3. Dificuldade: {difficulty.capitalize()}", True, WHITE)
        quit_text = menu_font.render("4. Sair", True, WHITE)

        screen.blit(new_game_text, (WIDTH // 2 - new_game_text.get_width() // 2, HEIGHT // 4))
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 4 + 50))
        screen.blit(difficulty_text, (WIDTH // 2 - difficulty_text.get_width() // 2, HEIGHT // 4 + 100))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 4 + 150))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "novo"
                elif event.key == pygame.K_2:
                    return "continuar"
                elif event.key == pygame.K_3:
                    change_difficulty()
                elif event.key == pygame.K_4:
                    pygame.quit()
                    exit()

# Função para mudar a dificuldade
def change_difficulty():
    global difficulty
    difficulties = ["fácil", "médio", "difícil"]
    current_index = difficulties.index(difficulty)
    current_index = (current_index + 1) % len(difficulties)
    difficulty = difficulties[current_index]

# Função principal do jogo
def game_loop():
    global bird_y, bird_y_change
    clock = pygame.time.Clock()
    score = 0

    # Posição dos canos
    pipe_x = WIDTH
    pipe_height = random.randint(150, 400)
    pipe_gap = 150
    pipe_speed = 3

    # Ajuste de dificuldade
    if difficulty == "fácil":
        pipe_speed = 3
    elif difficulty == "médio":
        pipe_speed = 5
    elif difficulty == "difícil":
        pipe_speed = 7

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_change = -8  # Pulo

        bird_y_change += gravity
        bird_y += bird_y_change

        if bird_y < 0:
            bird_y = 0
        if bird_y > HEIGHT - 50:  # Considerando altura do círculo
            bird_y = HEIGHT - 50

        # Movimenta os canos (Lula)
        pipe_x -= pipe_speed
        if pipe_x < -70:  # Largura do cano
            pipe_x = WIDTH
            pipe_height = random.randint(150, 400)
            score += 1

        # Desenhar personagem e canos
        draw_bolsonaro(bird_x, bird_y)
        draw_pipes(pipe_x, pipe_height, pipe_gap)

        # Verifica colisão
        if (bird_x + 50 > pipe_x and bird_x < pipe_x + 70):
            if bird_y < pipe_height or bird_y + 50 > pipe_height + pipe_gap:
                running = False  # Colisão com cano (fim de jogo)

        # Mostrar pontuação
        score_font = pygame.font.SysFont(None, 35)
        score_text = score_font.render(f"Pontos: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Atualiza a tela
        pygame.display.update()
        clock.tick(60)  # Aumenta para 60 FPS

    # Exibe mensagem de game over
    font = pygame.font.SysFont(None, 55)
    game_over_text = font.render(f" Pontos: {score}. Se LASCOU!", True, WHITE)
    screen.fill(BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Loop principal
show_logo()
show_developer_info()
while True:
    option = show_menu()
    if option == "novo":
        game_loop()
