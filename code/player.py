from code.constants import C
from code.helpers import *

class Player:
	def __init__(self):
		self.moving = False
		self.direction = C.NORTH
		self.x, self.y = 0, 0
		self.fx, self.fy = 0, 0
		self.dx, self.dy = 0, 0
		self.level = None
		self.draw_rect = pygame.Rect(center2D(C.GRID_SIZE, C.SCREEN_SIZE), C.GRID_SIZE)
		self.img = C.PLAYER_IMG
		self.sprite = pygame.transform.rotate(self.img, C.SOUTH)

	@property
	def pos(self):
		return self.x, self.y

	@property
	def fpos(self):
		return self.fx, self.fy

	def change_level(self, level):
		self.level = level
		self.x, self.y = level.player_start_pos
		self.set_direction(level.player_start_dir)
		self.stop_moving(False)

	def draw(self, screen):
		screen.blit(self.sprite, self.draw_rect.topleft)

	def try_start_moving(self, dx, dy, pulling):
		def rotate(compare):
			if dx != 0:
				self.set_direction(C.EAST if dx == compare else C.WEST)
			else:
				self.set_direction(C.SOUTH if dy == compare else C.NORTH)

		if not pulling:
			rotate(1)
		pulled = pulling and self.level.attempt_pull(dx, dy)
		if pulled:
			rotate(-1)
		if pulled or self.level.attempt_move(dx, dy):
			self.dx, self.dy = dx, dy
			self.moving = True

	def set_direction(self, direction):
		self.direction = direction
		self.sprite = pygame.transform.rotate(self.img, self.direction)

	def stop_moving(self, finish_move=True):
		self.moving = False
		if finish_move:
			self.level.finish_move()
			if self.dx != 0:
				self.x += self.dx
			else:
				self.y += self.dy
		self.fx, self.fy = self.x, self.y
		self.dx, self.dy = 0, 0

	def update(self, dt, kx, ky, pulling):
		if self.moving:
			if self.dx != 0:
				self.fx += self.dx * dt * C.PLAYER_SPEED
				if abs(self.x - self.fx) >= 1:
					self.stop_moving()
			else:  # Must be moving North or South
				self.fy += self.dy * dt * C.PLAYER_SPEED
				if abs(self.y - self.fy) >= 1:
					self.stop_moving()
		elif kx != 0 or ky != 0:
			dx, dy = (kx, 0) if kx != 0 else (0, ky)
			self.try_start_moving(dx, dy, pulling)


if __name__ == "__main__":
	import code.game

	code.game.run_game()
