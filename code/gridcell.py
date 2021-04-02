import string
from abc import ABC, abstractmethod
from code.constants import C
from code.helpers import *

class GridCell(ABC):
	@abstractmethod
	def draw(self, screen, x, y):
		pass

	# TODO this will need to change when cops to bribe are added, since they're occupied but can be pushed onto
	@property
	def pushable(self):
		return False

	@property
	def is_char(self):
		return False

	@staticmethod
	# Returns the created GridCell or the rotation angle integer for the player's position.
	def create_grid_cell(modifier, content):
		if modifier == '#': # Wall
			return Wall()
		if modifier == '$': # Player
			content = content.upper()
			if content == 'S':
				return C.SOUTH
			if content == 'E':
				return C.EAST
			if content == 'W':
				return C.WEST
			return C.NORTH
		if modifier in '1234':
			return modifier
		if content in string.whitespace:
			return None
		return Char(content, modifier == '!')

class Wall(GridCell):
	def draw(self, screen, x, y):
		screen.blit(C.WALL_IMG, (x, y))

class Char(GridCell):
	def __init__(self, char, locked=False):
		self.char = char
		self.locked = locked
		if self.locked:
			background = C.LOCKED_CHAR_IMG
			text_color = C.LOCKED_TEXT_COLOR
		else:
			background = C.CHAR_IMG
			text_color = C.CHAR_TEXT_COLOR

		self.img = background.convert_alpha()
		text = C.CHAR_FONT.render(char, True, text_color)
		self.img.blit(text, center2D(text.get_size(), C.GRID_SIZE))

	@property
	def pushable(self):
		return not self.locked

	@property
	def is_char(self):
		return True

	def draw(self, screen, x, y):
		screen.blit(self.img, (x, y))


if __name__ == "__main__":
	import code.game
	code.game.run_game()