import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""
# body_x_coords = [coord["x"] for coord in body]
# body_y_coords = [coord["y"] for coord in body]

def x(coord):
    return coord["x"]

def y(coord):
    return coord["y"]

class MoveBlock:
    def __init__(obj, coord, move):
        obj.x = x(coord)
        obj.y = y(coord)
        obj.move = move

class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "tywithings",
            "color": "#0093DC",
            "head": "fang",
            "tail": "hook",
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        data = cherrypy.request.json
        
        board = data["board"]
        me = data["you"]
        head = me["head"]
        body = me["body"]
        food = board["food"]
        hazards = board["hazards"]

        def top_limit():
            return board["height"] - 1

        def bottom_limit():
            return 0

        def right_limit():
            return board["height"] - 1

        def left_limit():
            return 0        

        def coord(x, y):
            return { "x": x, "y": y }

        def should_move_down():
            down_coord = coord(x(head), y(head) - 1)
            if y(down_coord) <= bottom_limit() or down_coord in body or down_coord in hazards:
                return (False, False, None)

            move_block = MoveBlock(down_coord, "down")

            if down_coord in food:
                return (True, True, move_block)

            return (True, False, move_block)

        def should_move_right():
            right_coord = coord(x(head) + 1, y(head))
            if x(right_coord) >= right_limit() or right_coord in body or right_coord in hazards:
                return (False, False, None)

            move_block = MoveBlock(right_coord, "right")

            return (True, False, move_block)

        def should_move_up():
            up_coord = coord(x(head), y(head) + 1)
            if y(up_coord) >= top_limit() or up_coord in body or up_coord in hazards:
                return (False, False, None)

            move_block = MoveBlock(up_coord, "up")

            return (True, False, move_block)

        def should_move_left():
            left_coord = coord(x(head) + 1, y(head))
            if x(left_coord) <= left_limit() or left_coord in body or left_coord in hazards:
                return (False, False, None)

            move_block = MoveBlock(left_coord, "left")

            return (True, False, move_block)

        

        possible_moves = []

        down_result = should_move_down()
        right_result = should_move_right()
        up_result = should_move_up()
        left_result = should_move_left()

        if bool(down_result[0]):
            possible_moves.append(down_result[2].move)
        if bool(right_result[0]):
            possible_moves.append(right_result[2].move)
        if bool(up_result[0]):
            possible_moves.append(up_result[2].move)
        if bool(left_result[0]):
            possible_moves.append(left_result[2].move)

        print(f"MOVES: {possible_moves}")

        

        
        # possible_moves = ["up", "down", "right", "left"]

        

        # Choose a random direction to move in from applicable moves
        move = random.choice(possible_moves)

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)


# no_up_mutilation = all(y != (head["y"] + 1) for y in body_y_coords)
#     if head["y"] < (board["height"] - 1) and no_up_mutilation :
#         possible_moves.append("up")

# no_down_mutilation = all(y != (head["y"] - 1) for y in body_y_coords)
#     if head["y"] > 0 and no_down_mutilation:
#         possible_moves.append("down")

# no_right_mutilation = all(x != (head["x"] + 1) for x in body_x_coords)
#     if head["x"] < (board["width"] - 1) and no_right_mutilation:
#         possible_moves.append("right")

# no_left_mutilation = all(x != (head["x"] - 1) for x in body_x_coords)
#     if head["x"] > 0 and no_left_mutilation:
#         possible_moves.append("left")

# food = board["food"]
#         closest = 0
#         target_bite = {}
#         for bite in food:
#           distance = abs(head["x"] - bite["x"]) + abs(head["y"] - bite["y"])

#           if closest == 0 or distance < closest:
#             closest = distance
#             target_bite = bite

#           break

#         print(f"FOOD: {food}")
#         print(f"CLOSEST: {closest}")
#         print(f"TARGET BITE: {target_bite}")

