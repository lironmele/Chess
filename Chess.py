import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

def get_width_height():
    return pygame.display.Info().current_w / 8, pygame.display.Info().current_h / 8

def draw_borders(win):
    light = True
    w, h = get_width_height()
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
    w, h = get_width_height()
    for col in range(8):
        for row in range(8):
            board[col].append({"x":col * w, "y":row * h})
    return board

def draw_mouse(win):
    w, h = get_width_height()
    rect = ((pygame.mouse.get_pos()[0] // w) * w, (pygame.mouse.get_pos()[1] // h) * h, w, h)
    pygame.draw.rect(win, (255,0,0), rect, 5)

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
    
    def check_hit(self, pieces):
        for piece in pieces:
            if self != piece and piece.Alive and self.x == piece.x and self.y == piece.y:
                piece.Alive = False
                return

def main():
    playing = True
    w, h = get_width_height()
    board = square_cords()
    pieces = [Piece(board[0][0],w,h,"Rook_B"), Piece(board[1][0],w,h,"Knight_B")]
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        board = square_cords()
        win.fill((255, 255, 255))
        draw_borders(win)
        for piece in pieces:
            if piece.Alive:
                piece.draw(win)
        draw_mouse(win)
        pygame.display.flip()

if __name__ == "__main__":
    main()
