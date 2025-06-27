from ECS.ecs import *
from pygame.math import *
from maze import Maze

class Mover(Component):
	def __init__(self, vel: Vector2 = Vector2(0, 0)):
		super()
		self.vel = vel

	def process(self, delta: float, keys: list[bool]):
		self.owner.pos += self.vel * delta

class ColliderMover(Component):
	def __init__(self, maze: Maze, offset: Vector2 = Vector2(0, 0), vel: Vector2 = Vector2(0, 0)):
		super()
		self.maze = maze
		self.offset = offset
		self.vel = vel

	def process(self, delta: float, keys: list[bool]):
		next_pos = self.owner.pos + self.vel * delta
		if (not self.maze.is_in_wall(next_pos + self.offset)):
			self.owner.pos = next_pos

	def test_move(self, delta: float):
		next_pos = self.owner.pos + self.vel * delta
		return not self.maze.is_in_wall(next_pos + self.offset)

