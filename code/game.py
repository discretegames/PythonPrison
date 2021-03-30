import pygame
from code.constants import *
from code.helpers import *
from code.player import *
from code.level import *

def init_game():
	# noinspection PyGlobalUndefined
	global screen, player, level
	pygame.init()
	pygame.key.set_repeat(100, 50)
	pygame.display.set_caption(C.SCREEN_TITLE)
	screen = pygame.display.set_mode(C.SCREEN_SIZE)
	player = Player()
	level = Level(player)

def exit_game():
	pygame.quit()

def draw_game():
	screen.fill(C.GRASS_COLOR)
	level.draw(screen)
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
			if event.type == pygame.KEYDOWN:
				if event.key in (pygame.K_w, pygame.K_UP):
					player.rotate(C.NORTH)
					player.y -= 1
					level.move(player)
				if event.key in (pygame.K_s, pygame.K_DOWN):
					player.rotate(C.SOUTH)
					player.y += 1
					level.move(player)
				if event.key in (pygame.K_a, pygame.K_LEFT):
					player.rotate(C.EAST)
					player.x -= 1
					level.move(player)
				if event.key in (pygame.K_d, pygame.K_RIGHT):
					player.rotate(C.WEST)
					player.x += 1
					level.move(player)
		draw_game()

	exit_game()

if __name__ == "__main__":
	os.chdir('../')
	run_game()