from queue import PriorityQueue
from PIL import Image
import numpy as np
import pygame
import maze
import threading
import time
import os
import random

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = '1'
PIXEL_SIZE = 2
MAZE_SIZE = 200

def main():
    pygame.init()
    clock = pygame.time.Clock()

    maze_array = maze.create_maze(MAZE_SIZE, random.randint(0, 3000))
    screen = pygame.display.set_mode((PIXEL_SIZE*len(maze_array[0]), PIXEL_SIZE*len(maze_array)))
    icon_surface = pygame.image.load('map.bmp')
    pygame.display.set_caption('A*')
    pygame.display.set_icon(icon_surface)

    autoplay = False
    thread = start_thread(screen, autoplay)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    autoplay = not autoplay
            if event.type == pygame.MOUSEBUTTONDOWN and (not thread.is_alive()) and not autoplay:
                pygame.display.flip()
                thread = start_thread(screen, autoplay)
        if autoplay and (not thread.is_alive()):
            pygame.display.flip()
            thread = start_thread(screen, autoplay)
        pygame.display.flip()
        clock.tick(960)

def gen_and_solve(screen, maze_array, autoplay):
    
    if(autoplay):
        time.sleep(1)

    img_solved_data = draw_maze(maze_array, screen)

    start = None
    for j in range(len(maze_array[0])):
        if maze_array[0][j]:
            start = (0, j)
            break
        elif maze_array[j][0]:
            start = (j, 0)
            break

    goal = None
    for j in range(len(maze_array[-1])):
        if maze_array[-1][j] and start != (len(maze_array) - 1, j):
            goal = (len(maze_array) - 1, j)
            break
        elif maze_array[j][-1] and start != (j, len(maze_array) - 1):
            goal = (j, len(maze_array) - 1)
            break
    
    path = a_star(start, goal, h, maze_array, screen)
    draw_solution(maze_array, path, screen, img_solved_data)

def start_thread(screen, autoplay):
    maze_array = maze.create_maze(MAZE_SIZE, random.randint(0, 5000))
    thread = threading.Thread(target=gen_and_solve, args=(screen, maze_array, autoplay))
    thread.start()
    return thread

def draw_maze(maze_array, screen):
    img_solved_data = [(0, 0, 0) for pixel in range(len(maze_array)*len(maze_array[0]))]
    for i in range(len(maze_array)):
        for j in range(len(maze_array[0])):
            if maze_array[i][j]:
                img_solved_data[len(maze_array[0])*i+j] = (255, 255, 255)
            else:
                img_solved_data[len(maze_array[0])*i+j] = (0, 0, 0)
            pygame.draw.rect(screen, img_solved_data[len(maze_array[0])*i+j], (PIXEL_SIZE*j, PIXEL_SIZE*i, PIXEL_SIZE, PIXEL_SIZE))
    return img_solved_data

def draw_solution(maze_array, path, screen, img_solved_data): 
    for (i, j) in path:
        img_solved_data[len(maze_array[0])*i+j] = (0, 255, 0)
        pygame.draw.rect(screen, (0, 255, 0), (PIXEL_SIZE*j, PIXEL_SIZE*i, PIXEL_SIZE, PIXEL_SIZE))

def h(node, goal):
    # Manhattan distance heuristic
    return (abs(node[0]-goal[0]) + abs(node[1]-goal[1]))

def reconstruct_path(came_from, current):
    total_path = []
    total_path.append(current)
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def a_star(start, goal, h, maze_array, screen):
    open_set = PriorityQueue()
    priority = 0
    open_set.put((priority, start))
    priority += 1

    came_from, g_score, f_score = {}, {}, {}

    for i in range(len(maze_array)):
        for j in range(len(maze_array[i])):
            if maze_array[i][j]:
                g_score[(i,j)], f_score[(i,j)] = 2**32-1, 2**32-1

    g_score[start] = 0
    f_score[start] = h(start, goal)

    while not open_set.empty():
        current = open_set.get()[1]
        if current == goal:
            return reconstruct_path(came_from, current)

        current_neighbors = []

        i, j = current

        if j < len(maze_array[0]) - 1 and maze_array[i][j+1]:
            current_neighbors.append((i, j+1))
        if j > 0 and maze_array[i][j-1]:
            current_neighbors.append((i, j-1))
        if i < len(maze_array) - 1 and maze_array[i+1][j]:
            current_neighbors.append((i+1, j))
        if i > 0 and maze_array[i-1][j]:
            current_neighbors.append((i-1, j))
        
        for neighbor in current_neighbors:
            pygame.draw.rect(screen, (255, 0, 0), (PIXEL_SIZE*neighbor[1], PIXEL_SIZE*neighbor[0], PIXEL_SIZE, PIXEL_SIZE))
            tentative_g_score = g_score[current] + 1 # all edges are weight 1 here
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor, goal)
                if neighbor not in open_set.queue:
                    open_set.put((priority, neighbor))
                    priority += 1
    return False

if __name__ == '__main__':
    main()