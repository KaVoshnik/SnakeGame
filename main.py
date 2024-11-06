import pygame
import random
import sys

pygame.init()
screen_width = 600
screen_height = 600
FPS = 30
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
green = (0, 255, 0)
red = (255, 0, 0)
font = pygame.font.SysFont("jetbrains mono", 20)
clock = pygame.time.Clock()


def main_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("jetbrains mono", 40)
    title_text = font.render("Snake Game", True, (255, 255, 255))
    screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, 100))

    font = pygame.font.SysFont("jetbrains mono", 20)
    play_text = font.render("Play", True, (255, 255, 255))
    screen.blit(play_text, (screen_width / 2 - play_text.get_width() / 2, 200))

    quit_text = font.render("Quit", True, (255, 255, 255))
    screen.blit(quit_text, (screen_width / 2 - quit_text.get_width() / 2, 250))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if screen_width / 2 - play_text.get_width() / 2 < event.pos[0] < screen_width / 2 + play_text.get_width() / 2 and 200 < event.pos[1] < 220:
                    return
                elif screen_width / 2 - quit_text.get_width() / 2 < event.pos[0] < screen_width / 2 + quit_text.get_width() / 2 and 250 < event.pos[1] < 270:
                    pygame.quit()
                    sys.exit()

def game_over_screen(score):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("jetbrains mono", 40)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, 100))

    font = pygame.font.SysFont("jetbrains mono", 20)
    score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, 150))

    restart_text = font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, (screen_width / 2 - restart_text.get_width() / 2, 200))

    menu_text = font.render("Menu", True, (255, 255, 255))
    screen.blit(menu_text, (screen_width / 2 - menu_text.get_width() / 2, 250))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if screen_width / 2 - restart_text.get_width() / 2 < event.pos[0] < screen_width / 2 + restart_text.get_width() / 2 and 200 < event.pos[1] < 220:
                    return "restart"
                elif screen_width / 2 - menu_text.get_width() / 2 < event.pos[0] < screen_width / 2 + menu_text.get_width() / 2 and 250 < event.pos[1] < 270:
                    return "menu"

def main():
    cell_size = 20
    snake_speed = 10
    snake_length = 3
    snake_body = []
    apple_position = pygame.Rect(random.randint(0, screen_width - cell_size), random.randint(0, screen_height - cell_size), cell_size, cell_size)


    while True:
        main_menu()
        game_over = False

        snake_body = []
        for i in range(snake_length):
            snake_body.append(pygame.Rect((screen_width / 2) - (cell_size * i), screen_height / 2, cell_size, cell_size))
        snake_direction = "right"
        new_direction = "right"

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake_direction != "down":
                        new_direction = "up"
                    elif event.key == pygame.K_DOWN and snake_direction != "up":
                        new_direction = "down"
                    elif event.key == pygame.K_LEFT and snake_direction != "right":
                        new_direction = "left"
                    elif event.key == pygame.K_RIGHT and snake_direction != "left":
                        new_direction = "right"

            snake_direction = new_direction
            if snake_direction == "up":
                snake_body.insert(0, pygame.Rect(snake_body[0].left, snake_body[0].top - cell_size, cell_size, cell_size))
            elif snake_direction == "down":
                snake_body.insert(0, pygame.Rect(snake_body[0].left, snake_body[0].top + cell_size, cell_size, cell_size))
            elif snake_direction == "left":
                snake_body.insert(0, pygame.Rect(snake_body[0].left - cell_size, snake_body[0].top, cell_size, cell_size))
            elif snake_direction == "right":
                snake_body.insert(0, pygame.Rect(snake_body[0].left + cell_size, snake_body[0].top, cell_size, cell_size))

            if snake_body[0].colliderect(apple_position):
                apple_position = pygame.Rect(random.randint(0, screen_width - cell_size), random.randint(0, screen_height-cell_size), cell_size, cell_size)
                snake_length += 1

            if len(snake_body) > snake_length:
                snake_body.pop()

            if snake_body[0].left < 0 or snake_body[0].right > screen_width or snake_body[0].top < 0 or snake_body[0].bottom > screen_height:
                game_over = True

            for i in range(1, len(snake_body)):
                if snake_body[0].colliderect(snake_body[i]):
                    game_over = True

            screen.fill((0, 0, 0))
            for i in range(len(snake_body)):
                if i == 0:
                    pygame.draw.circle(screen, green, snake_body[i].center, cell_size / 2)
                else:
                    pygame.draw.circle(screen, green, snake_body[i].center, cell_size / 2)
                    pygame.draw.circle(screen, (0, 200, 0), snake_body[i].center, cell_size / 4)

            pygame.draw.circle(screen, red, apple_position.center, cell_size / 2)

            score_text = font.render(f"Apple Score: {snake_length - 3}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            pygame.display.update()

            clock.tick(snake_speed)

            if game_over:
                score = snake_length - 3
                result = game_over_screen(score)
                if result == "restart":
                    game_over = False
                    snake_body = []
                    snake_length = 3
                    for i in range(snake_length):
                        snake_body.append(pygame.Rect((screen_width / 2) - (cell_size * i), screen_height / 2, cell_size, cell_size))
                    snake_direction = "right"
                    new_direction = "right"
                    apple_position = pygame.Rect(random.randint(0, screen_width - cell_size), random.randint(0, screen_height - cell_size), cell_size, cell_size)
                elif result == "menu":
                    snake_body = []
                    snake_length = 3
                    break

if __name__ == "__main__":
    main()