import pygame
from code.helpers import *
from code.constants import *

class Player:
	def __init__(self):
		self.x, self.y = 3, 1 # TODO get from file eventually
		self.draw_rect = pygame.Rect(center(C.SCREEN_WIDTH), center(C.SCREEN_HEIGHT), C.GRID_SIZE, C.GRID_SIZE)
		self.img = load_image('player')
		self.rotated = pygame.transform.rotate(self.img, C.SOUTH)

	@property
	def pos(self):
		return self.x, self.y

	def draw(self, screen):
		screen.blit(self.rotated, self.draw_rect.topleft)

	def rotate(self, angle):
		self.rotated = pygame.transform.rotate(self.img, angle)