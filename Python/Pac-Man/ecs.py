import pygame
from pygame.math import *
from pygame import Surface

class Component:
	def __init__(self):
		self.owner = None

	def process(self, delta: float):
		pass

	def draw(self, surface: Surface):
		pass

class Entity:
	def __init__(self, pos: Vector2 = Vector2(0, 0), components: list[Component] = []):
		self.pos = pos
		self.components = components
		for c in self.components:
			c.owner = self

	def process(self, delta: float):
		for c in self.components:
			c.process(delta)

	def draw(self, surface: Surface):
		for c in self.components:
			c.draw(surface)

