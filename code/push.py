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

if __name__ == "__main__":
	import code.game
	code.game.run_game()