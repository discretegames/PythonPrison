from code.helpers import *
from code.gridcell import GridCell
from code.executor import Executor

class Push:
	def __init__(self, x1, y1, x2, y2, dx, dy):
		self.x1, self.y1 = x1, y1
		self.x2, self.y2 = x2, y2
		self.dx, self.dy = dx, dy

	@property
	def x(self):
		return self.x1

	@property
	def y(self):
		return self.y1

	def in_push(self, x, y):
		if self.dx == 1:
			return y == self.y and self.x1 <= x < self.x2
		elif self.dx == -1:
			return y == self.y and self.x1 >= x > self.x2
		elif self.dy == 1:
			return x == self.x and self.y1 <= y < self.y2
		elif self.dy == -1:
			return x == self.x and self.y1 >= y > self.y2

class Level:
	grid: list = []
	title: str = 'Some Level'
	width: int = 0
	height: int = 0
	player_start_pos: tuple = 0, 0
	player_start_dir: int = C.NORTH
	push = None
	executor: Executor = Executor()

	def __init__(self, filename, player):
		self.player = player
		self.load_level(filename)
		self.draw_rect = pygame.Rect(0, 0, C.GRID_SCALE * self.width, C.GRID_SCALE * self.height)

	def load_level(self, filename):
		path = asset_path(filename, 'levels')
		with open(path) as file:
			lines = file.readlines()
		if lines:
			self.title = lines[0].strip()
		if len(lines) > 1:
			pass # TODO read the properties that would appear on lines[1]
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
				if isinstance(cell, int):
					self.player_start_dir = cell
					self.player_start_pos = x, y
				else:
					self.grid[y][x] = cell

	@property
	def size(self):
		return self.width, self.height

	def update(self):
		x = self.player.draw_rect.x - self.player.fx * C.GRID_SCALE
		y = self.player.draw_rect.y - self.player.fy * C.GRID_SCALE
		self.draw_rect.update(x, y, *self.draw_rect.size)

		if self.executor.is_done():
			self.finish_exec()

	def draw(self, screen):
		pygame.draw.rect(screen, C.LEVEL_COLOR, self.draw_rect)
		for y in range(self.height):
			draw_y = self.draw_rect.y + C.GRID_SCALE * y
			for x in range(self.width):
				draw_x = self.draw_rect.x + C.GRID_SCALE * x
				if self.grid[y][x]:
					if self.push and self.push.in_push(x, y):
						push_x = self.player.draw_rect.x + C.GRID_SCALE * (x - self.player.x)
						push_y = self.player.draw_rect.y + C.GRID_SCALE * (y - self.player.y)
						self.grid[y][x].draw(screen, push_x, push_y)
					else:
						self.grid[y][x].draw(screen, draw_x, draw_y)

	def in_bounds(self, x, y):
		return 0 <= x < self.width and 0 <= y < self.height

	def cell_occupied(self, x, y):
		return self.in_bounds(x, y) and self.grid[y][x]

	def attempt_pull(self, dx, dy):
		x, y = self.player.x + dx, self.player.y + dy
		pulled_x, pulled_y = self.player.x - dx, self.player.y - dy
		object_to_pull = self.cell_occupied(pulled_x, pulled_y) and self.grid[pulled_y][pulled_x].pushable
		destination_clear = not self.cell_occupied(x, y)
		if object_to_pull and destination_clear:
			self.push = Push(pulled_x, pulled_y, self.player.x, self.player.y, dx, dy)
			return True
		return False

	def attempt_move(self, dx, dy):
		x, y = self.player.x + dx, self.player.y + dy
		if not self.cell_occupied(x, y):
			return True # Always allow motion into empty spaces, even out of bounds.
		if not self.grid[y][x].pushable:
			return False

		x_start, y_start = x, y
		while self.cell_occupied(x, y) and self.grid[y][x].pushable:
			x += dx
			y += dy

		if not self.in_bounds(x, y):
			return False # Things can't be pushed out of bounds even though the player is allowed out there.
		if self.cell_occupied(x, y) and not self.grid[y][x].pushable:
			return False # Can't push something not pushable.

		self.push = Push(x_start, y_start, x, y, dx, dy)
		return True

	def finish_move(self):
		if self.push:
			self.apply_push()
			self.push = None

	def apply_push(self): # Assumes push is valid.
		p = self.push
		if p.dx == -1:
			for x in range(p.x2, p.x1):
				self.grid[p.y][x] = self.grid[p.y][x + 1]
		elif p.dx == 1:
			for x in range(p.x2, p.x1, -1):
				self.grid[p.y][x] = self.grid[p.y][x - 1]
		elif p.dy == -1:
			for y in range(p.y2, p.y1):
				self.grid[y][p.x] = self.grid[y + 1][p.x]
		elif p.dy == 1:
			for y in range(p.y2, p.y1, -1):
				self.grid[y][p.x] = self.grid[y - 1][p.x]
		self.grid[p.y1][p.x1] = None

	def get_code(self, x1, y1, x2, y2):
		lines = []
		min_indent = self.width
		x1, x2 = min(x1, x2), max(x1, x2)
		y1, y2 = min(y1, y2), max(y1, y2)
		for y in range(y1, y2+1):
			line = []
			indent = 0
			indent_over = False
			for x in range(x1, x2+1):
				char = self.grid[y][x].char if self.grid[y][x] else ' '
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
		code = self.get_code(0, 0, self.width - 1, self.height - 1)
		self.executor.execute(code)

	def finish_exec(self):
		print('Error: ', self.executor.error)
		print('Result:')
		print(self.executor.output)

if __name__ == "__main__":
	import code.game
	code.game.run_game()