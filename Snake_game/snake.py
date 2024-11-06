import pygame
import random
import math
import os
import json
from constants import screen, SCREEN_WIDTH, SCREEN_HEIGHT
from menu import main_menu
from game import difficulty_menu, game_over_screen, save_score

FPS = 30
green = (0, 255, 0)
red = (255, 0, 0)
font = pygame.font.SysFont("jetbrains mono", 20)
clock = pygame.time.Clock()

def main():
    cell_size = 20
    snake_speed = 10
    snake_length = 3
    snake_body = []
    apple_position = pygame.Rect(
        random.randint(0, SCREEN_WIDTH // cell_size - 1) * cell_size,
        random.randint(0, SCREEN_HEIGHT // cell_size - 1) * cell_size,
        cell_size,
        cell_size
    )

    while apple_position.collidelist(snake_body) != -1:
        apple_position = pygame.Rect(
            random.randint(0, SCREEN_WIDTH // cell_size - 1) * cell_size,
            random.randint(0, SCREEN_HEIGHT // cell_size - 1) * cell_size,
            cell_size,
            cell_size
        )

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
            snake_body.append(pygame.Rect((SCREEN_WIDTH / 2) - (cell_size * i), SCREEN_HEIGHT / 2, cell_size, cell_size))
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
                apple_position = pygame.Rect(random.randint(0, SCREEN_WIDTH - cell_size), random.randint(0, SCREEN_HEIGHT-cell_size), cell_size, cell_size)
                snake_length += 1

            if len(snake_body) > snake_length:
                snake_body.pop()

            if snake_body[0].left < 0 or snake_body[0].right > SCREEN_WIDTH or snake_body[0].top < 0 or snake_body[0].bottom > SCREEN_HEIGHT:
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

                saves_folder = "Data"
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
                        snake_body.append(pygame.Rect((SCREEN_WIDTH / 2) - (cell_size * i), SCREEN_HEIGHT / 2, cell_size, cell_size))
                    snake_direction = "right"
                    new_direction = "right"
                    apple_position = pygame.Rect(random.randint(0, SCREEN_WIDTH - cell_size), random.randint(0, SCREEN_HEIGHT - cell_size), cell_size, cell_size)
                elif result == "menu":
                    snake_body = []
                    snake_length = 3
                    break