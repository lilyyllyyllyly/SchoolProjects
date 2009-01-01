import pygame
from pygame.math import *
from pygame import Surface

class Component(object):
	def __init__(self):
		self.owner = None

	def process(self, delta: float, keys: list[bool]):
		pass

	def draw(self, surface: Surface):
		pass

class Entity(object): pass # forward declaring so i can access the class name inside it's declaration (for type hints)
class Entity(object):
	entities: list[Entity] = []

	def __init__(self, pos: Vector2 = Vector2(0, 0), components: list[Component] = []):
		self.pos = pos
		self.components = components

		for c in self.components:
			c.owner = self

		self.entities.append(self)

	def destroy(self):
		self.entities.remove(self)

	def process(self, delta: float, keys: list[bool]):
		for c in self.components:
			c.process(delta, keys)

	def draw(self, surface: Surface):
		for c in self.components:
			c.draw(surface)

