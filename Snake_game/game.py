import pygame
import random
import sys
import math
import json
import os
from constants import screen, SCREEN_WIDTH as screen_width, SCREEN_HEIGHT as screen_height

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake Game")
FPS = 30
green = (0, 255, 0)
red = (255, 0, 0)
font = pygame.font.SysFont("jetbrains mono", 20)
clock = pygame.time.Clock()

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
    saves_folder = "Data"
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
