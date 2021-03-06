import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from code.player import Player
from code.level import Level
from code.constants import C
from code.helpers import *
from datetime import datetime

screen: pygame.Surface
player: Player
level: Level
start_level = f'{C.START_LEVEL:02d}.txt'
level_file = start_level
sandbox = 'sandbox.txt'
won = last_won = permanent_won = False
muted = False
show_info = True
started = not start_level.startswith('01')

def init_game():
	global screen, player, level, level_file
	pygame.init()
	pygame.display.set_caption(C.SCREEN_TITLE)
	pygame.key.set_repeat() # no args intentionally
	screen = pygame.display.set_mode(C.SCREEN_SIZE)
	player = Player()
	load_level(level_file)
	pygame.mixer.music.load(C.MUSIC)
	pygame.mixer.music.set_volume(C.VOLUME)
	pygame.mixer.music.play(-1)

def advance_level_file():
	global level_file
	if level_file != sandbox:
		num = int(level_file[:-4]) + 1
		level_file = f'{num:02d}.txt'
		if not asset_path(level_file, 'levels'):
			level_file = sandbox

def exit_game():
	pygame.quit()
	print(f"Ended game at {datetime.now()}")
	sys.exit()

def draw_game():
	screen.fill(C.GRASS_COLOR)
	level.draw(screen)
	player.draw(screen)

	if show_info:
		for y, line in enumerate(C.INFO):
			info = C.INFO_FONT.render(line, True, C.LEVEL_TEXT_COLOR)
			screen.blit(info, (C.INFO_OFFSET, y * C.INFO_HEIGHT))

	pygame.display.update()

def load_level(filename):
	global level, won, last_won, permanent_won
	level = Level(filename, player)
	player.change_level(level)
	won = last_won = permanent_won = False
	player.move_count = 0

def run_game():
	print(f"Started game at {datetime.now()}")

	global won, last_won, permanent_won, muted, show_info, level_file, started
	init_game()
	clock = pygame.time.Clock()
	running = True

	while running:

		dt = clock.tick(C.FPS) / 1000
		keys = pygame.key.get_pressed()
		sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
		kx, ky = 0, 0
		pulling = keys[pygame.K_SPACE]
		corners = [False] * 4

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					load_level(level_file)  # reload level
				elif event.key == pygame.K_m:
					pygame.mixer.music.set_volume(C.VOLUME if muted else 0)
					muted = not muted
				elif event.key == pygame.K_i:
					show_info = not show_info
				elif event.key in (pygame.K_r, pygame.K_F5):
					level.start_exec()
				elif event.key in (pygame.K_1, pygame.K_KP1):
					corners[0] = True
				elif event.key in (pygame.K_2, pygame.K_KP2):
					corners[1] = True
				elif event.key in (pygame.K_3, pygame.K_KP3):
					corners[2] = True
				elif event.key in (pygame.K_4, pygame.K_KP4):
					corners[3] = True

				enter_hit = event.key in (pygame.K_RETURN, pygame.K_KP_ENTER)

				skip_level = event.key == pygame.K_F10
				if skip_level or permanent_won and enter_hit:
					if not started:
						started = True
					else:
						advance_level_file()
						load_level(level_file)

				skip_to_sandbox = event.key == pygame.K_F12
				if skip_to_sandbox:
					level_file = sandbox
					load_level(level_file)

				restart_game = event.key == pygame.K_F9
				if restart_game:
					level_file = start_level
					load_level(level_file)
					started = False

				if not started and enter_hit or skip_to_sandbox:
					started = True

				if not sprinting:
					if event.key in (pygame.K_w, pygame.K_UP):
						ky -= 1
					elif event.key in (pygame.K_s, pygame.K_DOWN):
						ky += 1
					elif event.key in (pygame.K_a, pygame.K_LEFT):
						kx -= 1
					elif event.key in (pygame.K_d, pygame.K_RIGHT):
						kx += 1

		if not started:
			screen.blit(C.MENU_IMG, (0, 0))
			pygame.display.update()
			continue

		if sprinting:
			if keys[pygame.K_w] or keys[pygame.K_UP]:
				ky -= 1
			if keys[pygame.K_s] or keys[pygame.K_DOWN]:
				ky += 1
			if keys[pygame.K_a] or keys[pygame.K_LEFT]:
				kx -= 1
			if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
				kx += 1

		last_won = won or permanent_won
		won = player.update(dt, kx, ky, pulling)
		level.update(corners)
		draw_game()

		if not last_won and won and level_file != sandbox:
			if not muted:
				pygame.mixer.Sound.play(C.SUCCESS)
			permanent_won = True
			message = f"You escaped level {level.filename} in {player.move_count} moves!"
			level.set_message(f"{message} Press enter to continue...")
			print(message)

	exit_game()

if __name__ == "__main__":
	run_game()