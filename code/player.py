import pygame
from code.helpers import *

class Player:
	moving: bool
	direction: int = C.NORTH
	x: int
	y: int
	fx: float
	fy: float
	dx: int = 0
	dy: int = 0

	def __init__(self, start_pos):
		self.x, self.y = start_pos
		cx = center(C.SCREEN_WIDTH, C.GRID_SIZE)
		cy = center(C.SCREEN_HEIGHT, C.GRID_SIZE)
		self.draw_rect = pygame.Rect(cx, cy, C.GRID_SIZE, C.GRID_SIZE)
		self.img = C.PLAYER_IMG
		self.sprite = pygame.transform.rotate(self.img, C.SOUTH)
		self.stop_moving()

	@property
	def pos(self):
		return self.x, self.y

	@property
	def fpos(self):
		return self.fx, self.fy

	def draw(self, screen):
		screen.blit(self.sprite, self.draw_rect.topleft)

	def start_moving(self, dx, dy):
		self.dx, self.dy = dx, dy
		if self.dx != 0:
			self.direction = C.EAST if self.dx == 1 else C.WEST
		else:
			self.direction = C.SOUTH if self.dy == 1 else C.NORTH
		self.sprite = pygame.transform.rotate(self.img, self.direction)
		self.moving = True

	def stop_moving(self):
		self.moving = False
		if self.direction in (C.EAST, C.WEST):
			self.x += self.dx
		else:
			self.y += self.dy
		self.fx, self.fy = self.x, self.y
		self.dx, self.dy = 0, 0

	def update(self, dt, kx, ky, level):
		if self.moving:
			if self.direction in (C.EAST, C.WEST):
				self.fx += self.dx * dt * C.PLAYER_SPEED
				if abs(self.x - self.fx) >= 1:
					self.stop_moving()
			else: # Must be moving North or South
				self.fy += self.dy * dt * C.PLAYER_SPEED
				if abs(self.y - self.fy) >= 1:
					self.stop_moving()
		elif kx != 0 or ky != 0:
			dx, dy = (kx, 0) if kx != 0 else (0, ky)
			if not level.is_solid(self.x + dx, self.y + dy):
				self.start_moving(dx, dy)

if __name__ == "__main__":
	import code.game
	code.game.run_game()