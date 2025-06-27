from ECS.ecs import *
from ECS.components.sprites import *

from pygame import Color
from pygame.math import *

class SmallDot(Entity):
	DOT_SIZE: int = 4
	DOT_COLOR: Color = Color(255, 255, 255)
	DOT_SCORE = 100

	def __init__(self, pacman: Entity, pos: Vector2 = Vector2(0, 0)):
		self.pacman = pacman
		super().__init__(pos, [
			CircleSprite(radius = self.DOT_SIZE/2, color = self.DOT_COLOR),
		])

	def process(self, delta: float, keys: list[bool]):
		super().process(delta, keys)

		if (self.pos.distance_squared_to(self.pacman.pos + self.pacman.center) < ((self.DOT_SIZE + self.pacman.PLAYER_SIZE)/2)**2):
			self.pacman.score += self.DOT_SCORE
			self.entities.remove(self)

