from constants import screen, SCREEN_WIDTH as screen_width, SCREEN_HEIGHT as screen_height
from menu import main_menu
import pygame
import json

def leaderboard():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont("jetbrains mono", 40)
    title_text = font.render("Leaderboard", True, (255, 255, 255))
    screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, 100))

    with open("Data/score.json", "r") as f:
        data = json.load(f)

    font = pygame.font.SysFont("jetbrains mono", 20)
    records_text = []
    for difficulty, score in data["records"].items():
        records_text.append(f"{difficulty.capitalize()}: {score}")

    for i, text in enumerate(records_text):
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (screen_width / 2 - text_surface.get_width() / 2, 200 + i * 30))

    exit_button_text = font.render("Exit", True, (255, 255, 255))
    exit_button_rect = exit_button_text.get_rect(center=(screen_width / 2, screen_height - 50))
    screen.blit(exit_button_text, exit_button_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    main_menu()