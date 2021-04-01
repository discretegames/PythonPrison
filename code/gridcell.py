from abc import ABC, abstractmethod
from code.helpers import *

class GridCell(ABC):
	@abstractmethod
	def draw(self, screen, x, y):
		pass

	@property
	def pushable(self):
		return False

	@staticmethod
	# Returns the created GridCell or the rotation angle integer for the player's position.
	def create_grid_cell(modifier, content):
		if content in string.whitespace:
			return None
		if modifier.upper() == 'P':
			content = content.upper()
			if content == 'S':
				return C.SOUTH
			if content == 'E':
				return C.EAST
			if content == 'W':
				return C.WEST
			return C.NORTH
		elif modifier == '|':
			if content == '#':
				return Wall()
		elif modifier == '!':
			return Char(content, True)
		return Char(content)

class Wall(GridCell):
	def draw(self, screen, x, y):
		screen.blit(C.WALL_IMG, (x, y))

class Char(GridCell):
	def __init__(self, char, locked=False):
		self.char = char
		self.locked = locked
		if self.locked:
			background = C.LOCKED_CHAR_IMG
			text_color = C.LOCKED_CHAR_TEXT_COLOR
		else:
			background = C.CHAR_IMG
			text_color = C.CHAR_TEXT_COLOR

		self.img = background.convert_alpha()
		text = C.CHAR_FONT.render(self.char, True, text_color)
		self.img.blit(text, center2D(text.get_size(), C.GRID_SIZE))
		super().__init__()

	@property
	def pushable(self):
		return not self.locked

	def draw(self, screen, x, y):
		screen.blit(self.img, (x, y))


if __name__ == "__main__":
	import code.game
	code.game.run_game()