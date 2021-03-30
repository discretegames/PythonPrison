class C:
	SCREEN_TITLE = 'PyWeek31 Entry - by discretegames'
	SCREEN_SIZE = 1920, 1080
	SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE
	GRID_SIZE = 32
	FPS = 60
	GRASS_COLOR = 120, 200, 70
	LEVEL_COLOR = 60, 60, 60
	NORTH = 0
	SOUTH = 180
	WEST = 90
	EAST = 270
	PLAYER_SPEED = 40

if __name__ == "__main__":
	import code.game
	code.game.run_game_subdir()