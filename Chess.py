import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

def draw_borders(win):
    w, h = pygame.display.Info().current_w / 8, pygame.display.Info().current_h / 8
    for y in range(8):
        for x in range(8):
            if ((x % 2 == 0 and y % 2 == 1) or (x % 2 == 1 and y % 2 == 0)):
                pygame.draw.rect(win, (0,0,0), (w * x, h * y, w, h))

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
