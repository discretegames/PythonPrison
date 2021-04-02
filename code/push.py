class Push:
	def __init__(self, x1, y1, x2, y2, dx, dy, delete_last=False):
		self.x1, self.y1 = x1, y1
		self.x2, self.y2 = x2, y2
		self.dx, self.dy = dx, dy
		self.delete_last = delete_last

	@property
	def x(self):
		return self.x1

	@property
	def y(self):
		return self.y1

	def contains(self, x, y):
		if self.dx == 1:
			return y == self.y and self.x1 <= x < self.x2
		elif self.dx == -1:
			return y == self.y and self.x1 >= x > self.x2
		elif self.dy == 1:
			return x == self.x and self.y1 <= y < self.y2
		elif self.dy == -1:
			return x == self.x and self.y1 >= y > self.y2

	def apply(self, grid): # Assumes push is valid.
		p = self
		if p.dx == -1:
			for x in range(p.x2, p.x1):
				grid[p.y][x] = grid[p.y][x + 1]
		elif p.dx == 1:
			for x in range(p.x2, p.x1, -1):
				grid[p.y][x] = grid[p.y][x - 1]
		elif p.dy == -1:
			for y in range(p.y2, p.y1):
				grid[y][p.x] = grid[y + 1][p.x]
		elif p.dy == 1:
			for y in range(p.y2, p.y1, -1):
				grid[y][p.x] = grid[y - 1][p.x]
		grid[p.y1][p.x1] = None
		if p.delete_last:
			grid[p.y2][p.x2] = None


if __name__ == "__main__":
	import code.game
	code.game.run_game()