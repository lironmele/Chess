import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

def draw_borders(win):
    light = True
    w, h = pygame.display.Info().current_w / 8, pygame.display.Info().current_h / 8
    for y in range(8):
        for x in range(8):
            if (light):
                pygame.draw.rect(win, (229,246,206), (w * x, h * y, w, h))
                light = False
            else:
                pygame.draw.rect(win, (177,200,103), (w * x, h * y, w, h))
                light = True
        light = not light

def square_cords():
    board = [[],[],[],[],[],[],[],[]]
    w, h = pygame.display.Info().current_w / 8, pygame.display.Info().current_h / 8
    for col in range(8):
        for row in range(8):
            board[col].append({"x":col * w, "y":row * h})
    return board


class Piece:
    def __init__(self, cords, width, height, piece):
        self.x = cords["x"]
        self.y = cords["y"]
        self.width = width
        self.height = height
        self.rect = (self.x, self.y, width, height)
        self.image = pygame.image.load(f"C:/Code/Python/Chess/Pieces/{piece}.png")
        self.Alive = True
    def draw(self, win):
        win.blit(self.image, self.rect)

def main():
    playing = True
    w, h = pygame.display.Info().current_w / 8, pygame.display.Info().current_h / 8
    board = square_cords()
    pieces = [Piece(board[0][0],w,h,"Rook_B"), Piece(board[1][0],w,h,"Knight_B")]
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        baord = square_cords()
        win.fill((255, 255, 255))
        draw_borders(win)
        for piece in pieces:
            piece.draw(win)
        pygame.display.flip()

if __name__ == "__main__":
    main()
