from irobot_iris_test import *

SIZE = 3
CELL_SIZE = 55
ERROR = 2

CELL_WIDTH = CELL_SIZE - ERROR
HALF_CELL_TIME = 1

STEER_LEFT = True
STRAIGHT = True

def steer(ack=True):

    global STEER_LEFT, STRAIGHT
    if ack:
        print "Steering..."

    if STEER_LEFT:
        execute(get_left_command(90 - ERROR, 25))
    else:
        execute(get_right_command(90 - ERROR, 25))

    STEER_LEFT = (not STEER_LEFT)
    STRAIGHT = (not STRAIGHT)

    if ack:
        get_sensor_value()
        print "Steer_complete."

def get_steer_command(steer_left, angle=90, speed=25 ):

    if steer_left:
        return get_left_command(angle - ERROR, speed)
    else:
        return get_right_command(angle - ERROR, speed)




def get_cells_travelled(t):
    c = int(t/(2*HALF_CELL_TIME))
    if c < SIZE:
        return c
    else:
        return SIZE -1


def move_forward():
    t = get_bump_time();
    print "Bump_time: ", t
    return get_cells_travelled(t);


def solve_maze ():

    global STRAIGHT
    maze = [[0 for x in range (0,SIZE)] for x in range(0,SIZE)]
    maze[0][0] = 1
    curr = [0,0]
    while not (curr[0] == 2 and curr[1] == 2):
        c = move_forward()
        print
        print curr, c, STRAIGHT

        print
        for x in maze:
            print x


        if c > 0:
            for x in range(c):
                # if direction of i-robot is straight
                # we increment row, else increment column
                if STRAIGHT:
                    curr[0] += 1
                else:
                    curr[1] += 1

                maze[curr[0]][curr[1]] = 1
        steer()

    for x in maze:
        print x

    sleep(5)
    solve_fast(maze)


def get_next(maze, curr, straight):
    if curr[0] == 2 and curr[1] == 2:
        return 0
    c = 0
    if straight:
        while (curr[0] + c) < SIZE and maze[curr[0] + c][curr[1]] == 1:
            c += 1
    else:
        while (curr[1] + c) < SIZE and maze[curr[0]][curr[1] + c] == 1:
            c += 1
    return c-1





def solve_fast(maze):

    straight = True
    steer_left = True

    curr = [0,0]
    cmd = ""
    while not (curr[0] == 2 and curr[1] == 2):
        print curr
        c = get_next(maze, curr, straight)
        if c > 0:
            print "Straight ", c
            # execute(get_forward_command(c*(CELL_WIDTH), 50))
            cmd += get_forward_command(c*(CELL_WIDTH), 50) + " "
            if straight:
                curr[0] += c
            else:
                curr[1] += c

        # steer()
        cmd += get_steer_command(steer_left) + " "
        print straight, steer_left
        straight = not straight
        steer_left = not steer_left

        # sleep(1)

    cmd = cmd.rstrip()
    print cmd
    execute (cmd)
    print "Solving fast"


# solve_fast([[1,0,0],[1,1,1],[0,0,1]])
solve_maze()
