import os
import pygame
import random

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

def clamp(n, n_max, n_min=0):
	return min(max(n, n_min), n_max)

if __name__ == "__main__":
	import code.game
	code.game.run_game()