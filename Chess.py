import pygame, requests, numpy, os
pygame.init()

server_ip = "localhost"

#detect automatically in the future
side = input("What side are you?\n")
requests.get(f"http://{server_ip}:3000/")
win = pygame.display.set_mode((500, 500))

if side == "White":
    turn = True
elif side == "Black":
    turn = False

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

def square_pos():
    board = [[],[],[],[],[],[],[],[]]
    w, h = get_width_height()
    for col in range(8):
        for row in range(8):
            board[col].append({"x":col * w, "y":row * h})
    return board

def draw_mouse(win, w, h):
    rect = ((pygame.mouse.get_pos()[0] // w) * w, (pygame.mouse.get_pos()[1] // h) * h, w, h)
    pygame.draw.rect(win, (255,0,0), rect, 5)

def mouse_selection(win, selection, pieces, mouse_pos=None):
    w, h = get_width_height()
    if mouse_pos is None:
        mouse_pos = (pygame.mouse.get_pos()[0] // w) * w, (pygame.mouse.get_pos()[1] // h) * h
    if selection is not None:
        if selection.x == mouse_pos[0] and selection.y == mouse_pos[1]:
            return None
        else:
            old_pos = [selection.x, selection.y]
            if selection.move(mouse_pos, pieces, w, h) is True and turn:
                send_turn(old_pos, [selection.x, selection.y])
    else:
        for piece in pieces:
            if (piece.x, piece.y) == mouse_pos or [piece.x, piece.y] == mouse_pos:
                return piece

def draw_selection(win, selection, w, h):
    if selection is not None:
        pygame.draw.rect(win, (0,255,0), ((selection.x // w) * w, (selection.y // h) * h, w, h), 5)

def fill_pieces(board, w, h):
    pieces = [
    King(board[4][0],w,h,"B"), Queen(board[3][0],w,h,"B"), Bishop(board[2][0],w,h,"B"),Bishop(board[5][0],w,h,"B"),
    Knight(board[1][0], w, h, "B"), Knight(board[6][0], w, h, "B"), Rook(board[0][0], w, h, "B"), Rook(board[7][0], w, h, "B")
    ]
    
    for i in range(8):
        pieces.append(Pawn(board[i][1], w, h, "B"))
    
    pieces.extend([King(board[4][7],w,h,"W"), Queen(board[3][7],w,h,"W"), Bishop(board[2][7],w,h,"W"),Bishop(board[5][7],w,h,"W"),
            Knight(board[1][7], w, h, "W"), Knight(board[6][7], w, h, "W"), Rook(board[0][7], w, h, "W"), Rook(board[7][7], w, h, "W")])
    
    for i in range(8):
        pieces.append(Pawn(board[i][6], w, h, "W"))

    return pieces

class Piece:
    def __init__(self, pos, width, height, piece, team):
        self.x = pos["x"]
        self.y = pos["y"]
        self.width = width
        self.height = height
        self.rect = (self.x, self.y, width, height)
        self.image = pygame.image.load(f"{os.curdir}/Pieces/{piece}.png")
        self.alive = True
        self.team = team

    def draw(self, win):
        win.blit(self.image, self.rect)

    def get_dif_pos(self, pos, w, h):
        return abs(pos[0] - self.x) // w, abs(pos[1] - self.y) // h

    def hit_team(self, pos, pieces):
        for piece in pieces:
            if self is not piece and self.team == piece.team and pos[0] == piece.x and pos[1] == piece.y:
                return True
        return False
    
    def register_hit(self, pieces):
        for piece in pieces:
            if self is not piece and piece.alive and self.team != piece.team and self.x == piece.x and self.y == piece.y:
                if isinstance(piece, King):
                    game_over(piece.team)
                pieces.remove(piece)
                

    def update_pos(self, pos, pieces):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = (self.x, self.y, self.width, self.height)
        self.register_hit(pieces)

    def is_way_free_x(self, pos, pieces, w):
        pos = list(pos)
        if pos[0] - self.x > 0:
            pos[0] -= w
        elif pos[0] - self.x < 0:
            pos[0] += w
        if abs(pos[0] - self.x) == 0:
            return True
        for piece in pieces:
            if self is piece:
                continue
            elif pos[0] == piece.x and pos[1] == piece.y:
                return False
        return self.is_way_free_x(pos, pieces, w)

    def is_way_free_y(self, pos, pieces, h):
        pos = list(pos)
        if pos[1] - self.y > 0:
            pos[1] -= h
        elif pos[1] - self.y < 0:
            pos[1] += h
        if abs(pos[1] - self.y) == 0:
            return True
        for piece in pieces:
            if self is piece:
                continue
            elif pos[0] == piece.x and pos[1] == piece.y:
                return False
        return self.is_way_free_y(pos, pieces, h)

    def is_way_free_diagonal_main(self, pos, pieces, w, h):
        pos = list(pos)
        if pos[0] - self.x > 0:
            pos[0] -= w
            pos[1] -= h
        elif pos[0] - self.x < 0:
            pos[0] += w
            pos[1] += h
        if abs(pos[1] - self.y) == 0:
            return True
        for piece in pieces:
            if self is piece:
                continue
            elif pos[0] == piece.x and pos[1] == piece.y:
                return False
        return self.is_way_free_diagonal_main(pos, pieces, w, h)

    def is_way_free_diagonal_secondary(self, pos, pieces, w, h):
        pos = list(pos)
        if pos[0] - self.x > 0:
            pos[0] -= w
            pos[1] += h
        elif pos[0] - self.x < 0:
            pos[0] += w
            pos[1] -= h
        if abs(pos[1] - self.y) == 0:
            return True
        for piece in pieces:
            if self is piece:
                continue
            elif pos[0] == piece.x and pos[1] == piece.y:
                return False
        return self.is_way_free_diagonal_secondary(pos, pieces, w, h)

class King(Piece):
    def __init__(self, pos, width, height, team):
        super().__init__(pos, width, height, "King_" + team, team)
    
    def move(self, pos, pieces, w, h):
        if self.hit_team(pos, pieces):
            return
        dif_x, dif_y = self.get_dif_pos(pos, w, h)
        if dif_x <= 1 and dif_y <= 1:
            self.update_pos(pos, pieces)
            return True

class Queen(Piece):
    def __init__(self, pos, width, height, team):
        super().__init__(pos, width, height, "Queen_" + team, team)

    def move(self, pos, pieces, w, h):
        if self.hit_team(pos, pieces):
            return
        dif_x, dif_y = self.get_dif_pos(pos, w, h)
        if (pos[0] - self.x) == (pos[1] - self.y) and self.is_way_free_diagonal_main(pos, pieces, w, h):
            self.update_pos(pos, pieces)
            return True
        elif (pos[0] - self.x) == -(pos[1] - self.y) and self.is_way_free_diagonal_secondary(pos, pieces, w, h):
            self.update_pos(pos, pieces)
            return True
        elif dif_x != 0 and dif_y == 0 and self.is_way_free_x(pos, pieces, w):
            self.update_pos(pos, pieces)
            return True
        elif dif_x == 0 and dif_y != 0 and self.is_way_free_y(pos, pieces, h):
            self.update_pos(pos, pieces)
            return True

class Bishop(Piece):
    def __init__(self, pos, width, height, team):
        super().__init__(pos, width, height, "Bishop_" + team, team)

    def move(self, pos, pieces, w, h):
        if self.hit_team(pos, pieces):
            return
        dif_x, dif_y = self.get_dif_pos(pos, w, h)
        if pos[0] - self.x == pos[1] - self.y and self.is_way_free_diagonal_main(pos, pieces, w, h):
            self.update_pos(pos, pieces)
            return True
        if pos[0] - self.x == -(pos[1] - self.y) and self.is_way_free_diagonal_secondary(pos, pieces, w, h):
            self.update_pos(pos, pieces)
            return True

class Knight(Piece):
    def __init__(self, pos, width, height, team):
        super().__init__(pos, width, height, "Knight_" + team, team)
    
    def move(self, pos, pieces, w, h):
        if self.hit_team(pos, pieces):
            return
        dif_x, dif_y = self.get_dif_pos(pos, w, h)
        if dif_x == 2 and dif_y == 1 or dif_x == 1 and dif_y == 2:
            self.update_pos(pos, pieces)
            return True

class Rook(Piece):
    def __init__(self, pos, width, height, team):
        super().__init__(pos, width, height, "Rook_" + team, team)

    def move(self, pos, pieces, w, h):
        if self.hit_team(pos, pieces):
            return
        dif_x, dif_y = self.get_dif_pos(pos, w, h)
        if dif_x == 0 and dif_y != 0 and self.is_way_free_y(pos, pieces, h):
            self.update_pos(pos, pieces)
            return True
        elif dif_x != 0 and dif_y == 0 and self.is_way_free_x(pos, pieces, w):
            self.update_pos(pos, pieces)
            return True

class Pawn(Piece):
    def __init__(self, pos, width, height, team):
        super().__init__(pos, width, height, "Pawn_" + team, team)
        self.first_turn = True
        
    def move(self, pos, pieces, w, h):
        if self.hit_team(pos, pieces):
            return
        if pos[1] - self.y > 0 and self.team == "W" or pos[1] - self.y < 0 and self.team == "B":
            return
        dif_x, dif_y = self.get_dif_pos(pos, w, h)
        if dif_x == 0 and dif_y == 1 and not self.is_way_blocked(pos, pieces, h):
            self.update_pos(pos)
            self.first_turn = False
            return True
        elif self.first_turn and dif_x == 0 and dif_y == 2 and not self.is_way_blocked(pos, pieces, h):
            self.update_pos(pos)
            self.first_turn = False
            return True
        elif dif_x == 1 and dif_y == 1 and self.is_eating(pos, pieces):
            super().update_pos(pos, pieces)
            self.first_turn = False
            return True

    def is_eating(self, pos, pieces):
        for piece in pieces:
            if self is piece or self.team == piece.team:
                continue

            if pos[0] == piece.x and pos[1] == piece.y:
                return True
        return False

    def is_way_blocked(self, pos, pieces, h):
        for piece in pieces:
            if self is piece:
                continue
      
            if self.team == "B":
                for y in numpy.arange(self.y, pos[1] + h, h):  
                    if pos[0] == piece.x and y == piece.y:
                            return True
            elif self.team == "W":
                for y in numpy.arange(pos[1], self.y + h, h):
                    if pos[0] == piece.x and y == piece.y:
                            return True
        return False

    def update_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = (self.x, self.y, self.width, self.height)

def game_over(team):
    if team == "B":
        team = "White"
    elif team == "W":
        team = "Black"
    overfont = pygame.font.SysFont('agencyfb', 75)
    overtext = overfont.render("Game Over!", True, (0,0,0))
    w, h = get_width_height()
    win.blit(overtext, (100, 100))
    pygame.display.flip()
    pygame.time.delay(1000)
    winteamfont = pygame.font.SysFont('agencyfb', 75)
    winteamtext = winteamfont.render('{} team wins!'.format(team), True, (0,0,0))
    win.blit(overtext, (100, 100))
    win.blit(winteamtext, (50, 200))
    pygame.display.flip()
    pygame.time.delay(2500)

def wait_turn():
    r = requests.get(f"http://{server_ip}:3000/{side}")
    if r.status_code == 200:
        headers = r.headers
        return [float(headers['old_x']), float(headers['old_y']), float(headers['new_x']), float(headers['new_y'])]
    else:
        return "Try Again"

def send_turn(old_pos, new_pos):
    r = requests.post(f"http://{server_ip}:3000/{side}", headers={"old_x":str(old_pos[0]), "old_y":str(old_pos[1])
    , "new_x":str(new_pos[0]), "new_y":str(new_pos[1])})
    global turn
    turn = False

def main():
    playing = True
    w, h = get_width_height()
    board = square_pos()
    pieces = fill_pieces(board, w, h)
    selection = None
    global turn
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONUP and turn:
                selection = mouse_selection(win, selection, pieces)
                if selection is not None and selection.team != side[0]:
                    selection = None
        w, h = get_width_height()
        board = square_pos()
        win.fill((255, 255, 255))
        draw_borders(win, w, h)
        if not turn:
            enemy_move = wait_turn()
            if enemy_move != "Try Again":
                selection = mouse_selection(win, selection, pieces, mouse_pos=enemy_move[:2])
                selection = mouse_selection(win, selection, pieces, mouse_pos=enemy_move[2:])
                turn = True
        for piece in pieces:
            piece.draw(win)
        draw_mouse(win, w, h)
        draw_selection(win, selection, w, h)
        pygame.display.flip()

if __name__ == "__main__":
    main()
