import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

def draw_borders(win):
    w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
    for i in range(0, 9):
        pygame.draw.line(win, (0,0,0), (w / 8 * i, 0), (w / 8 * i, h))
        pygame.draw.line(win, (0,0,0), (0, h / 8 * i), (w, h / 8 * i))

def main():
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        win.fill((255, 255, 255))
        draw_borders(win)
        pygame.display.flip()

if __name__ == "__main__":
    main()
