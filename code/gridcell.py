import string
from abc import ABC, abstractmethod
from code.constants import C
from code.helpers import *

class GridCell(ABC):
	def __init__(self, char=' '):
		self.char = char

	@abstractmethod
	def draw(self, screen, x, y):
		pass

	@property
	def pushable(self):
		return False

	@property
	def occupiable(self): # by player
		return False

	@staticmethod
	# Returns the created GridCell or the rotation angle integer for the player's position.
	def create_grid_cell(modifier, content):
		modifier = modifier.lower()
		if modifier == '@':
			return Wall()
		if modifier == '#':
			return Fence()
		if modifier == '%':
			return Door()
		if modifier == '&':
			return Gate()
		if modifier == 'c':
			return Cop(' ' if content in string.whitespace else content) # just in case of tabs
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

class Fence(GridCell):
	def draw(self, screen, x, y):
		screen.blit(C.FENCE_IMG, (x, y))

class Gate(GridCell):
	def draw(self, screen, x, y):
		screen.blit(C.GATE_IMG, (x, y))

	@property
	def occupiable(self):
		return True

class Door(GridCell):
	def draw(self, screen, x, y):
		screen.blit(C.DOOR_IMG, (x, y))

	@property
	def occupiable(self):
		return True

class Cop(GridCell):
	def __init__(self, char):
		super().__init__(char)
		self.img = C.COP_IMG.convert_alpha()
		text = C.COP_FONT.render(self.char, True, C.COP_TEXT_COLOR)
		self.img.blit(text, C.COP_FONT_OFFSET)

	def draw(self, screen, x, y):
		screen.blit(self.img, (x, y))

class Char(GridCell):
	def __init__(self, char, locked=False):
		super().__init__(char)
		self.locked = locked
		if self.locked:
			background = C.LOCKED_CHAR_IMG
			text_color = C.LOCKED_TEXT_COLOR
		else:
			background = C.CHAR_IMG
			text_color = C.CHAR_TEXT_COLOR

		self.img = background.convert_alpha()
		text = C.CHAR_FONT.render(self.char, True, text_color)
		self.img.blit(text, center2D(text.get_size(), C.GRID_SIZE))

	@property
	def pushable(self):
		return not self.locked

	def draw(self, screen, x, y):
		screen.blit(self.img, (x, y))


if __name__ == "__main__":
	import code.game
	code.game.run_game()