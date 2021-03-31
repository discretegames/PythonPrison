import pygame
from code.helpers import *
from code.constants import *

class Player:
	moving: bool
	direction: int
	last_direction: int
	x: int
	y: int
	fx: float
	fy: float
	dx: int = 0
	dy: int = 0

	def __init__(self):
		self.x, self.y = 3, 1 # TODO get from file eventually
		self.draw_rect = pygame.Rect(center(C.SCREEN_WIDTH), center(C.SCREEN_HEIGHT), C.GRID_SIZE, C.GRID_SIZE)
		self.img = load_image('player')
		self.sprite = pygame.transform.rotate(self.img, C.SOUTH)
		self.direction = C.NORTH
		self.stop_moving()

	@property
	def pos(self):
		return self.x, self.y

	@property
	def fpos(self):
		return self.fx, self.fy

	def draw(self, screen):
		screen.blit(self.sprite, self.draw_rect.topleft)

	def start_moving(self, direction):
		self.direction = direction
		self.sprite = pygame.transform.rotate(self.img, self.direction)
		self.moving = True

	def stop_moving(self):
		self.moving = False
		self.last_direction = self.direction
		if self.direction in (C.EAST, C.WEST):
			self.x += self.dx
		else:
			self.y += self.dy
		self.fx, self.fy = self.x, self.y
		self.dx, self.dy = 0, 0

	def update(self, dt, key_dx, key_dy):
		if self.moving:
			if self.direction in (C.EAST, C.WEST):
				self.fx += self.dx * dt * C.PLAYER_SPEED
				if abs(self.x - self.fx) >= 1:
					self.stop_moving()
			else: # Must be moving North or South
				self.fy += self.dy * dt * C.PLAYER_SPEED
				if abs(self.y - self.fy) >= 1:
					self.stop_moving()
		else:
			if key_dx != 0:
				self.dx = key_dx
				self.start_moving(C.EAST if key_dx == 1 else C.WEST)
			elif key_dy != 0:
				self.dy = key_dy
				self.start_moving(C.SOUTH if key_dy == 1 else C.NORTH)
		# TODO Consider just using dx,dy instead of converting to direction and back?

if __name__ == "__main__":
	import code.game
	code.game.run_game_subdir()