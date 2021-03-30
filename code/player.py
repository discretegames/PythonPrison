import pygame
from code import *

class Player:
	def __init__(self):
		self.pos = (C.SCREEN_WIDTH - C.GRID_SIZE)//2, (C.SCREEN_HEIGHT - C.GRID_SIZE)//2
		self.img = load_image('player')
		self.rotated = pygame.transform.rotate(self.img, C.SOUTH)

	def draw(self, screen):
		screen.blit(self.rotated, self.pos)

	def rotate(self, angle):
		self.rotated = pygame.transform.rotate(self.img, angle)

