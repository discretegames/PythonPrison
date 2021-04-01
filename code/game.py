import sys
from code.player import Player
from code.level import Level
from code.helpers import *

running: bool = False

def init_game():
	# noinspection PyGlobalUndefined
	global screen, player, level
	pygame.init()
	pygame.display.set_caption(C.SCREEN_TITLE)
	pygame.key.set_repeat() # no args intentionally
	screen = pygame.display.set_mode(C.SCREEN_SIZE)
	player = Player()
	level = Level(player, 'testlevel.txt')
	player.change_level(level)

def exit_game():
	pygame.quit()
	sys.exit()

def draw_game():
	screen.blit(C.BACKGROUND_IMG, (0, 0))
	level.draw(screen)
	player.draw(screen)
	pygame.display.update()

def get_inputs():
	keys = pygame.key.get_pressed()
	sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
	kx, ky = 0, 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			global running
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

	return kx, ky

def run_game():
	init_game()
	clock = pygame.time.Clock()
	global running
	running = True

	while running:
		dt = clock.tick(C.FPS) / 1000
		kx, ky = get_inputs()
		player.update(dt, kx, ky)
		level.update()
		draw_game()

	exit_game()

if __name__ == "__main__":
	run_game()