import pygame
import sys

from ECS.ecs import *
from ECS.components.sprites import *
from ECS.components.movement import *
from ECS.entities.pacman import *
from ECS.entities.ghost import *
from ECS.entities.dots import *

from pygame.math import *
from pygame import Rect
from pygame import Color, Surface
from pygame.time import Clock
from pygame.font import Font

from maze import Maze

from random import randint

# window globals
FPS: int = 60
WIN_TITLE: str = ":3"

win_w: int = 480
win_h: int = 480

# color globals
BG_COLOR: Color = Color(5, 5, 20)
BORDER_COLOR: Color = Color(0, 0, 0)
OBSTACLE_COLOR: Color = Color(10, 10, 100)

# game globals
GAME_OVER_TIME: int = 1000 # ms

maze_file: str = sys.argv[1] if (len(sys.argv) > 1) else "maps/maze.csv"
try:
	with open(maze_file, 'r') as f:
		maze: Maze = Maze.from_csv(f.read())
except FileNotFoundError:
	maze: Maze = Maze([["1","1","1","1","1","1","1","1","1","1","1","1"],
	                   ["1","0","0","0","0","0","0","0","0","0","0","1"],
	                   ["1","0","1","1","1","0","0","1","1","1","0","1"],
	                   ["1","0","0","0","0","0","0","0","0","0","0","1"],
	                   ["1","0","1","0","1","0","0","1","0","1","0","1"],
	                   ["1","0","1","0","1","1","1","1","0","1","0","1"],
	                   ["1","0","1","0","0","0","0","0","0","1","0","1"],
	                   ["1","0","1","0","1","1","1","1","0","1","0","1"],
	                   ["1","0","0","0","0","0","0","0","0","0","0","1"],
	                   ["1","1","1","1","1","1","1","1","1","1","1","1"]])

game_w: int = maze.maze_w
game_h: int = maze.maze_h

paused: bool = False

# setup pygame
pygame.init()

win: Surface = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
scr: Surface = Surface((game_w, game_h))

pygame.display.set_caption(WIN_TITLE)
clock: Clock = Clock()

font: Font = Font(size = 20)
# ---

player: Pacman = None
ghosts: list[Ghost] = []
def init():
	global player, ghosts, paused

	Entity.entities.clear()
	paused = False

	# player
	player = Pacman(maze, pos = Vector2(maze.CELL_W, maze.CELL_H))

	# ghost
	ghosts.clear()
	for i in range(3):
		pos: Vector2 = Vector2(-1, -1)
		while pos == Vector2(-1, -1) or maze.is_in_wall(pos + Vector2(Ghost.GHOST_SIZE/2, Ghost.GHOST_SIZE/2)):
			pos = Vector2(randint(0, game_w - Ghost.GHOST_SIZE), randint(0, game_h - Ghost.GHOST_SIZE))
		ghosts.append(Ghost(maze, player, pos))

	# dots
	for i in range(0, maze.rows):
		for j in range(0, maze.cols):
			if (maze.grid[i][j] == maze.FREE):
				SmallDot(player, pos = Vector2((j + 0.5) * maze.CELL_W, (i + 0.5) * maze.CELL_H))

def handle_events():
	global win_w, win_h
	for e in pygame.event.get():
		if   e.type == pygame.QUIT: return True
		elif e.type == pygame.VIDEORESIZE:
			win_w = e.dict["w"]
			win_h = e.dict["h"]

def process():
	global player, curr_step

	delta: float = clock.get_time() / 1000
	keys: list[bool] = pygame.key.get_pressed()

	if (not paused):
		for e in Entity.entities:
			e.process(delta, keys)

	# lose
	for ghost in ghosts:
		if (ghost.pos.distance_squared_to(player.pos) < ((ghost.GHOST_SIZE + player.PLAYER_SIZE)/2)**2):
			pygame.time.wait(GAME_OVER_TIME)
			init()

def draw(win, scr):
	global win_w, win_h, game_w, game_h, maze
	scr.fill(BG_COLOR)

	# draw maze
	scr.blit(maze.tex, (0, 0))

	# draw entities
	for e in Entity.entities:
		e.draw(scr)

	# draw score
		scr.blit(font.render(str(player.score), False, Color(255, 255, 255), OBSTACLE_COLOR), (1, 1))

	# blit game screen to window and flip
	win.fill(BORDER_COLOR)

	dst_w: int = 0
	dst_h: int = 0
	if ((win_w/win_h) > (game_w/game_h)):
		dst_h = win_h
		dst_w = game_w * (win_h/game_h)
	else:
		dst_w = win_w
		dst_h = game_h * (win_w/game_w)

	scr = pygame.transform.scale(scr, (dst_w, dst_h))

	win.blit(scr, Rect((win_w - dst_w)/2, (win_h - dst_h)/2, dst_w, dst_h))
	pygame.display.flip()

# main loop
init()
while True:
	clock.tick(FPS)

	if (handle_events()): break # handle_events returns True when quitting

	process()
	draw(win, scr)

# quit
pygame.quit()

