from random import shuffle

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

		self.last_resolve_dir = Vector2(0, 0)

		self.mover = ColliderMover(self.maze, offset = self.center)
		super().__init__(pos, [
			self.mover,
			CircleSprite(radius = self.GHOST_SIZE/2, offset = self.center, color = self.GHOST_COLOR),
		])

	def process(self, delta: float, keys: list[bool]):
		self.mover.vel = self.player.pos - self.pos
		self.mover.vel = self.mover.vel.normalize() if (self.mover.vel) else Vector2(0, 0)
		self.mover.vel *= self.GHOST_SPEED

		if (not self.mover.test_move(delta)):
			# if move will collide, try to avoid the wall
			# - make ghost not able to go backwards
			dirs = [Vector2( 0,  1),
			        Vector2( 0, -1),
			        Vector2( 1,  0),
			        Vector2(-1,  0)]
			if ((backwards := self.last_resolve_dir * -1) in dirs): dirs.remove(backwards)

			# - find dir that gets closest to pac-man
			smallest_dist: float = -1
			picked_dir: Vector2 = Vector2(0, 0)
			for dir in dirs:
				self.mover.vel = dir * self.GHOST_SPEED
				if (not self.mover.test_move(delta)): continue

				# dir valid (doesn't collide)
				dist = (self.player.pos - (self.pos + self.mover.vel * delta)).magnitude()
				if (dist < smallest_dist or smallest_dist < 0):
					smallest_dist = dist
					picked_dir = dir

			# - use chosen dir
			self.mover.vel = picked_dir * self.GHOST_SPEED
			self.last_resolve_dir = picked_dir
		else:
			self.last_resolve_dir = Vector2(0, 0)

		super().process(delta, keys)

