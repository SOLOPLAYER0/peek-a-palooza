import pgzrun
import pygame
import os

TILE_SIZE = 24
WIDTH = TILE_SIZE * 25
HEIGHT = TILE_SIZE * 25

tiles = ['empty', 'wall', 'goal', 'door', 'key']
unlock = 0

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,0,0,1,1,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1],
    [1,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1],
    [1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1],
    [1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,2,0,0,0,0,3,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,1],
    [1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

player = Actor("player", anchor=(0, 0), pos=(1 * TILE_SIZE, 1 * TILE_SIZE))
enemy = Actor("enemy", anchor=(0, 0), pos=(22 * TILE_SIZE, 23 * TILE_SIZE))
enemy.yv = -1

def draw():

    pygame.display.set_caption('Phamtom Thief')
    screen.clear()
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[row][column]]
            screen.blit(tile, (x, y))
    player.draw()
    enemy.draw()

def player_move(key):
    row = int(player.y / TILE_SIZE)
    column = int(player.x / TILE_SIZE)
    if key == keys.UP:
        row = row - 1
    elif key == keys.DOWN:
        row = row + 1
    elif key == keys.LEFT:
        column = column - 1
    elif key == keys.RIGHT:
        column = column + 1
    tile = tiles[maze[row][column]]
    if tile == 'empty':
        x = column * TILE_SIZE
        y = row * TILE_SIZE
        animate(player, duration=0.1, pos=(x, y))
    global unlock
    if tile == 'goal':
        print("Well done")
        exit()
    elif tile == 'key':
        unlock = unlock + 1
        maze[row][column] = 0 
    elif tile == 'door' and unlock > 0:
        unlock = unlock - 1
        maze[row][column] = 0 

def enemy_move(key):
    row = int(enemy.y / TILE_SIZE)
    column = int(enemy.x / TILE_SIZE)

    if key == keys.W:
        row = row - 1
    elif key == keys.S:
        row = row + 1
    elif key == keys.A:
        column = column - 1
    elif key == keys.D:
        column = column + 1

    
    tile = tiles[maze[row][column]]
    if not tile == 'wall':
        x = column * TILE_SIZE
        y = row * TILE_SIZE
        animate(enemy, duration=0.1, pos=(x, y))
    
    if enemy.colliderect(player):
        print("You died")
        exit()

def on_key_down(key):
   
    player_move(key)


    enemy_move(key)


os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()