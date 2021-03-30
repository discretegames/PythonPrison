import os
import pygame
from code.constants import *

def asset_path(filename, ext=''):
	if ext and not ext.startswith('.'):
		ext = f'.{ext}'
	return os.path.join('assets', f'{filename}{ext}')

def load_image(name, resize=C.GRID_SIZE):
	image = pygame.image.load(asset_path(name, 'png'))
	w, h = image.get_rect().size
	return pygame.transform.smoothscale(image, (resize, resize))

def center(bigger, smaller=C.GRID_SIZE):
	return (bigger - smaller) // 2

if __name__ == "__main__":
	import code.game
	code.game.run_game_subdir()