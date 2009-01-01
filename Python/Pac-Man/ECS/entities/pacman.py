from ECS.ecs import *
from ECS.components.movement import *
from ECS.components.sprites import *

from pygame import Color
from pygame.math import *

class Pacman(Entity):
	PLAYER_SPEED: float = 64
	PLAYER_SIZE: int = 12
	PLAYER_COLOR: Color = Color(255, 255, 0)

	def __init__(self, maze: Maze, pos: Vector2 = Vector2(0, 0)):
		self.maze = maze
		self.center = Vector2(self.PLAYER_SIZE/2, self.PLAYER_SIZE/2)

		self.mover = ColliderMover(self.maze, offset = self.center)
		super().__init__(pos, [
			self.mover,
				CircleSprite(radius = self.PLAYER_SIZE/2, offset = self.center, color = self.PLAYER_COLOR),
		])

	def process(self, delta: float, keys: list[bool]):
		dir: Vector2 = Vector2(int(keys[pygame.K_d]) - int(keys[pygame.K_a]),
		                       int(keys[pygame.K_s]) - int(keys[pygame.K_w]))
		self.mover.vel = self.PLAYER_SPEED * (dir.normalize() if (dir) else Vector2(0, 0))

		super().process(delta, keys)

