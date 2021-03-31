import pygame
from code.constants import *
from code.helpers import *
from code.player import *
from code.level import *

def init_game():
	# noinspection PyGlobalUndefined
	global screen, player, level
	pygame.init()
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

	# TODO shift to sprint with both movement types
	move_method = False

	while running:
		dt = clock.tick(C.FPS) / 1000
		dx, dy = 0, 0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN and move_method:
				if event.key in (pygame.K_w, pygame.K_UP):
					dy -= 1
				elif event.key in (pygame.K_s, pygame.K_DOWN):
					dy += 1
				elif event.key in (pygame.K_a, pygame.K_LEFT):
					dx -= 1
				elif event.key in (pygame.K_d, pygame.K_RIGHT):
					dx += 1

		if not move_method:
			dx, dy = 0, 0
			keys = pygame.key.get_pressed()
			if keys[pygame.K_w] or keys[pygame.K_UP]:
				dy -= 1
			if keys[pygame.K_s] or keys[pygame.K_DOWN]:
				dy += 1
			if keys[pygame.K_a] or keys[pygame.K_LEFT]:
				dx -= 1
			if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
				dx += 1

		# -stepped diagonal movement would be nice

		player.update(dt, dx, dy)
		level.move(player)

		draw_game()

	exit_game()

def run_game_subdir(change_dir='../'):
	os.chdir(change_dir)
	run_game()

if __name__ == "__main__":
	run_game_subdir()