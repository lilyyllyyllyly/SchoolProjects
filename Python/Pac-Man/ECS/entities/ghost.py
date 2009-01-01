from ECS.ecs import *
from ECS.components.movement import *
from ECS.components.sprites import *

from pygame import Color
from pygame.math import *

class Ghost(Entity):
	GHOST_SPEED: float = 32
	GHOST_SIZE: int = 12
	GHOST_COLOR: Color = Color(255, 0, 0)

	def __init__(self, maze: Maze, player: Entity, pos: Vector2 = Vector2(0, 0)):
		self.maze = maze
		self.player = player
		self.center = Vector2(self.GHOST_SIZE/2, self.GHOST_SIZE/2)

		self.mover = ColliderMover(self.maze, offset = self.center)
		super().__init__(pos, [
			self.mover,
			CircleSprite(radius = self.GHOST_SIZE/2, offset = self.center, color = self.GHOST_COLOR),
		])

	def process(self, delta: float, keys: list[bool]):
		self.mover.vel = self.player.pos - self.pos
		self.mover.vel = self.mover.vel.normalize() if (self.mover.vel) else Vector2(0, 0)
		self.mover.vel *= self.GHOST_SPEED

		super().process(delta, keys)

