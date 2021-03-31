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
	pygame.key.set_repeat() # no args intentionally
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
		dt = clock.tick(C.FPS) / 1000
		keys = pygame.key.get_pressed()
		sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
		kx, ky = 0, 0

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if not sprinting and event.type == pygame.KEYDOWN:
				if event.key in (pygame.K_w, pygame.K_UP):
					ky -= 1
				elif event.key in (pygame.K_s, pygame.K_DOWN):
					ky += 1
				elif event.key in (pygame.K_a, pygame.K_LEFT):
					kx -= 1
				elif event.key in (pygame.K_d, pygame.K_RIGHT):
					kx += 1

		if sprinting:
			if keys[pygame.K_w] or keys[pygame.K_UP]:
				ky -= 1
			if keys[pygame.K_s] or keys[pygame.K_DOWN]:
				ky += 1
			if keys[pygame.K_a] or keys[pygame.K_LEFT]:
				kx -= 1
			if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
				kx += 1

		player.update(dt, kx, ky)
		level.move(player)

		draw_game()

	exit_game()

def run_game_subdir(change_dir='../'):
	os.chdir(change_dir)
	run_game()

if __name__ == "__main__":
	run_game_subdir()