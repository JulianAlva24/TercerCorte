import pygame
import random
import sys
import copy

# Inicializar pygame
pygame.init()

# Constantes
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 300  # Espacio extra para UI
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 100

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Colores de las piezas
PIECE_COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

# Formas de las piezas de Tetris (matrices 4x4)
PIECES = [
    # I-piece
    [
        ['.....',
         '..#..',
         '..#..',
         '..#..',
         '..#..'],
        ['.....',
         '.....',
         '####.',
         '.....',
         '.....']
    ],
    # O-piece
    [
        ['.....',
         '.....',
         '.##..',
         '.##..',
         '.....']
    ],
    # T-piece
    [
        ['.....',
         '.....',
         '.#...',
         '##...',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '.#...'],
        ['.....',
         '.....',
         '.#...',
         '.##..',
         '.#...'],
        ['.....',
         '.....',
         '.#...',
         '###..',
         '.....']
    ],
    # S-piece
    [
        ['.....',
         '.....',
         '.##..',
         '##...',
         '.....'],
        ['.....',
         '.....',
         '.#...',
         '.##..',
         '..#..']
    ],
    # Z-piece
    [
        ['.....',
         '.....',
         '##...',
         '.##..',
         '.....'],
        ['.....',
         '.....',
         '..#..',
         '.##..',
         '.#...']
    ],
    # J-piece
    [
        ['.....',
         '.....',
         '.#...',
         '.#...',
         '##...'],
        ['.....',
         '.....',
         '.....',
         '#....',
         '###..'],
        ['.....',
         '.....',
         '.##..',
         '.#...',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '..#..']
    ],
    # L-piece
    [
        ['.....',
         '.....',
         '.#...',
         '.#...',
         '.##..'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '#....'],
        ['.....',
         '.....',
         '##...',
         '.#...',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '..#..',
         '###..']
    ]
]

class Piece:
    """Clase para las piezas de Tetris"""
    def __init__(self, piece_type=None):
        if piece_type is None:
            self.type = random.randint(0, len(PIECES) - 1)
        else:
            self.type = piece_type
        
        self.color = PIECE_COLORS[self.type]
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0
        self.rotation = 0
        self.shape = PIECES[self.type][self.rotation]
    
    def get_rotated_shape(self, rotation=None):
        """Obtiene la forma de la pieza en una rotación específica"""
        if rotation is None:
            rotation = self.rotation
        return PIECES[self.type][rotation % len(PIECES[self.type])]
    
    def rotate(self):
        """Rota la pieza"""
        new_rotation = (self.rotation + 1) % len(PIECES[self.type])
        return new_rotation
    
    def get_cells(self, x=None, y=None, rotation=None):
        """Obtiene las celdas ocupadas por la pieza"""
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if rotation is None:
            shape = self.shape
        else:
            shape = self.get_rotated_shape(rotation)
        
        cells = []
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    cells.append((x + col_idx, y + row_idx))
        return cells

class TetrisGame:
    """Clase principal del juego de Tetris"""
    def __init__(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  # millisegundos
        self.game_over = False
        self.paused = False
        
        # Crear ventana
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def is_valid_position(self, piece, x=None, y=None, rotation=None):
        """Verifica si una posición es válida para la pieza"""
        cells = piece.get_cells(x, y, rotation)
        
        for cell_x, cell_y in cells:
            # Verificar límites
            if cell_x < 0 or cell_x >= GRID_WIDTH or cell_y >= GRID_HEIGHT:
                return False
            
            # Verificar colisión con piezas colocadas (solo si y >= 0)
            if cell_y >= 0 and self.grid[cell_y][cell_x] != BLACK:
                return False
        
        return True
    
    def place_piece(self):
        """Coloca la pieza actual en el grid"""
        cells = self.current_piece.get_cells()
        
        for cell_x, cell_y in cells:
            if cell_y >= 0:  # Solo colocar celdas visibles
                self.grid[cell_y][cell_x] = self.current_piece.color
        
        # Verificar líneas completas
        self.clear_lines()
        
        # Nueva pieza
        self.current_piece = self.next_piece
        self.next_piece = Piece()
        
        # Verificar game over
        if not self.is_valid_position(self.current_piece):
            self.game_over = True
    
    def clear_lines(self):
        """Elimina las líneas completas"""
        lines_to_clear = []
        
        for y in range(GRID_HEIGHT):
            if all(cell != BLACK for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        # Eliminar líneas y agregar nuevas arriba
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        
        # Actualizar puntuación
        if lines_to_clear:
            lines_count = len(lines_to_clear)
            self.lines_cleared += lines_count
            
            # Puntuación según líneas eliminadas
            points = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += points.get(lines_count, 0) * self.level
            
            # Aumentar nivel cada 10 líneas
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
    
    def move_piece(self, dx, dy):
        """Mueve la pieza si es posible"""
        new_x = self.current_piece.x + dx
        new_y = self.current_piece.y + dy
        
        if self.is_valid_position(self.current_piece, new_x, new_y):
            self.current_piece.x = new_x
            self.current_piece.y = new_y
            return True
        return False
    
    def rotate_piece(self):
        """Rota la pieza si es posible"""
        new_rotation = self.current_piece.rotate()
        
        if self.is_valid_position(self.current_piece, rotation=new_rotation):
            self.current_piece.rotation = new_rotation
            self.current_piece.shape = self.current_piece.get_rotated_shape()
            return True
        return False
    
    def hard_drop(self):
        """Hace caer la pieza hasta abajo"""
        while self.move_piece(0, 1):
            self.score += 2  # Puntos por hard drop
        self.place_piece()
    
    def update(self, dt):
        """Actualiza el estado del juego"""
        if self.game_over or self.paused:
            return
        
        self.fall_time += dt
        
        if self.fall_time >= self.fall_speed:
            if not self.move_piece(0, 1):
                self.place_piece()
            self.fall_time = 0
    
    def draw_grid(self):
        """Dibuja el grid del juego"""
        # Dibujar celdas ocupadas
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, self.grid[y][x], rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
        
        # Dibujar pieza actual
        if not self.game_over:
            cells = self.current_piece.get_cells()
            for cell_x, cell_y in cells:
                if 0 <= cell_x < GRID_WIDTH and cell_y >= 0:
                    rect = pygame.Rect(cell_x * CELL_SIZE, cell_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, self.current_piece.color, rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def draw_next_piece(self):
        """Dibuja la siguiente pieza"""
        start_x = GRID_WIDTH * CELL_SIZE + 20
        start_y = 50
        
        # Título
        text = self.font.render("Siguiente:", True, WHITE)
        self.screen.blit(text, (start_x, start_y - 30))
        
        # Pieza
        shape = self.next_piece.shape
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    rect = pygame.Rect(
                        start_x + col_idx * 20,
                        start_y + row_idx * 20,
                        20, 20
                    )
                    pygame.draw.rect(self.screen, self.next_piece.color, rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def draw_ui(self):
        """Dibuja la interfaz de usuario"""
        start_x = GRID_WIDTH * CELL_SIZE + 20
        start_y = 200
        
        # Puntuación
        score_text = self.font.render(f"Puntos: {self.score}", True, WHITE)
        self.screen.blit(score_text, (start_x, start_y))
        
        # Nivel
        level_text = self.font.render(f"Nivel: {self.level}", True, WHITE)
        self.screen.blit(level_text, (start_x, start_y + 40))
        
        # Líneas
        lines_text = self.font.render(f"Líneas: {self.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (start_x, start_y + 80))
        
        # Controles
        controls_y = start_y + 150
        controls = [
            "Controles:",
            "A/D - Mover",
            "S - Caída rápida",
            "W - Rotar",
            "Espacio - Drop",
            "P - Pausa",
            "R - Reiniciar"
        ]
        
        for i, control in enumerate(controls):
            font = self.font if i == 0 else self.small_font
            color = WHITE if i == 0 else GRAY
            text = font.render(control, True, color)
            self.screen.blit(text, (start_x, controls_y + i * 25))
    
    def draw_game_over(self):
        """Dibuja la pantalla de game over"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Texto de game over
        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Puntuación Final: {self.score}", True, WHITE)
        restart_text = self.small_font.render("Presiona R para reiniciar", True, WHITE)
        
        # Centrar textos
        go_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
        
        self.screen.blit(game_over_text, go_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def draw_pause(self):
        """Dibuja la pantalla de pausa"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("PAUSADO", True, YELLOW)
        continue_text = self.small_font.render("Presiona P para continuar", True, WHITE)
        
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 25))
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 25))
        
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(continue_text, continue_rect)
    
    def reset_game(self):
        """Reinicia el juego"""
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500
        self.game_over = False
        self.paused = False
    
    def handle_events(self):
        """Maneja los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                
                elif not self.game_over and not self.paused:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                    
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                    
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if self.move_piece(0, 1):
                            self.score += 1
                    
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.rotate_piece()
                    
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
        
        return True
    
    def run(self):
        """Bucle principal del juego"""
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            running = self.handle_events()
            self.update(dt)
            
            # Dibujar
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_next_piece()
            self.draw_ui()
            
            if self.game_over:
                self.draw_game_over()
            elif self.paused:
                self.draw_pause()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    game = TetrisGame()
    game.run()
