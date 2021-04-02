from code.helpers import *


class Player:
	moving: bool = False
	direction: int = C.NORTH
	x: int = 0
	y: int = 0
	fx: float = 0
	fy: float = 0
	dx: int = 0
	dy: int = 0
	level = None

	def __init__(self):
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
		if not pulling:
			if dx != 0:
				self.set_direction(C.EAST if dx == 1 else C.WEST)
			else:
				self.set_direction(C.SOUTH if dy == 1 else C.NORTH)

		if pulling and self.level.attempt_pull(dx, dy) or self.level.attempt_move(dx, dy):
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
