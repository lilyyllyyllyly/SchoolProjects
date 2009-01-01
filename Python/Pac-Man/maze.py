import pygame
from pygame import Color, Surface
from pygame.math import Vector2

class Maze(object):
	CELL_W = 16
	CELL_H = 16

	FREE = '0'
	OBSTACLE = '1'

	FREE_CLR = Color(0, 0, 0, 0)
	OBSTACLE_CLR = Color(10, 10, 100)

	def __init__(self, grid: list[list[str]]):
		# initializing
		self.grid = grid

		self.rows = len(grid)
		self.cols = len(grid[0])

		self.cell_w = self.CELL_W
		self.cell_h = self.CELL_H

		self.maze_w = self.cols * self.CELL_W
		self.maze_h = self.rows * self.CELL_H

		# drawing maze texture
		self.base_tex = Surface((self.cols, self.rows))

		self.base_tex.lock()
		for i in range(0, self.rows):
			for j in range(0, self.cols):
				if (grid[i][j] == self.OBSTACLE):
					self.base_tex.set_at((j, i), self.OBSTACLE_CLR)
		self.base_tex.unlock()

		self.tex = pygame.transform.scale(self.base_tex, (self.maze_w, self.maze_h))

	def from_csv(csv: str):
		grid_unstripped = [text_row.split(',') for text_row in csv.split('\n') if text_row != ""]
		grid = [list(map(str.strip, row)) for row in grid_unstripped]
		return Maze(grid)

	def is_in_wall(self, pos: Vector2):
		if ((y := int(pos.y // self.CELL_H)) < 0 or y >= len(self.grid)):    return True
		if ((x := int(pos.x // self.CELL_W)) < 0 or x >= len(self.grid[0])): return True
		return self.grid[y][x] == self.OBSTACLE

