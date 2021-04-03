from code.helpers import *

class C:
	pygame.init()  # Initialize pygame so constant fonts and such can be created. Unrelated to welcome message replay.
	SCREEN_TITLE = 'Python Prison - PyWeek31 entry by discretegames'
	SCREEN_SIZE = 1600, 900
	SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE

	FPS = 60
	GRID_SCALE = 32
	GRID_SIZE = GRID_SCALE, GRID_SCALE
	PLAYER_SPEED = 30
	EXEC_TIME_LIMIT = 2

	NORTH = 0
	SOUTH = 180
	WEST = 90
	EAST = 270

	CHAR_FONT = pygame.font.Font(asset_path('OxygenMono.ttf'), int(.75 * GRID_SCALE))
	COP_FONT = pygame.font.Font(asset_path('OxygenMono.ttf'), int(.5 * GRID_SCALE))
	COP_FONT_OFFSET = int(.5 * GRID_SCALE), int(.26 * GRID_SCALE)
	LEVEL_TITLE_FONT = pygame.font.Font(asset_path('SimpleSlum.ttf'), 44)
	MESSAGE_FONT = pygame.font.Font(asset_path('SimpleSlum.ttf'), 32)
	FONT_VERT_OFFSET = 4

	GRASS_COLOR = 75, 145, 45

	LEVEL_BG_COLOR = 115, 113, 109 # good
	LEVEL_BORDER_COLOR = 79, 78, 77 # good
	LEVEL_TEXT_COLOR = 252, 252, 250 # good
	LEVEL_BORDER = 4

	CHAR_TEXT_COLOR = 253, 253, 253 # good
	LOCKED_TEXT_COLOR = 190, 190, 190 # good
	COP_TEXT_COLOR = 61, 44, 9

	EXEC_REGION_COLOR = 96, 163, 230 # good
	OUT_REGION_COLOR = 227, 98, 117 # good
	EXEC_LOCKED_COLOR = 48, 81, 115 # good
	OUT_LOCKED_COLOR = 153, 66, 79 # good
	REGION_RECT_RADIUS = 10

	PLAYER_IMG = load_image('player', GRID_SCALE)
	WALL_IMG = load_image('wall', GRID_SCALE)
	FENCE_IMG = load_image('fence', GRID_SCALE)
	CHAR_IMG = load_image('char', GRID_SCALE)
	DOOR_IMG = load_image('door', GRID_SCALE)
	GATE_IMG = load_image('gate', GRID_SCALE)
	COP_IMG = load_image('cop', GRID_SCALE)
	LOCKED_CHAR_IMG = load_image('locked', GRID_SCALE)
	CODE_HEADER = 'global p,r;open=None;p=print;r=range;\n'

	MUSIC = asset_path('music.wav')
	VOLUME = 0.5
	SUCCESS = pygame.mixer.Sound(asset_path('success.wav'))

	INFO_OFFSET = 4
	INFO_HEIGHT = 16
	INFO_FONT = pygame.font.Font(asset_path('PTSans.ttf'), INFO_HEIGHT - 2)
	INFO = """WASD/Arrows = move
Shift = sprint
Space = pull
12 = set execution area
34 = set output area
R = run execution area
Esc = reload level
M = toggle mute
I = toggle info""".split('\n')

if __name__ == "__main__":
	import code.game
	code.game.run_game()