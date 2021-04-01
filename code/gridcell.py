from abc import ABC, abstractmethod
from code.helpers import *

class GridCell(ABC):
	@abstractmethod
	def draw(self, screen, x, y):
		pass

	@property
	def solid(self):
		return True

	@property
	def pushable(self):
		return False

	@staticmethod
	# Returns the created GridCell or the rotation angle integer for the player's position.
	def create_grid_cell(modifier, content):
		modifier, content = modifier.upper(), content.upper()
		if modifier == 'P':
			if content == 'S':
				return C.SOUTH
			if content == 'E':
				return C.EAST
			if content == 'W':
				return C.WEST
			return C.NORTH
		if modifier == '|':
			if content == '#':
				return Wall()
		return None

class Wall(GridCell):
	def draw(self, screen, x, y):
		screen.blit(C.WALL_IMG, (x, y))

if __name__ == "__main__":
	import code.game
	code.game.run_game()