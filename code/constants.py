from code.helpers import load_image

class C:
	SCREEN_TITLE = 'PyWeek31 Entry - by discretegames'
	SCREEN_SIZE = 1920, 1080
	SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
	GRID_SIZE = 32 # TODO allow this to be dynamic? Same with resolution.
	FPS = 60
	LEVEL_COLOR = 100, 100, 100
	NORTH = 0
	SOUTH = 180
	WEST = 90
	EAST = 270
	PLAYER_SPEED = 30
	PLAYER_IMG = load_image('player', GRID_SIZE)
	WALL_IMG = load_image('wall', GRID_SIZE)
	BACKGROUND_IMG = load_image('background', SCREEN_SIZE)

if __name__ == "__main__":
	import code.game
	code.game.run_game()