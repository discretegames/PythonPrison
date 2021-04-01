from code.helpers import *
from gridcell import GridCell

class Level:
	grid: list = []
	title: str = 'Some Level'
	width: int = 0
	height: int = 0
	player_start_pos: tuple = 0, 0
	player_start_dir: int = C.NORTH

	def __init__(self, filename):
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

	def update(self, player):
		x = player.draw_rect.x - player.fx * C.GRID_SCALE
		y = player.draw_rect.y - player.fy * C.GRID_SCALE
		self.draw_rect.update(x, y, *self.draw_rect.size)

	def draw(self, screen):
		pygame.draw.rect(screen, C.LEVEL_COLOR, self.draw_rect)
		for y in range(self.height):
			draw_y = self.draw_rect.y + C.GRID_SCALE * y
			for x in range(self.width):
				draw_x = self.draw_rect.x + C.GRID_SCALE * x
				if self.grid[y][x]:

					self.grid[y][x].draw(screen, draw_x, draw_y)

	def in_bounds(self, x, y):
		return 0 <= x < self.width and 0 <= y < self.height

	def cell_occupied(self, x, y):
		return self.in_bounds(x, y) and self.grid[y][x]

	def attempt_move(self, player, dx, dy):
		x, y = player.x + dx, player.y + dy
		if not self.cell_occupied(x, y):
			return True # Always allow motion into empty spaces, even out of bounds.
		if not self.grid[y][x].pushable:
			return False

		x_start, y_start = x, y
		while self.cell_occupied(x, y) and self.grid[y][x].pushable:
			x += dx
			y += dy

		if not self.in_bounds(x, y):
			return False # Things can't be pushed out of bounds, even though the player is allowed out there.
		if self.cell_occupied(x, y) and not self.grid[y][x].pushable:
			return False # Can't push something not pushable.

		self.apply_push(x_start, y_start, x, y, dx, dy)
		return True

	def apply_push(self, x1, y1, x2, y2, dx, dy): # Assumes push is valid.
		if dx == -1:
			for x in range(x2, x1):
				self.grid[y1][x] = self.grid[y1][x + 1]
		elif dx == 1:
			for x in range(x2, x1, -1):
				self.grid[y1][x] = self.grid[y1][x - 1]
		elif dy == -1:
			for y in range(y2, y1):
				self.grid[y][x1] = self.grid[y + 1][x1]
		elif dy == 1:
			for y in range(y2, y1, -1):
				self.grid[y][x1] = self.grid[y - 1][x1]
		self.grid[y1][x1] = None

	# TODO draw pushes properly

if __name__ == "__main__":
	import code.game
	code.game.run_game()