import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

def get_width_height():
    return pygame.display.Info().current_w / 8, pygame.display.Info().current_h / 8

def draw_borders(win, w, h):
    light = True
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

def draw_mouse(win, w, h):
    rect = ((pygame.mouse.get_pos()[0] // w) * w, (pygame.mouse.get_pos()[1] // h) * h, w, h)
    pygame.draw.rect(win, (255,0,0), rect, 5)

def mouse_selection(win, selection, pieces):
    w, h = get_width_height()
    mouse_pos = (pygame.mouse.get_pos()[0] // w) * w, (pygame.mouse.get_pos()[1] // h) * h
    if selection is not None:
        if selection.x == mouse_pos[0] and selection.y == mouse_pos[1]:
            return None
        else:
            selection.move(mouse_pos, pieces, w, h)
    else:
        for piece in pieces:
            if (piece.x, piece.y) == mouse_pos:
                return piece

def draw_selection(win, selection, w, h):
    if selection is not None:
        pygame.draw.rect(win, (0,255,0), ((selection.x // w) * w, (selection.y // h) * h, w, h), 5)

class Piece:
    def __init__(self, cords, width, height, piece):
        self.x = cords["x"]
        self.y = cords["y"]
        self.width = width
        self.height = height
        self.rect = (self.x, self.y, width, height)
        self.image = pygame.image.load(f"C:/Code/Python/Chess/Pieces/{piece}.png")
        self.alive = True
        self.team = ""

    def draw(self, win):
        win.blit(self.image, self.rect)
    
    def register_hit(self, pieces):
        for piece in pieces:
            if self is not piece and piece.alive and self.team != piece.team and self.x == piece.x and self.y == piece.y:
                pieces.remove(piece)
                return

class King(Piece):
    def __init__(self, cords, width, height, team):
        super().__init__(cords, width, height, "King_" + team)
        self.team = team
    
    def move(self, pos, pieces, w, h):
        for piece in pieces:
            if self is not piece and self.team == piece.team and pos[0] == piece.x and pos[1] == piece.y:
                return
        if abs(pos[0] - self.x) // w <= 1 and abs(pos[1] - self.y) // h <= 1:
            self.x = pos[0]
            self.y = pos[1]
            self.rect = (self.x, self.y, self.width, self.height)
            self.register_hit(pieces)

def main():
    playing = True
    w, h = get_width_height()
    board = square_cords()
    pieces = [King(board[0][0],w,h,"B"), King(board[1][0],w,h,"W")]
    selection = None
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONUP:
                selection = mouse_selection(win, selection, pieces)
        w, h = get_width_height()
        board = square_cords()
        win.fill((255, 255, 255))
        draw_borders(win, w, h)
        for piece in pieces:
            piece.draw(win)
        draw_mouse(win, w, h)
        draw_selection(win, selection, w, h)
        pygame.display.flip()

if __name__ == "__main__":
    main()
