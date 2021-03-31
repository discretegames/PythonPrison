import pygame
from code.constants import *

class Level:
	def __init__(self, player):
		self.width, self.height = 30, 3 # TODO get from file eventually
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
		for x in range(self.width): # temporary
			x = self.draw_rect.x + 32 * x
			for y in range(self.height):
				y = self.draw_rect.y + 32 * y
				pygame.draw.rect(screen, (80, 80, 80), pygame.Rect(x, y, 31, 31))



if __name__ == "__main__":
	import code.game
	code.game.run_game_subdir()