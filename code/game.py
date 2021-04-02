import sys
from code.player import Player
from code.level import Level
from code.helpers import *

screen: pygame.Surface
player: Player
level: Level

def init_game():
	global screen, player, level
	pygame.init()
	pygame.display.set_caption(C.SCREEN_TITLE)
	pygame.key.set_repeat() # no args intentionally
	screen = pygame.display.set_mode(C.SCREEN_SIZE)
	player = Player()
	load_level('testlevel.txt')

def exit_game():
	pygame.quit()
	sys.exit()

def draw_game():
	screen.blit(C.BACKGROUND_IMG, (0, 0))
	level.draw(screen)
	player.draw(screen)
	pygame.display.update()

def load_level(filename):
	global level
	level = Level(filename, player)
	player.change_level(level)

def run_game():
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
					load_level('testlevel.txt')  # reload level
				elif event.key == pygame.K_r:
					level.start_exec()
				elif event.key == pygame.K_1:
					corners[0] = True
				elif event.key == pygame.K_2:
					corners[1] = True
				elif event.key == pygame.K_3:
					corners[2] = True
				elif event.key == pygame.K_4:
					corners[3] = True

				if not sprinting:
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


		player.update(dt, kx, ky, pulling)
		level.update(corners)
		draw_game()

	exit_game()

if __name__ == "__main__":
	run_game()