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

def center(bigger, smaller):
	return (bigger - smaller) // 2

def pos_in_dir(pos, direction):
	x, y = pos
	if direction == C.NORTH:
		y -= 1


# Constants
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