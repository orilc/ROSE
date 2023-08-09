from rose.common import obstacles, actions

"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "Group5"

btb = [obstacles.BIKE, obstacles.TRASH, obstacles.BARRIER]
wc = [obstacles.WATER, obstacles.CRACK]
btbwc = [obstacles.BIKE, obstacles.TRASH, obstacles.BARRIER, obstacles.WATER, obstacles.CRACK]
wcp = [obstacles.WATER, obstacles.CRACK, obstacles.PENGUIN]


def check(worlds, x, loc):
    if worlds[0][x - loc] in btb:
        return bar(worlds, x)
    elif worlds[0][x - loc] in wc:
        return wac(worlds, x, loc)
    elif worlds[0][x - loc] == obstacles.PENGUIN:
        return pickup()
    return actions.NONE


def bar(worlds, x):
    if x % 3 == 1:
        if worlds[1][2] == obstacles.PENGUIN:
            return actions.RIGHT
        if worlds[1][0] == obstacles.PENGUIN:
            return actions.RIGHT
        if worlds[2][2] == obstacles.PENGUIN:
            return actions.RIGHT
        if worlds[2][0] == obstacles.PENGUIN:
            return actions.RIGHT
        if worlds[1][2] == obstacles.CRACK:
            return actions.RIGHT
        if worlds[1][0] == obstacles.CRACK:
            return actions.LEFT
        if worlds[2][2] == obstacles.CRACK:
            return actions.RIGHT
        if worlds[2][0] == obstacles.CRACK:
            return actions.LEFT
        if worlds[1][2] == obstacles.WATER:
            return actions.RIGHT
        if worlds[1][0] == obstacles.WATER:
            return actions.LEFT
        if worlds[2][2] == obstacles.WATER:
            return actions.RIGHT
        if worlds[2][0] == obstacles.WATER:
            return actions.LEFT
        else:
            return actions.LEFT
    if x % 3 == 0:
        return actions.RIGHT
    else:
        return actions.LEFT


def wac(worlds, x, loc):
    if worlds[0][x - loc] == obstacles.CRACK:
        return actions.JUMP
    elif worlds[0][x - loc] == obstacles.WATER:
        return actions.BRAKE
    return actions.NONE


def pickup():
    return actions.PICKUP


def look_for(obs, worlds):
    if obs in worlds[1] or obs in worlds[2]:
        return True


def get_world_copy(world, x, y):
    world_copy = []
    if x < 3:
        loc = 0
    else:
        loc = 3
    for i in range(1, 4):
        wc_row = []
        for j in range(loc, loc + 3):
            wc_row.append(world.get((j, y - i)))
        world_copy.append(wc_row)
    return world_copy


def drive(world):
    x = world.car.x
    y = world.car.y
    # rout = []
    # recursive_routs(world, x, y, rout)
    # print(routes)
    # ACTUAL_ROUT = best_rout(routes)
    # for i in range(len(ACTUAL_ROUT)):
    #     return ACTUAL_ROUT[i]

    # m = lanes_map_r(world, x, y)
    # future = number_map(m)
    # after = False
    if x < 3:
        loc = 0
    else:
        loc = 3
    worlds = [[world.get((loc, y - 1)), world.get((loc + 1, y - 1)), world.get((loc + 2, y - 1))],
              [world.get((loc, y - 2)), world.get((loc + 1, y - 2)), world.get((loc + 2, y - 2))],
              [world.get((loc, y - 3)), world.get((loc + 1, y - 3)), world.get((loc + 2, y - 3))]]

    act = check(worlds, x, loc)
    if act != actions.NONE:
        return act

    if look_for(obstacles.PENGUIN, worlds):
        if x % 3 == 1:
            if worlds[1][0] == obstacles.PENGUIN and worlds[0][0] not in btb:
                return actions.LEFT
            elif worlds[1][2] == obstacles.PENGUIN and worlds[0][2] not in btb:
                return actions.RIGHT
        elif x % 3 == 0:
            if worlds[1][1] == obstacles.PENGUIN and worlds[0][1] not in btb:
                return actions.RIGHT
            elif worlds[2][2] == obstacles.PENGUIN and worlds[0][1] not in btb:
                return actions.RIGHT
        elif x % 3 == 2:
            if worlds[1][1] == obstacles.PENGUIN and worlds[0][1] not in btb:
                return actions.LEFT
            elif worlds[2][0] == obstacles.PENGUIN and worlds[0][1] not in btb:
                return actions.LEFT

    elif look_for(obstacles.CRACK, worlds):
        if x % 3 == 1:
            if worlds[1][0] == obstacles.CRACK and worlds[0][0] not in btbwc:
                return actions.LEFT
            elif worlds[1][2] == obstacles.CRACK and worlds[0][2] not in btbwc:
                return actions.RIGHT
        elif x % 3 == 0:
            if worlds[1][1] == obstacles.CRACK and worlds[0][1] not in btbwc:
                return actions.RIGHT
            elif worlds[2][2] == obstacles.CRACK and worlds[0][1] not in btbwc:
                return actions.RIGHT
        elif x % 3 == 2:
            if worlds[1][1] == obstacles.CRACK and worlds[0][1] not in btbwc:
                return actions.LEFT
            elif worlds[2][0] == obstacles.CRACK and worlds[0][1] not in btbwc:
                return actions.LEFT

    elif look_for(obstacles.WATER, worlds):
        if x % 3 == 1:
            if worlds[1][0] == obstacles.WATER and worlds[0][0] not in btbwc:
                return actions.LEFT
            elif worlds[1][2] == obstacles.WATER and worlds[0][2] not in btbwc:
                return actions.RIGHT
        elif x % 3 == 0:
            if worlds[1][1] == obstacles.WATER and worlds[0][1] not in btbwc:
                return actions.RIGHT
            elif worlds[2][2] == obstacles.WATER and worlds[0][1] not in btbwc:
                return actions.RIGHT
        elif x % 3 == 2:
            if worlds[1][1] == obstacles.WATER and worlds[0][1] not in btbwc:
                return actions.LEFT
            elif worlds[2][0] == obstacles.WATER and worlds[0][1] not in btbwc:
                return actions.LEFT

    return check(worlds, x, loc)
