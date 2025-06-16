from pygame.math import Vector2

class Movable:
	def __init__(self, pos: Vector2 = Vector2(0, 0), vel: Vector2 = Vector2(0, 0)):
		self.pos = pos
		self.vel = vel

