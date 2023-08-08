"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "de best"
global routes, iterationsNum
iterationsNum = 4
routes = []
btb = [obstacles.BIKE, obstacles.TRASH, obstacles.BARRIER]
def rec_routes(x, y, route):
    global routes
    global iterationsNum
    if iterationsNum != 0:
        iterationsNum -= 1
        route.append((x, y - 1))
        rec_routes(x, y - 1, route)
        if x != 0 and x != 3:
            route.append((x - 1, y - 1))
            rec_routes(x - 1, y - 1, route)
        elif x != 2 and x != 5:
            route.append((x + 1, y - 1))
            rec_routes(x + 1, y - 1, route)

    routes.append(route)

def rec_findScore(route, world):
    try:
        score = 0
        for i in range(len(route)):
            if world.get(route[i]) in btb:
                score -= 10
            if route[i][0] < 3:
                if route[i][0] == route[i + 1][0]:
                    if world.get(route[i + 1]) == obstacles.PENGUIN:
                        score += 10
                    elif world.get(route[i + 1]) == obstacles.WATER:
                        score += 4
                    elif world.get(route[i]) == obstacles.CRACK:
                        score += 5
            elif world.get(route[i]) == obstacles.WATER or world.get(route[i]) == obstacles.CRACK:
                score -= 10
    except IndexError:
        pass
    finally:
        return score

def rec_BestRoute(world):
    global routes
    best_score = 0
    best_route = routes[0]
    for route in routes:
        findScore = rec_findScore(route, world)
        best = best_score
        print((findScore, best))
        if findScore > best:
            best_score = rec_findScore(route, world)
            best_route = route
    print(best_route)
    return best_route

def rec_turnToActions(world, best_route):
    ACTUAL_ROUTE = []
    for i in range(len(best_route)):
        if best_route[i][0] < 3:
            if best_route[i][0] == best_route[i + 1][0]:
                if world.get(best_route[i + 1]) == obstacles.PENGUIN:
                    ACTUAL_ROUTE.append(actions.PICKUP)
                elif world.get(best_route[i + 1]) == obstacles.WATER:
                    ACTUAL_ROUTE.append(actions.BRAKE)
                elif world.get(best_route[i + 1]) == obstacles.CRACK:
                    ACTUAL_ROUTE.append(actions.JUMP)
                ACTUAL_ROUTE.append(actions.NONE)
            elif best_route[i][0] == best_route[i + 1][0] + 1:
                ACTUAL_ROUTE.append(actions.RIGHT)
            elif best_route[i][0] == best_route[i + 1][0] - 1:
                ACTUAL_ROUTE.append(actions.LEFT)
        return ACTUAL_ROUTE


def drive(world):
    x = world.car.x
    y = world.car.y
    route = []
    rec_routes(x, y, route)
    best_route = rec_BestRoute(world)
    ACTUAL_ROUTE = rec_turnToActions(world, best_route)
    return ACTUAL_ROUTE[0]
