import pygame
from code.helpers import *
from code.constants import *

class Player:
	moving: bool
	fx: float
	fy: float

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

	def stop_moving(self, dx=0, dy=0):
		self.moving = False
		self.x += dx
		self.y += dy
		self.fx, self.fy = self.x, self.y

	def update(self, dt, dx, dy):
		if self.moving:
			if self.direction in (C.EAST, C.WEST):
				dx = -1 if self.direction == C.WEST else 1
				self.fx += dx * dt * C.PLAYER_SPEED
				if abs(self.x - self.fx) >= 1:
					self.stop_moving(dx=dx)
			else: # Must be moving North or South
				dy = -1 if self.direction == C.NORTH else 1
				self.fy += dy * dt * C.PLAYER_SPEED
				if abs(self.y - self.fy) >= 1:
					self.stop_moving(dy=dy)
		else:
			if dx != 0:
				self.start_moving(C.EAST if dx == 1 else C.WEST)
			elif dy != 0:
				self.start_moving(C.SOUTH if dy == 1 else C.NORTH)
		# TODO Consider just using dx,dy instead of converting to direction and back?

if __name__ == "__main__":
	import code.game
	code.game.run_game_subdir()