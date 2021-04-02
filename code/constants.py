from code.helpers import *

class C:
	pygame.init()  # Initialize pygame so constant fonts and such can be created. Unrelated to welcome message replay.
	SCREEN_TITLE = 'Python Prison - PyWeek31 entry by discretegames'
	SCREEN_SIZE = 1600, 900 # 1920, 1080 # 1600, 900
	SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE

	FPS = 60
	GRID_SCALE = 32
	GRID_SIZE = GRID_SCALE, GRID_SCALE
	PLAYER_SPEED = 30
	EXEC_TIME_LIMIT = 1

	NORTH = 0
	SOUTH = 180
	WEST = 90
	EAST = 270

	CHAR_FONT = pygame.font.Font(asset_path('OxygenMono.ttf'), int(.75 * GRID_SCALE))
	COP_FONT = pygame.font.Font(asset_path('OxygenMono.ttf'), int(.5 * GRID_SCALE))
	COP_FONT_OFFSET = 0, 4
	LEVEL_TITLE_FONT = pygame.font.Font(asset_path('SimpleSlum.ttf'), 32)
	ERROR_FONT = pygame.font.Font(asset_path('OxygenMono.ttf'), 24)
	FONT_VERT_OFFSET = 6

	LEVEL_BG_COLOR = 100, 100, 100
	LEVEL_TEXT_COLOR = 255, 255, 255

	CHAR_TEXT_COLOR = 220, 220, 220
	LOCKED_TEXT_COLOR = 180, 180, 180
	COP_TEXT_COLOR = 0, 0, 0

	EXEC_REGION_COLOR = 100, 100, 160
	EXEC_LOCKED_COLOR = 70, 70, 130
	OUT_REGION_COLOR = 160, 100, 100
	OUT_LOCKED_COLOR = 130, 70, 70
	REGION_RECT_RADIUS = 10

	PLAYER_IMG = load_image('player', GRID_SCALE)
	WALL_IMG = load_image('wall', GRID_SCALE)
	CHAR_IMG = load_image('char', GRID_SCALE)
	DOOR_IMG = load_image('door', GRID_SCALE)
	COP_IMG = load_image('cop', GRID_SCALE)
	LOCKED_CHAR_IMG = load_image('locked', GRID_SCALE)
	BACKGROUND_IMG = load_image('background', SCREEN_SIZE)
	CODE_HEADER = 'open=None;p=print;r=range;\n'

if __name__ == "__main__":
	import code.game
	code.game.run_game()