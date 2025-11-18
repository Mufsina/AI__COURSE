import pygame, sys, os, copy, math, random, time
from dataclasses import dataclass


FPS = 60
BOARD_SIZE = 640
SIDEBAR_W = 360
WIDTH = BOARD_SIZE + SIDEBAR_W
HEIGHT = 720
SQUARE = BOARD_SIZE // 8
BOARD_ORIGIN = (20, 20)
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

AI_DEPTH = 2


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Offline Chess — Single-file (Pygame)")
clock = pygame.time.Clock()


WHITE = (245,245,245)
BLACK = (30,30,30)
LIGHT = (240,217,181)
DARK  = (181,136,99)
HIGHLIGHT = (86,180,90)
LASTMOVE = (100,150,220)
HINTCOLOR = (220,80,80)
SIDEBAR_BG = (240,240,245)
TEXT = (20,20,20)
BUTTON_BG = (200,200,210)
RED = (220,40,40)

FONT = pygame.font.SysFont("Arial", 16)
BIG = pygame.font.SysFont("Arial", 20, bold=True)
SMALL = pygame.font.SysFont("Arial", 14)

UNICODE = {
    'wK':'\u2654','wQ':'\u2655','wR':'\u2656','wB':'\u2657','wN':'\u2658','wP':'\u2659',
    'bK':'\u265A','bQ':'\u265B','bR':'\u265C','bB':'\u265D','bN':'\u265E','bP':'\u265F'
}

@dataclass
class Move:
    start: tuple
    end: tuple
    piece: str
    captured: str = None
    promotion: str = None
    is_en_passant: bool = False
    is_castling: bool = False

    def __repr__(self):
        s = f"{self.piece}@{self.start}->{self.end}"
        if self.captured: s += f"x{self.captured}"
        if self.promotion: s += f"={self.promotion}"
        if self.is_castling: s += " (castle)"
        if self.is_en_passant: s += " (ep)"
        return s

class Board:
    def __init__(self):
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.white_to_move = True
        self.castling_rights = {'wK': True, 'wQ': True, 'bK': True, 'bQ': True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.move_history = []  
        self.setup_start()

    def setup_start(self):
        pieces = ['R','N','B','Q','K','B','N','R']
        self.board[0] = ['b'+p for p in pieces]
        self.board[1] = ['bP']*8
        for r in range(2,6): self.board[r] = ['']*8
        self.board[6] = ['wP']*8
        self.board[7] = ['w'+p for p in pieces]
        self.white_to_move = True
        self.castling_rights = {'wK': True, 'wQ': True, 'bK': True, 'bQ': True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.move_history = []

    def clone(self):
        return copy.deepcopy(self)

    def piece_at(self, r,c): return self.board[r][c]

    def same_color(self,a,b):
        if not a or not b: return False
        return a[0] == b[0]

    def is_white(self,p): return p and p[0]=='w'
    def is_black(self,p): return p and p[0]=='b'

    def generate_moves(self):
        moves = []
        side = 'w' if self.white_to_move else 'b'
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if not p or p[0] != side: continue
                moves.extend(self._moves_for_piece(r,c,p))
        
        legal = []
        for m in moves:
            snap = self._make_move_internal(m)
            if not self.is_in_check('w' if self.white_to_move else 'b'):
                legal.append(m)
            self._unmake_move_internal(snap)
        return legal

    def _moves_for_piece(self, r, c, piece):
        color = piece[0]; p_type = piece[1]
        moves = []
        def inb(rr,cc): return 0<=rr<8 and 0<=cc<8
        if p_type == 'P':
            dir_ = -1 if color=='w' else 1
            start_row = 6 if color=='w' else 1
            nr, nc = r+dir_, c
            if inb(nr,nc) and self.board[nr][nc]=='':
                if nr==0 or nr==7:
                    for promo in ['Q','R','B','N']: moves.append(Move((r,c),(nr,nc),piece,promotion=promo))
                else: moves.append(Move((r,c),(nr,nc),piece))
                nr2 = r + 2*dir_
                if r==start_row and inb(nr2,nc) and self.board[nr2][nc]=='':
                    moves.append(Move((r,c),(nr2,nc),piece))
            for dc in (-1,1):
                cr, cc = r+dir_, c+dc
                if inb(cr,cc):
                    target = self.board[cr][cc]
                    if target and not self.same_color(target,piece):
                        if cr==0 or cr==7:
                            for promo in ['Q','R','B','N']: moves.append(Move((r,c),(cr,cc),piece,captured=target,promotion=promo))
                        else: moves.append(Move((r,c),(cr,cc),piece,captured=target))
            
            if self.en_passant_target:
                er, ec = self.en_passant_target
                if er == r + dir_ and abs(ec - c) == 1:
                    cap_r, cap_c = r, ec
                    moves.append(Move((r,c),(er,ec),piece,captured=self.board[cap_r][cap_c],is_en_passant=True))
        elif p_type in ('R','B','Q'):
            directions = []
            if p_type=='R': directions = [(-1,0),(1,0),(0,-1),(0,1)]
            if p_type=='B': directions = [(-1,-1),(-1,1),(1,-1),(1,1)]
            if p_type=='Q': directions = directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
            for dr,dc in directions:
                nr, nc = r+dr, c+dc
                while inb(nr,nc):
                    tgt = self.board[nr][nc]
                    if tgt=='':
                        moves.append(Move((r,c),(nr,nc),piece))
                    else:
                        if not self.same_color(tgt,piece):
                            moves.append(Move((r,c),(nr,nc),piece,captured=tgt))
                        break
                    nr += dr; nc += dc
        elif p_type == 'N':
            for dr,dc in [(-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2)]:
                nr, nc = r+dr, c+dc
                if inb(nr,nc):
                    tgt = self.board[nr][nc]
                    if tgt=='' or not self.same_color(tgt,piece):
                        moves.append(Move((r,c),(nr,nc),piece,captured=tgt if tgt!='' else None))
        elif p_type == 'K':
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr==0 and dc==0: continue
                    nr, nc = r+dr, c+dc
                    if inb(nr,nc):
                        tgt = self.board[nr][nc]
                        if tgt=='' or not self.same_color(tgt,piece):
                            moves.append(Move((r,c),(nr,nc),piece,captured=tgt if tgt!='' else None))
            # castling
            if color=='w' and r==7 and c==4:
                if self.castling_rights.get('wK') and self.board[7][5]=='' and self.board[7][6]=='':
                    moves.append(Move((r,c),(7,6),piece,is_castling=True))
                if self.castling_rights.get('wQ') and self.board[7][3]=='' and self.board[7][2]=='' and self.board[7][1]=='':
                    moves.append(Move((r,c),(7,2),piece,is_castling=True))
            if color=='b' and r==0 and c==4:
                if self.castling_rights.get('bK') and self.board[0][5]=='' and self.board[0][6]=='':
                    moves.append(Move((r,c),(0,6),piece,is_castling=True))
                if self.castling_rights.get('bQ') and self.board[0][3]=='' and self.board[0][2]=='' and self.board[0][1]=='':
                    moves.append(Move((r,c),(0,2),piece,is_castling=True))
        return moves

    def _make_move_internal(self, move):
        snapshot = {
            'board': [row[:] for row in self.board],
            'white_to_move': self.white_to_move,
            'castling_rights': self.castling_rights.copy(),
            'en_passant_target': self.en_passant_target,
            'halfmove_clock': self.halfmove_clock,
            'fullmove_number': self.fullmove_number
        }
        sr, sc = move.start; er, ec = move.end
        piece = self.board[sr][sc]
        
        if move.is_en_passant and self.en_passant_target:
            cap_r = sr; cap_c = ec
            captured = self.board[cap_r][cap_c]
            self.board[cap_r][cap_c] = ''
            move.captured = captured
       
        if move.is_castling:
            if ec == 6: 
                rook_sr, rook_sc = sr, 7; rook_er, rook_ec = sr, 5
            else:
                rook_sr, rook_sc = sr, 0; rook_er, rook_ec = sr, 3
            rook_piece = self.board[rook_sr][rook_sc]
            self.board[rook_er][rook_ec] = rook_piece
            self.board[rook_sr][rook_sc] = ''
        
        cap = self.board[er][ec]
        if cap and not move.captured:
            move.captured = cap
       
        self.board[er][ec] = self.board[sr][sc]
        self.board[sr][sc] = ''
      
        if move.promotion:
            self.board[er][ec] = self.board[er][ec][0] + move.promotion
        
        if piece[1] == 'K':
            if piece[0]=='w': self.castling_rights['wK']=False; self.castling_rights['wQ']=False
            else: self.castling_rights['bK']=False; self.castling_rights['bQ']=False
        if piece[1] == 'R':
            if sr==7 and sc==0: self.castling_rights['wQ']=False
            if sr==7 and sc==7: self.castling_rights['wK']=False
            if sr==0 and sc==0: self.castling_rights['bQ']=False
            if sr==0 and sc==7: self.castling_rights['bK']=False
        
        if move.captured and move.captured[1]=='R':
            cr, cc = move.end
            if cr==7 and cc==0: self.castling_rights['wQ']=False
            if cr==7 and cc==7: self.castling_rights['wK']=False
            if cr==0 and cc==0: self.castling_rights['bQ']=False
            if cr==0 and cc==7: self.castling_rights['bK']=False
       
        self.en_passant_target = None
        if piece[1]=='P' and abs(er - sr) == 2:
            self.en_passant_target = ((sr+er)//2, sc)
       
        if piece[1]=='P' or move.captured:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
       
        self.white_to_move = not self.white_to_move
        if not self.white_to_move: self.fullmove_number += 1
        self.move_history.append((move, snapshot))
        return snapshot

    def _unmake_move_internal(self, snapshot):
        self.board = [row[:] for row in snapshot['board']]
        self.white_to_move = snapshot['white_to_move']
        self.castling_rights = snapshot['castling_rights'].copy()
        self.en_passant_target = snapshot['en_passant_target']
        self.halfmove_clock = snapshot['halfmove_clock']
        self.fullmove_number = snapshot['fullmove_number']
        if self.move_history: self.move_history.pop()

    def make_move(self, move):
        self._make_move_internal(move)

    def undo(self):
        if not self.move_history: return False
        move, snapshot = self.move_history[-1]
        self._unmake_move_internal(snapshot)
        return True

    def find_king(self, side):
        target = (side=='w') and 'wK' or 'bK'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target: return (r,c)
        return None

    def is_in_check(self, color):
        side = 'w' if color in ('w','white') else 'b'
        krkc = self.find_king(side)
        if not krkc: return False
        kr,kc = krkc
        saved = self.white_to_move
        self.white_to_move = not (side=='w')
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p[0] != side:
                    for m in self._moves_for_piece(r,c,p):
                        if m.end == (kr,kc):
                            self.white_to_move = saved
                            return True
        self.white_to_move = saved
        return False

    def is_checkmate(self):
        side = 'w' if self.white_to_move else 'b'
        if self.is_in_check(side) and len(self.generate_moves())==0: return True
        return False

    def is_stalemate(self):
        side = 'w' if self.white_to_move else 'b'
        if not self.is_in_check(side) and len(self.generate_moves())==0: return True
        return False

    def material_score(self):
        vals = {'K':0,'Q':9,'R':5,'B':3,'N':3,'P':1}
        total = 0
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p:
                    v = vals.get(p[1],0)
                    total += v if p[0]=='w' else -v
        return total


def evaluate(board: Board):
    
    mat = board.material_score()
    mobility = len(board.generate_moves()) * (1 if board.white_to_move else -1)
    return mat + 0.01 * mobility

def minimax(board: Board, depth, alpha, beta, maximizing, start_time=None, time_limit=None):
    if depth==0 or board.is_checkmate() or board.is_stalemate():
        return evaluate(board), None
    best_move = None
    moves = board.generate_moves()
    if not moves: return evaluate(board), None
    if maximizing:
        max_eval = -math.inf
        for m in moves:
            snap = board._make_move_internal(m)
            val, _ = minimax(board, depth-1, alpha, beta, False, start_time, time_limit)
            board._unmake_move_internal(snap)
            if val > max_eval:
                max_eval = val; best_move = m
            alpha = max(alpha, val)
            if beta <= alpha: break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for m in moves:
            snap = board._make_move_internal(m)
            val, _ = minimax(board, depth-1, alpha, beta, True, start_time, time_limit)
            board._unmake_move_internal(snap)
            if val < min_eval:
                min_eval = val; best_move = m
            beta = min(beta, val)
            if beta <= alpha: break
        return min_eval, best_move

def find_best_move(board: Board, depth=AI_DEPTH):
    _, move = minimax(board, depth, -math.inf, math.inf, not board.white_to_move)
    return move


PIECES_IMG = {}
USE_IMAGES = True
def load_images():
    global USE_IMAGES
    names = ['wp','wr','wn','wb','wq','wk','bp','br','bn','bb','bq','bk']
    try:
        for n in names:
            p = os.path.join(ASSETS_DIR, f"{n}.png")
            img = pygame.image.load(p).convert_alpha()
            PIECES_IMG[n] = pygame.transform.smoothscale(img, (SQUARE, SQUARE))
    except Exception as e:
        USE_IMAGES = False
        print("Assets missing or failed to load; using Unicode fallback.", e)

load_images()

FILES = "abcdefgh"
def rc_to_alg(r,c): return f"{FILES[c]}{8-r}"

def move_to_text(m: Move):
    s = f"{rc_to_alg(*m.start)}{rc_to_alg(*m.end)}"
    if m.promotion: s += f"={m.promotion}"
    return s

def draw_piece_at(piece, pos):
    if not piece: return
    if USE_IMAGES:
        key = piece.lower()
        if key in PIECES_IMG:
            screen.blit(PIECES_IMG[key], pos); return
    ch = UNICODE.get(piece, '?')
    text = BIG.render(ch, True, (0,0,0))
    screen.blit(text, pos)

def draw_board(board_obj, selected=None, possible_moves=None, hint_move=None, last_move=None):
    ox, oy = BOARD_ORIGIN
    
    for r in range(8):
        for c in range(8):
            color = LIGHT if (r+c)%2==0 else DARK
            pygame.draw.rect(screen, color, (ox+c*SQUARE, oy+r*SQUARE, SQUARE, SQUARE))
    
    if last_move:
        for (rr,cc) in [last_move.start, last_move.end]:
            pygame.draw.rect(screen, LASTMOVE, (ox+cc*SQUARE, oy+rr*SQUARE, SQUARE, SQUARE))
   
    if hint_move:
        sr, sc, er, ec = hint_move
        pygame.draw.rect(screen, HINTCOLOR, (ox+sc*SQUARE, oy+sr*SQUARE, SQUARE, SQUARE), 4)
        pygame.draw.rect(screen, HINTCOLOR, (ox+ec*SQUARE, oy+er*SQUARE, SQUARE, SQUARE), 4)
    
    if selected:
        r,c = selected
        pygame.draw.rect(screen, HIGHLIGHT, (ox + c*SQUARE, oy + r*SQUARE, SQUARE, SQUARE), 4)
    if possible_moves:
        for (r,c) in possible_moves:
            center = (ox + c*SQUARE + SQUARE//2, oy + r*SQUARE + SQUARE//2)
            pygame.draw.circle(screen, HIGHLIGHT, center, 9)
    
    for r in range(8):
        for c in range(8):
            p = board_obj.piece_at(r,c)
            if p:
                draw_piece_at(p, (ox + c*SQUARE, oy + r*SQUARE))
    
    pygame.draw.rect(screen, BLACK, (ox-2, oy-2, SQUARE*8+4, SQUARE*8+4), 2)
    for c in range(8):
        t = SMALL.render(FILES[c], True, TEXT)
        screen.blit(t, (ox + c*SQUARE + 4, oy + 8*SQUARE + 2))
    for r in range(8):
        t = SMALL.render(str(8-r), True, TEXT)
        screen.blit(t, (ox - 16, oy + r*SQUARE + 6))

def draw_sidebar(board_obj, move_texts, captured, score, move_count, status):
    sx = BOARD_SIZE + 40
    pygame.draw.rect(screen, SIDEBAR_BG, (sx-20, 10, SIDEBAR_W, HEIGHT-20))
    screen.blit(BIG.render("Game", True, TEXT), (sx, 14))
    screen.blit(FONT.render(status, True, TEXT), (sx, 44))
    screen.blit(FONT.render(f"Score: {score:+.2f}", True, TEXT), (sx, 72))
    screen.blit(FONT.render(f"Moves: {move_count}", True, TEXT), (sx, 96))
 
    btns = [("New Game (N)", (sx, 130, 160, 28)), ("Undo (U)", (sx+170, 130, 160, 28)),
            ("Hint (H)", (sx, 170, 160, 28)), ("Toggle AI (A)", (sx+170, 170, 160, 28))]
    for label, rect in btns:
        pygame.draw.rect(screen, BUTTON_BG, rect)
        screen.blit(FONT.render(label, True, TEXT), (rect[0]+8, rect[1]+7))
    
    screen.blit(BIG.render("Moves", True, TEXT), (sx, 210))
    ml_rect = pygame.Rect(sx, 240, SIDEBAR_W-40, 220)
    pygame.draw.rect(screen, (250,250,255), ml_rect)
    pygame.draw.rect(screen, (200,200,210), ml_rect, 1)
    y = 246
    for i in range(0, len(move_texts), 2):
        w = move_texts[i]
        b = move_texts[i+1] if i+1 < len(move_texts) else ""
        idx = i//2 + 1
        screen.blit(FONT.render(f"{idx}. {w}", True, TEXT), (sx+6, y))
        if b:
            screen.blit(FONT.render(b, True, TEXT), (sx + 140, y))
        y += 18
        if y > ml_rect.bottom - 18: break
    
    screen.blit(BIG.render("Captured", True, TEXT), (sx, 480))
    screen.blit(FONT.render("White lost:", True, TEXT), (sx, 512))
    screen.blit(FONT.render("Black lost:", True, TEXT), (sx, 560))
    
    wx, bx = sx+100, sx+100
    for i, p in enumerate(captured.get('w',[])):
        draw_small(p, (wx + i*18, 508))
    for i, p in enumerate(captured.get('b',[])):
        draw_small(p, (bx + i*18, 556))

def draw_small(p, pos):
    if not p: return
    if USE_IMAGES:
        key = p.lower()
        if key in PIECES_IMG:
            img = pygame.transform.smoothscale(PIECES_IMG[key], (16,16))
            screen.blit(img, pos); return
    ch = UNICODE.get(p, '?')
    screen.blit(SMALL.render(ch, True, TEXT), pos)


def lerp(a,b,t): return a + (b-a)*t
def animate_move(board_obj, move_obj, speed=0.35):
    sr, sc = move_obj.start; er, ec = move_obj.end
    piece = board_obj.board[sr][sc]
    start = (BOARD_ORIGIN[0] + sc*SQUARE, BOARD_ORIGIN[1] + sr*SQUARE)
    end = (BOARD_ORIGIN[0] + ec*SQUARE, BOARD_ORIGIN[1] + er*SQUARE)
    frames = max(6, int(FPS * speed))
    
    temp_board = copy.deepcopy(board_obj)
    temp_board.board[sr][sc] = ''
    for f in range(frames):
        t = (f+1)/frames
        screen.fill(WHITE)
        draw_board(temp_board, last_move=move_obj)  
        x = lerp(start[0], end[0], t); y = lerp(start[1], end[1], t)
        draw_piece_at(piece, (x,y))
        draw_sidebar(temp_board, [], {}, temp_board.material_score(), len(temp_board.move_history), "")
        pygame.display.flip()
        clock.tick(FPS)


def main():
    board = Board()
    selected = None
    possible_moves = []
    last_move = None
    hint_move = None
    ai_enabled = True
    ai_depth = AI_DEPTH
    status = "White to move"

    while True:
        score = board.material_score()
        move_texts = [move_to_text(m) for m,_ in board.move_history]
        captured = {'w':[], 'b':[]}
        for m,_ in board.move_history:
            if m.captured:
                captured.setdefault(m.captured[0], []).append(m.captured)
        move_count = len(board.move_history)

        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx,my = pygame.mouse.get_pos()
                sx = BOARD_SIZE + 40
              
                if sx <= mx <= sx+160 and 130 <= my <= 158:
                    board = Board(); selected=None; possible_moves=[]; last_move=None; hint_move=None
                if sx+170 <= mx <= sx+330 and 130 <= my <= 158:
                    board.undo(); last_move=None
                if sx <= mx <= sx+160 and 170 <= my <= 198:
                    mv = find_best_move(board, depth=1)
                    if mv:
                        hint_move = (mv.start[0], mv.start[1], mv.end[0], mv.end[1])
                if sx+170 <= mx <= sx+330 and 170 <= my <= 198:
                    ai_enabled = not ai_enabled
                
                ox, oy = BOARD_ORIGIN
                if ox <= mx <= ox+8*SQUARE and oy <= my <= oy+8*SQUARE:
                    c = (mx - ox)//SQUARE; r = (my - oy)//SQUARE
                    p = board.piece_at(r,c)
                    if selected and (r,c) in possible_moves:
                        
                        chosen = [m for m in board.generate_moves() if m.start==(selected[0], selected[1]) and m.end==(r,c)]
                        if chosen:
                            move_obj = chosen[0]
                            animate_move(board, move_obj)
                            board.make_move(move_obj)
                            last_move = move_obj
                            selected=None; possible_moves=[]; hint_move=None
                        else:
                            selected=None; possible_moves=[]
                    else:
                       
                        if p and ((p[0]=='w') == board.white_to_move):
                            selected = (r,c)
                            possible_moves = [m.end for m in board.generate_moves() if m.start==(r,c)]
                        else:
                            selected=None; possible_moves=[]
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_u:
                    board.undo(); last_move=None
                if ev.key == pygame.K_n:
                    board = Board(); selected=None; possible_moves=[]; last_move=None; hint_move=None
                if ev.key == pygame.K_h:
                    mv = find_best_move(board, depth=1)
                    if mv:
                        hint_move = (mv.start[0], mv.start[1], mv.end[0], mv.end[1])
                if ev.key == pygame.K_a:
                    ai_enabled = not ai_enabled

        
        if ai_enabled and not board.white_to_move:
            
            pygame.time.delay(180)
            mv = find_best_move(board, depth=ai_depth)
            if mv:
                animate_move(board, mv)
                board.make_move(mv)
                last_move = mv
                hint_move = None

        
        screen.fill(WHITE)
        draw_board(board, selected, possible_moves, hint_move, last_move)
        status = "White to move" if board.white_to_move else "Black to move"
        draw_sidebar(board, move_texts, captured, score, move_count, status)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
