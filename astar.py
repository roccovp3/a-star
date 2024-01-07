from queue import PriorityQueue
from PIL import Image
import numpy as np
import pygame
import maze

pixel_size = 2

def main():
    pygame.init()

    img_array = maze.create_maze(200, 2000)
    screen = pygame.display.set_mode((pixel_size*len(img_array[0]), pixel_size*len(img_array)))
    icon_surface = pygame.image.load('map.bmp')
    pygame.display.set_caption('A*')
    pygame.display.set_icon(icon_surface)

    while True:
        gen_and_solve(screen, img_array)

def gen_and_solve(screen, img_array):

    img_solved_data = draw_maze(img_array, screen)

    start = (0, 0)
    goal = (0, 0)

    start = None
    for j in range(len(img_array[0])):
        if img_array[0][j]:
            start = (0, j)
            break
        elif img_array[j][0]:
            start = (j, 0)
            break

    goal = None
    for j in range(len(img_array[-1])):
        if img_array[-1][j] and start != (len(img_array) - 1, j):
            goal = (len(img_array) - 1, j)
            break
        elif img_array[j][-1] and start != (j, len(img_array) - 1):
            goal = (j, len(img_array) - 1)
            break
    
    path = a_star(start, goal, h, img_array, screen)

    img_solved = draw_solution(img_array, path, screen, img_solved_data)
    #img_solved.save('out.bmp')

def parse_maze(img_path):
    img = Image.open(img_path)
    img_array = np.array(img)
    return img_array

def draw_maze(img_array, screen):
    img_solved_data = [(0, 0, 0) for pixel in range(len(img_array)*len(img_array[0]))]
    for i in range(len(img_array)):
        for j in range(len(img_array[0])):
            if img_array[i][j]:
                img_solved_data[len(img_array[0])*i+j] = (255, 255, 255)
            else:
                img_solved_data[len(img_array[0])*i+j] = (0, 0, 0)
            pygame.draw.rect(screen, img_solved_data[len(img_array[0])*i+j], (pixel_size*j, pixel_size*i, pixel_size, pixel_size))
    pygame.display.update()
    return img_solved_data

def draw_solution(img_array, path, screen, img_solved_data): 
    for (i, j) in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        img_solved_data[len(img_array[0])*i+j] = (0, 255, 0)
        pygame.draw.rect(screen, (0, 255, 0), (pixel_size*j, pixel_size*i, pixel_size, pixel_size))
        pygame.display.update((pixel_size*j, pixel_size*i, pixel_size, pixel_size))
    img_solved = Image.new(mode="RGB", size=(len(img_array), len(img_array[0])))
    img_solved.putdata(img_solved_data)
    return img_solved

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

def a_star(start, goal, h, img_array, screen):
    open_set = PriorityQueue()
    priority = 0
    open_set.put((priority, start))
    priority += 1

    came_from = {}
    g_score = {}
    f_score = {}

    for i in range(len(img_array)):
        for j in range(len(img_array[i])):
            if img_array[i][j] == True:
                g_score[(i,j)] = 2**32-1
                f_score[(i,j)] = 2**32-1

    g_score[start] = 0
    f_score[start] = h(start, goal)

    while not open_set.empty():
        event_thread = 0
        current = open_set.get()[1]
        if current == goal:
            return reconstruct_path(came_from, current)

        current_neighbors = []

        i, j = current

        if j < len(img_array[0]) - 1 and img_array[i][j+1]:
            current_neighbors.append((i, j+1))
        if j > 0 and img_array[i][j-1]:
            current_neighbors.append((i, j-1))
        if i < len(img_array) - 1 and img_array[i+1][j]:
            current_neighbors.append((i+1, j))
        if i > 0 and img_array[i-1][j]:
            current_neighbors.append((i-1, j))
        
        for neighbor in current_neighbors:
            pygame.draw.rect(screen, (255, 0, 0), (pixel_size*neighbor[1], pixel_size*neighbor[0], pixel_size, pixel_size))
            tentative_g_score = g_score[current] + 1 # all edges are weight 1 here
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor, goal)
                if neighbor not in open_set.queue:
                    open_set.put((priority, neighbor))
                    priority += 1
        pygame.display.update((pixel_size*j, pixel_size*i, pixel_size, pixel_size))
        if event_thread % 60 == 0:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
    return False

if __name__ == '__main__':
    main()