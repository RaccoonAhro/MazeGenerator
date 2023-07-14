import pygame
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (114, 176, 131)
ORANGE= (235, 171, 52)
WINERED=(74, 1, 32)

WIDTH=HEIGHT=10
MARGIN=2
maze_color=WINERED
speed=240
grid_length=grid_height=80

pygame.init()

print('Maze starting up...')

pygame.display.set_caption('Maze generator')
done = False
clock = pygame.time.Clock()

position_x=0
position_y=0
spaces_finished=0
path=['']

grid=[]
temp=[]
for y in range(0, grid_length):
    for x in range(0, grid_height):
        temp.append(['U','D','L','R'])
        if x==0:
            temp[x].remove('L')
        if y==0:
            temp[x].remove('U')
        if x==grid_length-1:
            temp[x].remove('R')
        if y==grid_height-1:
            temp[x].remove('D')
    grid.append(temp)
    temp=[]

WINDOW_SIZE= [len(grid)*(HEIGHT+MARGIN)+MARGIN,len(grid[0])*(WIDTH+MARGIN)+MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)
neighbors_visited=[]
for y in range(0, grid_height):
    temp_neighbors=[]
    for x in range(0, grid_length):
        temp_neighbors.append(False)
    neighbors_visited.append(temp_neighbors)        

def step(x_step,y_step):
    directions = []
    possible_moves=grid[y_step][x_step]
    if possible_moves.count('D')==1 and path[-1]!='up':
        if space_visited[y_step+1][x_step]!=True:
            directions.append('down')
    if possible_moves.count('U')==1 and path[-1]!='down':
        if space_visited[y_step-1][x_step]!=True:
            directions.append('up')
    if possible_moves.count('L')==1 and path[-1]!='right':
        if space_visited[y_step][x_step-1]!=True:
            directions.append('left')
    if possible_moves.count('R')==1 and path[-1]!='left':
        if space_visited[y_step][x_step+1]!=True:
            directions.append('right')
    if len(directions)==0:
        return False
    choice = random.choice(directions)
    return choice

def update_grid(x_grid,y_grid):
    space_visited[y_grid][x_grid]=True
    
    right_visited=False
    left_visited=False
    down_visited=False
    up_visited=False

    possible_moves=grid[y_grid][x_grid]
    if possible_moves.count('D')==1:
        if space_visited[y_grid+1][x_grid]==True:
            down_visited=True
    else:
        down_visited='invalid'
    
    if possible_moves.count('U')==1:
        if space_visited[y_grid-1][x_grid]==True:
            up_visited=True
    else: 
        up_visited='invalid'

    if possible_moves.count('L')==1:
        if space_visited[y_grid][x_grid-1]==True:
            left_visited=True
    else: 
        left_visited='invalid'
    
    if possible_moves.count('R')==1:
        if space_visited[y_grid][x_grid+1]==True:
            right_visited=True
    else: 
        right_visited='invalid'

    if right_visited!=False and down_visited!=False and left_visited!=False and up_visited!=False:
        neighbors_visited[y_grid][x_grid]=True

    for row in range(grid_height):
        for column in range(grid_length):
            color=WHITE
            if neighbors_visited[row][column]==True:
                color=maze_color
            elif space_visited[row][column]==True:
                color=GREEN
            if row==y_grid and column==x_grid:
                color=ORANGE
            pygame.draw.rect(screen,
                            color,
                            [(MARGIN + WIDTH) * column + MARGIN,
                            (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH,
                            HEIGHT])
        pygame.display.flip()

space_visited=[]
for y in range(0, grid_height):
    empty_grid_temp=[]
    for x in range(0, grid_length):
        empty_grid_temp.append('')
    space_visited.append(empty_grid_temp)

#space_visited is for if the space has been visited once
#grid is for the possible movement choices at the generation of the maze
#neighbors_visited is for when all the neighbors of a space have been visited

space_visited[0][0]=True
screen.fill(WHITE)

for i in range(0, grid_height):
    for j in range(0, grid_length):
        clock.tick(speed)
        if neighbors_visited[position_y][position_x]==True:
            if done==True:
                break
            while neighbors_visited[position_y][position_x]==True:
                if spaces_finished>=(grid_length*grid_height-1):
                    done=True
                    break
                if path[-1]=='up':
                    path.pop()
                    pygame.draw.line(screen, maze_color, (position_x*(WIDTH+MARGIN), position_y*(HEIGHT+MARGIN)+HEIGHT+MARGIN), (position_x*(WIDTH+MARGIN)+WIDTH+MARGIN, position_y*(HEIGHT+MARGIN)+HEIGHT+MARGIN), 2)
                    position_y+=1
                    spaces_finished+=1
                    update_grid(position_x,position_y)
                elif path[-1]=='down':
                    path.pop()
                    pygame.draw.line(screen, maze_color, (position_x*(WIDTH+MARGIN), position_y*(HEIGHT+MARGIN)), (position_x*(WIDTH+MARGIN)+WIDTH+MARGIN, position_y*(HEIGHT+MARGIN)), 2)
                    position_y-=1
                    spaces_finished+=1
                    update_grid(position_x,position_y)
                elif path[-1]=='left':
                    path.pop()
                    pygame.draw.line(screen, maze_color, (position_x*(WIDTH+MARGIN)+WIDTH+MARGIN, position_y*(HEIGHT+MARGIN)), (position_x*(WIDTH+MARGIN)+WIDTH+MARGIN, position_y*(HEIGHT+MARGIN)+HEIGHT+MARGIN), 2)
                    position_x+=1
                    spaces_finished+=1
                    update_grid(position_x,position_y)
                elif path[-1]=='right':
                    path.pop()
                    pygame.draw.line(screen, maze_color, (position_x*(WIDTH+MARGIN), position_y*(HEIGHT+MARGIN)), (position_x*(WIDTH+MARGIN), position_y*(HEIGHT+MARGIN)+HEIGHT+MARGIN), 2)
                    position_x-=1
                    spaces_finished+=1
                    update_grid(position_x,position_y)
                update_grid(position_x,position_y)
                pygame.event.pump()
        choice=step(position_x,position_y)
        path.append(choice)
        pygame.event.pump()
        if choice == 'up':
            position_y-=1
            update_grid(position_x,position_y)
        elif choice == 'down':
            position_y+=1
            update_grid(position_x,position_y)
        elif choice == 'left':
            position_x-=1
            update_grid(position_x,position_y)
        elif choice == 'right':
            position_x+=1
            update_grid(position_x,position_y)
        elif choice==False:
            break

print('Maze generation complete.')

running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
