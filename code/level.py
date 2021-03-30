import pygame
from code.constants import *

class Level:
	def __init__(self, player):
		self.width, self.height = 30, 20 # TODO get from file eventually
		self.draw_rect = pygame.Rect(0, 0, C.GRID_SIZE * self.width, C.GRID_SIZE * self.height)
		self.move(player)

	@property
	def size(self):
		return self.width, self.height

	def move(self, player):
		x = player.draw_rect.x - player.fx * C.GRID_SIZE
		y = player.draw_rect.y - player.fy * C.GRID_SIZE
		self.draw_rect.update(x, y, *self.draw_rect.size)

	def draw(self, screen):
		pygame.draw.rect(screen, C.LEVEL_COLOR, self.draw_rect)
		#screen.fill(C.LEVEL_COLOR, self.draw_rect)

if __name__ == "__main__":
	import code.game
	code.game.run_game_subdir()