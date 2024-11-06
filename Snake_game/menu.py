import pygame
import sys
from constants import screen, SCREEN_WIDTH as screen_width

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
