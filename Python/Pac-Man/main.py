import pygame
import sys

from ecs import *
from sprites import *
from movement import *

from pygame.math import *
from pygame import Rect
from pygame import Color, Surface
from pygame.time import Clock

from movable import Movable
from maze import Maze

from random import randint

# globals
FPS: int = 60
WIN_TITLE: str = ":3"

game_w: int = 128
game_h: int = 128

win_w: int = 480
win_h: int = 480

BG_COLOR: Color = Color(5, 5, 20)
BORDER_COLOR: Color = Color(0, 0, 0)
OBSTACLE_COLOR: Color = Color(10, 10, 100)

maze_file = sys.argv[1] if (len(sys.argv) > 1) else "maps/maze.csv"
with open(maze_file, 'r') as f:
	maze = Maze.from_csv(f.read(), game_w, game_h)

# player
PLAYER_COLOR: Color = Color(255, 255, 0)
PLAYER_SIZE: float = maze.col_size/2
PLAYER_SPEED: float = 64

#player: Movable = Movable(pos = Vector2(maze.col_size + PLAYER_SIZE, maze.row_size + PLAYER_SIZE), vel = Vector2(10, 0))
player_mover = Mover(vel = Vector2(0, 0))
player: Entity = Entity(pos = Vector2(maze.col_size + PLAYER_SIZE, maze.row_size + PLAYER_SIZE), components = [
	player_mover,
	CircleSprite(radius = PLAYER_SIZE, color = PLAYER_COLOR),
])

# ghost
ghosts: list[Movable] = [Movable(pos = Vector2(randint(0, int(maze.cols * maze.col_size)), randint(0, int(maze.rows * maze.row_size)))) for _ in range(3)]

# setup pygame
pygame.init()

win: Surface = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
scr: Surface = Surface((game_w, game_h))

pygame.display.set_caption(WIN_TITLE)
clock: Clock = Clock()
# ---

def handle_events():
	global win_w, win_h
	for e in pygame.event.get():
		if   e.type == pygame.QUIT: return True
		elif e.type == pygame.VIDEORESIZE:
			win_w = e.dict["w"]
			win_h = e.dict["h"]

def process():
	global player, player_mover, curr_step
	dt: float = clock.get_time() / 1000

	dir: Vector2 = Vector2(int(pygame.key.get_pressed()[pygame.K_d]) - int(pygame.key.get_pressed()[pygame.K_a]),
	                       int(pygame.key.get_pressed()[pygame.K_s]) - int(pygame.key.get_pressed()[pygame.K_w]))
	player_mover.vel = PLAYER_SPEED * (dir.normalize() if (dir) else Vector2(0, 0))

	player.process(dt)

	# update pos
	#next_pos = player.pos + player_mover.vel * dt
	#if (maze.is_in_wall(next_pos)):
	#	player.pos = next_pos

	# ghost
	for ghost in ghosts:
		ghost.vel = player.pos - ghost.pos
		ghost.vel = ghost.vel.normalize() if (ghost.vel) else Vector2(0, 0)
		ghost.vel *= PLAYER_SPEED * 0.5
		next_ghost_pos = ghost.pos + ghost.vel * dt
		if (maze.is_in_wall(next_ghost_pos)):
			ghost.pos += ghost.vel * dt
		

def draw(win, scr):
	global win_w, win_h, game_w, game_h, maze
	scr.fill(BG_COLOR)

	# draw maze
	scr.blit(maze.tex, (0, 0))

	player.draw(scr)

	# draw ghost
	for ghost in ghosts:
		pygame.draw.circle(scr, Color(255, 0, 0), tuple(ghost.pos), PLAYER_SIZE)

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
while True:
	clock.tick(FPS)

	if (handle_events()): break # handle_events returns True when quitting

	process()
	draw(win, scr)

# quit
pygame.quit()

