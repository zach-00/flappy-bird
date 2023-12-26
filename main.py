import pygame
import os
import random
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")
game_font = pygame.font.Font(os.path.join("Assets", "PixelifySans.ttf"), 50)
intro_font = pygame.font.Font(os.path.join("Assets", "PressStart2P.ttf"), 75)
message_font = pygame.font.Font(os.path.join("Assets", "Orbitron.ttf"), 50)
game_active = True

score = 0

WIDTH = 1000
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.png")), (WIDTH, HEIGHT))

bird = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "flappy-bird.png")), (70, 35))
# bird_rect2 = pygame.Rect(100, 300, 80, 40)
bird_rect = bird.get_rect(center=(100,300))

ground = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "ground.png")), (1500, 100))
ground_rect = ground.get_rect(bottom=750)

pipe = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "pipe.png")), (120, 315))
pipe_rect = pipe.get_rect(center=(900, 525)) # 480 pixel gap between pipes

top_pipe = pygame.transform.rotozoom(pipe, 180, 1)
top_pipe_rect = top_pipe.get_rect(center=(894, 45)) # 480 pixel gap between pipes

# Intro Screen
bird_3d = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets", "flappy-bird-3d.png")), 0, 1.2)
bird_3d_rect = bird_3d.get_rect(center=(500, 375))

game_name = intro_font.render("Flappy Bird!", False, "Black")
game_name_rect = game_name.get_rect(center=(500, 100))

game_message = message_font.render("Press space to play!", False, "Black")
game_message_rect = game_message.get_rect(center=(500, 650))

bird_gravity = 0


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_gravity = -15
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                bird_rect.center = (100, 300)
                pipe_rect.center = (900, 525)
                top_pipe_rect.center = (894, 45)
                bird_gravity = 0
                score = 0


    if game_active:
        score_surf = game_font.render(f"Score: {score}", False, "Black")
        score_rect = score_surf.get_rect(center = (500, 50))
        screen.blit(background, (0, 0))
        screen.blit(bird, bird_rect)
        screen.blit(pipe, pipe_rect)
        screen.blit(score_surf, score_rect)
        screen.blit(ground, ground_rect)
        screen.blit(top_pipe, top_pipe_rect)

        # Game speed
        ground_rect.x -= 6
        pipe_rect.x -= 6
        top_pipe_rect.x -= 6


        # Ground reset
        if ground_rect.right == 1080:
            ground_rect.right = 1500

        # Dynamic Pipe reset placement
        random_num = random.randint(450, 600)
        if pipe_rect.right <= 0:
            pipe_rect.center = (1000, random_num)

        if top_pipe_rect.right <= 0:
            top_pipe_rect.center = (1000, (random_num - 480))


        # Score
        if pipe_rect.right < 135 and pipe_rect.right > 128:
            score += 1


        # Bird
        bird_gravity += 1
        bird_rect.y += bird_gravity

        # collisions
        if bird_rect.colliderect(pipe_rect) or bird_rect.colliderect(top_pipe_rect):
            game_active = False
        if bird_rect.colliderect(ground_rect):
            game_active = False

    else: # Game Over / Intro Screen
        screen.fill("#1ecbe1")
        screen.blit(bird_3d, bird_3d_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)

    pygame.display.update()
    clock.tick(60)
