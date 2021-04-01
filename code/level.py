from code.helpers import *
from gridcell import GridCell

class Level:
	grid: list = []
	title: str = 'Some Level'
	width: int = 0
	height: int = 0
	player_start_pos: tuple = 0, 0
	player_start_dir: int = C.NORTH

	def __init__(self, player, filename):
		self.player = player
		self.load_level(filename)
		self.draw_rect = pygame.Rect(0, 0, C.GRID_SIZE * self.width, C.GRID_SIZE * self.height)

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
			for x in range(self.width):
				modifier = file_grid_lines[y][2*x]
				content = file_grid_lines[y][2*x+1]
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
		x = self.player.draw_rect.x - self.player.fx * C.GRID_SIZE
		y = self.player.draw_rect.y - self.player.fy * C.GRID_SIZE
		self.draw_rect.update(x, y, *self.draw_rect.size)

	# TODO move and tile background properly
	# def draw_background(self, screen):
	# 	w, h = C.BACKGROUND_IMG.get_size()
	# 	screen.blit(C.BACKGROUND_IMG, self.draw_rect)
	# 	screen.blit(C.BACKGROUND_IMG, self.draw_rect.move(0, -h))
	# 	screen.blit(C.BACKGROUND_IMG, self.draw_rect.move(-w, 0))
	# 	screen.blit(C.BACKGROUND_IMG, self.draw_rect.move(-w, -h))

	def draw(self, screen):
		pygame.draw.rect(screen, C.LEVEL_COLOR, self.draw_rect)
		for y in range(self.height):
			draw_y = self.draw_rect.y + C.GRID_SIZE * y
			for x in range(self.width):
				draw_x = self.draw_rect.x + C.GRID_SIZE * x
				if self.grid[y][x]:
					self.grid[y][x].draw(screen, draw_x, draw_y)

	def in_bounds(self, x, y):
		return 0 <= x < self.width and 0 <= y < self.height

	def is_solid(self, x, y):
		if self.in_bounds(x, y) and self.grid[y][x]:
			return self.grid[y][x].solid
		return False


if __name__ == "__main__":
	import code.game
	code.game.run_game()