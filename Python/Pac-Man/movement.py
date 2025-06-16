from ecs import *
from pygame.math import *

class Mover(Component):
	def __init__(self, vel: Vector2 = Vector2(0, 0)):
		super()
		self.vel = vel

	def process(self, delta: float):
		self.owner.pos += self.vel * delta

