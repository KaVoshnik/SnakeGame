import pygame
import random
import sys
import math
import json
import os

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
    play_rect = play_text.get_rect(center=(screen_width / 2, 200))
    screen.blit(play_text, play_rect)

    quit_text = font.render("Quit", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(screen_width / 2, 250))
    screen.blit(quit_text, quit_rect)

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

def game_over_screen(score, records_text=None):
    screen.fill((0, 0, 0))

    if records_text:
        font = pygame.font.SysFont("jetbrains mono", 20)
        text = font.render(f"Record: {records_text}", True, (255, 255, 255))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, 130))

    font = pygame.font.SysFont("jetbrains mono", 40)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, 50))

    font = pygame.font.SysFont("jetbrains mono", 20)
    score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, 100))

    restart_text = font.render("Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(screen_width / 2, 200))
    screen.blit(restart_text, restart_rect)

    menu_text = font.render("Menu", True, (255, 255, 255))
    menu_rect = menu_text.get_rect(center=(screen_width / 2, 250))
    screen.blit(menu_text, menu_rect)

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

def difficulty_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("jetbrains mono", 40)
    title_text = font.render("Choose Difficulty", True, (255, 255, 255))
    screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, 100))

    font = pygame.font.SysFont("jetbrains mono", 20)
    easy_text = font.render("Easy", True, (255, 255, 255))
    screen.blit(easy_text, (screen_width / 2 - easy_text.get_width() / 2, 200))

    medium_text = font.render("Medium", True, (255, 255, 255))
    screen.blit(medium_text, (screen_width / 2 - medium_text.get_width() / 2, 250))

    hard_text = font.render("Hard", True, (255, 255, 255))
    screen.blit(hard_text, (screen_width / 2 - hard_text.get_width() / 2, 300))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if screen_width / 2 - easy_text.get_width() / 2 < event.pos[0] < screen_width / 2 + easy_text.get_width() / 2 and 200 < event.pos[1] < 220:
                    return "easy"
                elif screen_width / 2 - medium_text.get_width() / 2 < event.pos[0] < screen_width / 2 + medium_text.get_width() / 2 and 250 < event.pos[1] < 270:
                    return "medium"
                elif screen_width / 2 - hard_text.get_width() / 2 < event.pos[0] < screen_width / 2 + hard_text.get_width() / 2 and 300 < event.pos[1] < 320:
                    return "hard"


def save_score(score, difficulty):
    saves_folder = "saves"
    if not os.path.exists(saves_folder):
        os.makedirs(saves_folder)
    save_file = os.path.join(saves_folder, "score.json")
    data = {}
    try:
        with open(save_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        pass

    if "total_score" not in data:
        data["total_score"] = 0
    data["total_score"] += score

    if "records" not in data:
        data["records"] = {}
    if difficulty not in data["records"] or score > data["records"][difficulty]:
        data["records"][difficulty] = score

    data["last_score"] = score

    with open(save_file, "w") as f:
        json.dump(data, f)


def main():
    cell_size = 20
    snake_speed = 10
    snake_length = 3
    snake_body = []
    apple_position = pygame.Rect(random.randint(0, screen_width - cell_size), random.randint(0, screen_height - cell_size), cell_size, cell_size)


    while True:
        main_menu()
        difficulty = difficulty_menu()
        game_over = False

        if difficulty == "easy":
            snake_speed = 10
        elif difficulty == "medium":
            snake_speed = 15
        elif difficulty == "hard":
            snake_speed = 20


        snake_body = []
        for i in range(snake_length):
            snake_body.append(pygame.Rect((screen_width / 2) - (cell_size * i), screen_height / 2, cell_size, cell_size))
        snake_direction = "right"
        new_direction = "right"

        while not game_over:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        game_over = True
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_UP:
                                if snake_direction != "down":
                                    snake_direction = "up"
                            case pygame.K_DOWN:
                                if snake_direction != "up":
                                    snake_direction = "down"
                            case pygame.K_LEFT:
                                if snake_direction != "right":
                                    snake_direction = "left"
                            case pygame.K_RIGHT:
                                if snake_direction != "left":
                                    snake_direction = "right"

            match snake_direction:
                case "up":
                    snake_body.insert(0, pygame.Rect(snake_body[0].left, snake_body[0].top - cell_size, cell_size, cell_size))
                case "down":
                    snake_body.insert(0, pygame.Rect(snake_body[0].left, snake_body[0].top + cell_size, cell_size, cell_size))
                case "left":
                    snake_body.insert(0, pygame.Rect(snake_body[0].left - cell_size, snake_body[0].top, cell_size, cell_size))
                case "right":
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
                if difficulty == "easy":
                    score *= 0.5
                    score = math.floor(score)
                    save_score(score, difficulty)
                if difficulty == "medium":
                    score *= 1
                    save_score(score, difficulty)
                elif difficulty == "hard":
                    score *= 1.5
                    score = math.floor(score)
                    save_score(score, difficulty)

                saves_folder = "saves"
                save_file = os.path.join(saves_folder, "score.json")
                with open(save_file, "r") as f:
                    data = json.load(f)

                records_text = ""
                records_text = data["records"].get(difficulty, 0)
                #records_text += f"{difficulty.capitalize()}: {record}\n"
                    
                result = game_over_screen(score, records_text)
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