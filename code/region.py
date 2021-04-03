from code.helpers import *
from code.constants import C

class Region:
	def __init__(self, level):
		self.level = level
		self.start = None
		self.end = None
		self.locked = False

	def update(self, pos, start, force=False):
		if self.locked and not force:
			self.level.set_message("That region is locked in this level")
			return
		x, y = clamp(pos[0], self.level.width - 1), clamp(pos[1], self.level.height - 1)
		if start:
			if self.end and (x > self.end[0] or y > self.end[1]):
				self.end = None
			self.start = x, y
		else:
			if self.start and (x < self.start[0] or y < self.start[1]):
				self.start = None
			self.end = x, y

	def lock(self):
		self.locked = True

	def empty(self):
		return not self.start and not self.end

	def contains(self, x, y):
		if self.empty():
			return False
		x1, y1, x2, y2 = self.coords()
		return x1 <= x <= x2 and y1 <= y <= y2

	def coords(self):
		if self.start and self.end:
			return *self.start, *self.end
		if self.start:
			return *self.start, *self.start
		if self.end:
			return *self.end, *self.end
		return None

	def draw(self, screen, color, locked_color):
		if not self.empty():
			x1, y1, x2, y2 = (c * C.GRID_SCALE for c in self.coords())
			rect = pygame.Rect(x1, y1, x2 - x1 + C.GRID_SCALE, y2 - y1 + C.GRID_SCALE)
			rect.move_ip(self.level.draw_rect.topleft)
			if self.locked:
				color = locked_color
			pygame.draw.rect(screen, color, rect, border_radius=C.REGION_RECT_RADIUS)

if __name__ == "__main__":
	import code.game
	code.game.run_game()