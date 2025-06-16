from ecs import *
from pygame import Color

class CircleSprite(Component):
	def __init__(self, radius: float, color: Color = Color(0, 0, 0)):
		self.radius = radius
		self.color = color

	def draw(self, surface: Surface):
		pygame.draw.circle(surface, self.color, tuple(self.owner.pos), self.radius)

