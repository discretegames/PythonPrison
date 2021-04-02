import os
import pygame

def asset_path(filename, folder='assets'):
	path = os.path.join(folder, filename)
	if not os.path.exists(path): # Check parent directory as we may be executing from code folder.
		path = os.path.join(os.pardir, path)
	return path

def load_image(name, resize=None):
	image = pygame.image.load(asset_path(f'{name}.png'))
	if resize is None:
		return image
	if isinstance(resize, int):
		resize = resize, resize
	return pygame.transform.smoothscale(image, resize)

def center1D(smaller, bigger):
	return (bigger - smaller) // 2

def center2D(smaller, bigger):
	return center1D(smaller[0], bigger[0]), center1D(smaller[1], bigger[1])

def order(n1, n2): # sorted works but this seems more efficient
	if n1 < n2:
		return n1, n2
	return n2, n1

def clamp(n, n_max, n_min=0):
	return min(max(n, n_min), n_max)

# Constants
class C:
	pygame.init() # Initialize pygame so constant fonts and such can be created.
	SCREEN_TITLE = 'PyWeek31 Entry - by discretegames'
	SCREEN_SIZE = 1920, 1080 # 1600, 900
	SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
	FPS = 60
	GRID_SCALE = 40
	GRID_SIZE = GRID_SCALE, GRID_SCALE
	PLAYER_SPEED = 30
	EXEC_TIME_LIMIT = 1
	NORTH = 0
	SOUTH = 180
	WEST = 90
	EAST = 270
	LEVEL_COLOR = 100, 100, 100
	EXEC_REGION_COLOR = 100, 100, 160
	OUT_REGION_COLOR = 160, 100, 100
	REGION_RECT_RADIUS = 10
	CHAR_TEXT_COLOR = 220, 220, 220
	LOCKED_CHAR_TEXT_COLOR = 180, 180, 180
	PLAYER_IMG = load_image('player', GRID_SCALE)
	WALL_IMG = load_image('wall', GRID_SCALE)
	CHAR_IMG = load_image('char', GRID_SCALE)
	LOCKED_CHAR_IMG = load_image('locked', GRID_SCALE)
	BACKGROUND_IMG = load_image('background', SCREEN_SIZE)
	CHAR_FONT = pygame.font.Font(asset_path('OxygenMono.ttf'), GRID_SCALE - 8)
	CODE_HEADER = 'open=None;p=print;r=range;\n'

if __name__ == "__main__":
	import code.game
	code.game.run_game()