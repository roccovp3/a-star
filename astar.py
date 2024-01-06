from queue import PriorityQueue
from PIL import Image
import numpy as np

def main():
    img_array = parse_maze('maze.bmp')
    print(img_array)

    start = (0, 0)
    goal = (0, 0)

    j = 0
    while j < len(img_array[0]):
        if img_array[0][j]:
            start = (0, j)
        j += 1

    j = 0
    while j < len(img_array[-1]):
        if img_array[-1][j]:
            goal = (len(img_array)-1, j)
        j += 1
    
    path = a_star(start, goal, h, img_array)

    img_solved = draw_solution(img_array, path)
    img_solved.save('out.bmp')
    return img_solved

def parse_maze(img_path):
    img = Image.open(img_path)
    img_array = np.array(img)
    return img_array

def draw_solution(img_array, path):
    img_solved_data = [(0, 0, 0) for pixel in range(len(img_array)*len(img_array[0]))]
    for i in range(len(img_array)):
        for j in range(len(img_array[0])):
            if img_array[i][j]:
                img_solved_data[len(img_array[0])*i+j] = (255, 255, 255)
            else:
                img_solved_data[len(img_array[0])*i+j] = (0, 0, 0)
            if (i, j) in path:
                img_solved_data[len(img_array[0])*i+j] = (0, 255, 0)
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

def a_star(start, goal, h, img_array):
    open_set = PriorityQueue()
    priority = 0
    open_set.put((priority, start))
    priority += 1
    came_from = {}

    g_score = {}
    f_score = {}
    for i, row in enumerate(img_array):
        for j, col in enumerate(img_array[i]):
            if col == True:
                g_score[(i,j)] = 2**32-1
                f_score[(i,j)] = 2**32-1

    g_score[start] = 0
    f_score[start] = h(start, goal)

    while open_set.empty() == False:
        
        current = open_set.get()[1]
        if current == goal:
            return reconstruct_path(came_from, current)
        
        current_neighbors = []

        i = current[0]
        j = current[1]

        if j < len(img_array[0])-1:
            if img_array[i][j+1]:
                current_neighbors.append((i, j+1))
        if j > 0:
            if img_array[i][j-1]:
                current_neighbors.append((i, j-1))
        if i < len(img_array)-1:
            if img_array[i+1][j]:
                current_neighbors.append((i+1, j))
        if i > 0:
            if img_array[i-1][j]:
                current_neighbors.append((i-1, j))
        
        for neighbor in current_neighbors:
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