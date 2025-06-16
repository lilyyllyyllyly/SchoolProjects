import pygame
from pygame import Color, Surface
from pygame.math import Vector2

class Maze:
	FREE = '0'
	OBSTACLE = '1'

	FREE_CLR = Color(0, 0, 0, 0)
	OBSTACLE_CLR = Color(10, 10, 100)

	def __init__(self, grid: list[list[str]], game_w: int, game_h: int):
		# initializing
		self.grid = grid

		self.rows = len(grid)
		self.cols = len(grid[0])

		self.row_size = (float(game_h)/self.rows)
		self.col_size = (float(game_w)/self.cols)

		# drawing maze texture
		self.base_tex = Surface((self.cols, self.rows))
		self.base_tex.lock()
		for i in range(0, self.rows):
			for j in range(0, self.cols):
				if (grid[i][j] == self.OBSTACLE):
					self.base_tex.set_at((j, i), self.OBSTACLE_CLR)
		self.base_tex.unlock()

		self.tex = self.base_tex
		self.scale_maze_tex(game_w, game_h)

	def from_csv(csv: str, game_w: int, game_h: int):
		grid_unstripped = [text_row.split(',') for text_row in csv.split('\n') if text_row != ""]
		grid = [list(map(str.strip, row)) for row in grid_unstripped]
		return Maze(grid, game_w, game_h)

	def scale_maze_tex(self, game_w: int, game_h: int):
		self.tex = pygame.transform.scale(self.base_tex, (game_w, game_h))

	def is_in_wall(self, pos: Vector2):
		return self.grid[int(pos.y // self.row_size)][int(pos.x // self.col_size)] != self.OBSTACLE

