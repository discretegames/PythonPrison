import string
from code.helpers import *
from code.gridcell import GridCell, Char, Cop
from code.executor import Executor
from code.constants import C
from code.push import Push
from code.region import Region
import random

class Level:
	def __init__(self, filename, player, message=''):
		self.grid = []
		self.title = 'Some Level'
		self.set_message(message)
		self.width, self.height = 0, 0
		self.player_start_pos = 0, 0
		self.player_start_dir = C.NORTH
		self.push = None
		self.executor = Executor()
		self.exec_region = Region(self)
		self.out_region = Region(self)
		self.player = player
		self.load_level(filename)
		self.draw_rect = pygame.Rect(0, 0, C.GRID_SCALE * self.width, C.GRID_SCALE * self.height)

	def set_message(self, message):
		self.message = C.ERROR_FONT.render(message, True, C.LEVEL_TEXT_COLOR)

	def load_level(self, filename):
		path = asset_path(filename, 'levels')
		with open(path) as file:
			lines = file.readlines()
		if lines:
			self.title = lines[0].strip()
			self.text = C.LEVEL_TITLE_FONT.render(self.title, True, C.LEVEL_TEXT_COLOR)
		if len(lines) > 1:
			args = [arg.lower() for arg in lines[1].split()]
			if 'lockexec' in args:
				self.exec_region.lock()
			if 'lockout' in args:
				self.out_region.lock()
		self.load_grid(lines[2:])

	def load_grid(self, file_grid_lines):
		file_grid_lines = [line for line in file_grid_lines if line]
		self.height = len(file_grid_lines)
		self.width = max(map(len, file_grid_lines)) // 2 if file_grid_lines else 0
		self.grid = [[None] * self.width for _ in range(self.height)]

		for y in range(self.height):
			length = len(file_grid_lines[y])
			for x in range(self.width):
				modifier = file_grid_lines[y][2 * x] if 2 * x < length else ' '
				content = file_grid_lines[y][2 * x + 1] if 2 * x + 1 < length else ' '
				cell = GridCell.create_grid_cell(modifier, content)
				if isinstance(cell, int): # Must be player rotation.
					self.player_start_dir = cell
					self.player_start_pos = x, y
				elif isinstance(cell, str): # Must be region corner.
					if cell in '12':
						self.exec_region.update((x, y), cell == '1', True)
					else:
						self.out_region.update((x, y), cell == '3', True)
				else:
					self.grid[y][x] = cell

	@property
	def size(self):
		return self.width, self.height

	def update(self, corners):
		if corners[0]:
			self.exec_region.update(self.player.pos, True)
		elif corners[1]:
			self.exec_region.update(self.player.pos, False)
		if corners[2]:
			self.out_region.update(self.player.pos, True)
		elif corners[3]:
			self.out_region.update(self.player.pos, False)

		x = self.player.draw_rect.x - self.player.fx * C.GRID_SCALE
		y = self.player.draw_rect.y - self.player.fy * C.GRID_SCALE
		self.draw_rect.update(x, y, *self.draw_rect.size)

		if self.executor.is_done():
			self.finish_exec(self.executor.error, self.executor.output)

	def draw(self, screen):
		# Border
		pygame.draw.rect(screen, C.LEVEL_BORDER_COLOR, self.draw_rect.inflate(C.LEVEL_BORDER, C.LEVEL_BORDER))
		#Background
		pygame.draw.rect(screen, C.LEVEL_BG_COLOR, self.draw_rect)

		# Regions
		self.out_region.draw(screen, C.OUT_REGION_COLOR, C.OUT_LOCKED_COLOR)
		self.exec_region.draw(screen, C.EXEC_REGION_COLOR, C.EXEC_LOCKED_COLOR)

		# Grid
		for y in range(self.height):
			draw_y = self.draw_rect.y + C.GRID_SCALE * y
			for x in range(self.width):
				draw_x = self.draw_rect.x + C.GRID_SCALE * x
				if self.grid[y][x]:
					if self.push and self.push.contains(x, y):
						push_x = self.player.draw_rect.x + C.GRID_SCALE * (x - self.player.x)
						push_y = self.player.draw_rect.y + C.GRID_SCALE * (y - self.player.y)
						self.grid[y][x].draw(screen, push_x, push_y)
					else:
						self.grid[y][x].draw(screen, draw_x, draw_y)
		# Text
		w, h = self.message.get_size()
		screen.blit(self.message, (center1D(w, C.SCREEN_WIDTH), C.SCREEN_HEIGHT - h - C.FONT_VERT_OFFSET))
		screen.blit(self.text, (center1D(self.text.get_width(), C.SCREEN_WIDTH), C.FONT_VERT_OFFSET))

	def in_bounds(self, x, y):
		return 0 <= x < self.width and 0 <= y < self.height

	def cell_occupied(self, x, y):
		return self.in_bounds(x, y) and self.grid[y][x]

	def player_can_occupy(self, x, y):
		if not self.cell_occupied(x, y):
			return True
		return self.grid[y][x].occupiable

	def attempt_pull(self, dx, dy):
		x, y = self.player.x + dx, self.player.y + dy
		pulled_x, pulled_y = self.player.x - dx, self.player.y - dy
		object_to_pull = self.cell_occupied(pulled_x, pulled_y) and self.grid[pulled_y][pulled_x].pushable
		if object_to_pull and self.player_can_occupy(x, y) and not self.cell_occupied(*self.player.pos):
			self.push = Push(pulled_x, pulled_y, self.player.x, self.player.y, dx, dy)
			return True
		return False

	def attempt_move(self, dx, dy):
		x, y = self.player.x + dx, self.player.y + dy
		if self.player_can_occupy(x, y):
			return True # Always allow motion into empty spaces, even out of bounds.
		if not self.grid[y][x].pushable:
			return False

		x_start, y_start = x, y
		while self.cell_occupied(x, y) and self.grid[y][x].pushable:
			x += dx
			y += dy

		if not self.in_bounds(x, y):
			return False # Things can't be pushed out of bounds even though the player is allowed out there.

		is_cop = isinstance(self.grid[y][x], Cop)
		# Feels like unnecessary checks here but I forget the exact logic so I'll leave it.
		if self.cell_occupied(x, y) and not self.grid[y][x].pushable and not is_cop:
			return False # Can't push something not pushable.

		if is_cop and self.grid[y][x].char != self.grid[y - dy][x - dx].char:
			return False # Cop char must match.
		self.push = Push(x_start, y_start, x, y, dx, dy, is_cop)
		return True

	def finish_move(self):
		if self.push:
			self.push.apply(self.grid)
			self.push = None

	def cell_is_char(self, x, y): # assumes x,y in bounds
		return self.grid[y][x] and isinstance(self.grid[y][x], Char)

	def read_code(self, x1, y1, x2, y2):
		lines = []
		min_indent = self.width
		for y in range(y1, y2+1):
			line = []
			indent = 0
			indent_over = False
			for x in range(x1, x2+1):
				char = self.grid[y][x].char if self.cell_is_char(x, y) else ' '
				line.append(char)
				if char != ' ':
					indent_over = True
				elif not indent_over:
					indent += 1
			line = ''.join(line)
			if not line.lstrip().startswith('#'):
				min_indent = min(min_indent, indent)
				lines.append(line)

		return C.CODE_HEADER + '\n'.join(line[min_indent:] for line in lines)

	def start_exec(self):
		if self.exec_region.empty():
			self.finish_exec('no execution region')
		else:
			code = self.read_code(*self.exec_region.coords())
			self.executor.execute(code)

	def finish_exec(self, error, output=''):
		header = 'Error: '
		if error:
			message = f'{header}{error}'
		elif self.out_region.empty():
			message = f'{header}no output region'
		else:
			message = 'Execution successful!'
		self.set_message(message)
		self.write_output(output)

	def cell_writable(self, x, y): # assumes x,y in bounds
		overwritable = (not self.grid[y][x]) or (self.cell_is_char(x, y) and not self.grid[y][x].locked)
		avoids_player = self.player.pos != (x, y)
		avoids_exec = not self.exec_region.contains(x, y)
		return overwritable and avoids_player and avoids_exec

	def write_cell(self, x, y, char): # assumes x,y valid and char valid
		if char == ' ':
			self.grid[y][x] = None
		else:
			self.grid[y][x] = Char(char)

	def write_output(self, output):
		if not output or self.out_region.empty():
			return

		def char_at(x, y):
			if y >= len(lines) or x >= len(lines[y]):
				return ' '
			char = lines[y][x]
			if char in string.whitespace:
				return ' '
			if char not in string.printable:
				return '?'
			return char

		lines = output.split('\n')
		x1, y1, x2, y2 = self.out_region.coords()
		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				if self.cell_writable(x, y):
					self.write_cell(x, y, char_at(x - x1, y - y1))

if __name__ == "__main__":
	import code.game
	code.game.run_game()