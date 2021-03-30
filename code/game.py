import pygame
from code import *

def init_game():
	# noinspection PyGlobalUndefined
	global screen, player
	pygame.init()
	pygame.display.set_caption(C.SCREEN_TITLE)
	screen = pygame.display.set_mode(C.SCREEN_SIZE)
	player = Player()

def exit_game():
	pygame.quit()

def draw_game():
	screen.fill(C.GRASS_COLOR)
	player.draw(screen)
	pygame.display.update()

def run_game():
	init_game()
	running = True
	clock = pygame.time.Clock()

	while running:
		clock.tick(C.FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_w] or pressed[pygame.K_UP]:
			player.rotate(C.NORTH)
		if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
			player.rotate(C.SOUTH)
		if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
			player.rotate(C.EAST)
		if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
			player.rotate(C.WEST)

		draw_game()

	exit_game()