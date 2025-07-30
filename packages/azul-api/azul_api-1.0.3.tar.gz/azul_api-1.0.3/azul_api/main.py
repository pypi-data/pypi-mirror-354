import sys
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from flasgger import Swagger
from azul_game_engine.action_not_allowed_exception import ActionNotAllowedException
from azul_game_engine.lid import Lid
from azul_game_engine.player import Player
from azul_game_engine.board import Board
from azul_game_engine.wall import Wall
from azul_game_engine.floor import Floor
from azul_game_engine.game import Game
from azul_game_engine.center import Center
from game_controller import GameController
from factory_taking_request import FactoryTakingRequest
from center_taking_request import CenterTakingRequest

def create_app():
    app = Flask(__name__)
    
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Azul Game API",
            "description": "An API for Azul board game",
            "version": "1.0.0",
            "contact": {
                "name": "Evaldas Visockas",
                "email": "developersediary@gmail.com"
            }
        }
    }
    
    swagger = Swagger(app, config=swagger_config, template=swagger_template)
    game_controller = GameController(create_game())

    @app.route('/show', methods=['GET'])
    def show():
        """Get game state as plain-text
        ---
        tags:
          - Azul Game
        summary: Get game state as a plain-text
        description: Returns the current game state as a plain-text string representation
        responses:
          200:
            description: Current game state
            schema:
              type: string
              example: |
                Factories: 1) 2B R Y 2) 2W 2K 3) 2R B Y 4) Y R K B 5) 2Y K W
                Center: Empty
                Player: Player 1:
                Score: 0
                Has the starting player token.
                Board:
                Pattern lines:
                E 
                E E 
                E E E 
                E E E E 
                E E E E E 
                Wall:
                b y r k w
                w b y r k
                k w b y r
                r k w b y
                y r k w b
                Floor: Empty
                Player: Player 2:
                Score: 0
                Board:
                Pattern lines:
                E 
                E E 
                E E E 
                E E E E 
                E E E E E 
                Wall:
                b y r k w
                w b y r k
                k w b y r
                r k w b y
                y r k w b
                Floor: Empty
                Bag: 16B 15Y 16R 16K 17W
                Lid: 
        """
        return game_controller.show()

    @app.route('/showJson', methods=['GET'])
    def show_json():
        """Get game state as JSON
        ---
        tags:
          - Azul Game
        summary: Get game state as JSON
        description: Returns the current game state as a JSON object containing all relevant game information
        responses:
          200:
            description: Current game state in JSON format
            schema:
              type: object
            examples:
              application/json:
                Bag:
                  B: 15
                  K: 16
                  R: 16
                  W: 17
                  Y: 16
                Center: {}
                "Factory displays":
                  - K: 1
                    W: 2
                    Y: 1
                  - K: 2
                    R: 2
                  - K: 1
                    R: 2
                    Y: 1
                  - B: 2
                    W: 1
                    Y: 1
                  - B: 3
                    Y: 1
                Lid: {}
                Players:
                  - Board:
                      Floor: []
                      "Pattern lines": [[], [], [], [], []]
                      Wall:
                        - ["b", "y", "r", "k", "w"]
                        - ["w", "b", "y", "r", "k"]
                        - ["k", "w", "b", "y", "r"]
                        - ["r", "k", "w", "b", "y"]
                        - ["y", "r", "k", "w", "b"]
                    Name: "Player 1"
                    Score: 0
                    startsRound: true
                  - Board:
                      Floor: []
                      "Pattern lines": [[], [], [], [], []]
                      Wall:
                        - ["b", "y", "r", "k", "w"]
                        - ["w", "b", "y", "r", "k"]
                        - ["k", "w", "b", "y", "r"]
                        - ["r", "k", "w", "b", "y"]
                        - ["y", "r", "k", "w", "b"]
                    Name: "Player 2"
                    Score: 0
                    startsRound: false
                isRunning: true
        """
        return game_controller.show_json()

    @app.route('/takeFromFactory', methods=['POST'])
    def take_tiles_from_factory():
        """Take tiles from factory
        ---
        tags:
          - Azul Game
        summary: Take tiles from factory
        description: Take tiles of a specific color from a factory display, drop some on the floor (if you want) and put them on a pattern line
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - factory_index
                - tile_to_take
                - tiles_to_put_on_floor
                - pattern_line_index
              properties:
                factory_index:
                  type: integer
                  description: Index of the factory display (0-based)
                  example: 0
                tile_to_take:
                  type: string
                  description: Color of tiles to take
                  enum: [RED, BLUE, YELLOW, BLACK, WHITE]
                  example: RED
                tiles_to_put_on_floor:
                  type: integer
                  description: Number of tiles to drop on floor
                  minimum: 0
                  example: 0
                pattern_line_index:
                  type: integer
                  description: Pattern line to place tiles (0-4)
                  minimum: 0
                  maximum: 4
                  example: 1
        responses:
          200:
            description: Updated game state after taking tiles (same format as /showJson)
          400:
            description: Invalid move
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Factory index must be between 0 and 5."
        """
        return game_controller.take_tiles_from_factory(FactoryTakingRequest(**request.get_json()))

    @app.route('/takeFromCenter', methods=['POST'])
    def take_tiles_from_center():
        """Take tiles from center
        ---
        tags:
          - Azul Game
        summary: Take tiles from center
        description: Take tiles of a specific color from the center area, drop some on the floor (if you want) and put them on a pattern line
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - tile_to_take
                - tiles_to_put_on_floor
                - pattern_line_index
              properties:
                tile_to_take:
                  type: string
                  description: Color of tiles to take
                  enum: [RED, BLUE, YELLOW, BLACK, WHITE]
                  example: BLUE
                tiles_to_put_on_floor:
                  type: integer
                  description: Number of tiles to drop on floor
                  minimum: 0
                  example: 1
                pattern_line_index:
                  type: integer
                  description: Pattern line to place tiles (0-4)
                  minimum: 0
                  maximum: 4
                  example: 2
        responses:
          200:
            description: Updated game state after taking tiles (same format as /showJson)
          400:
            description: Invalid move
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Can't take tile(s) from an empty center."
        """
        return game_controller.take_tiles_from_center(CenterTakingRequest(**request.get_json()))

    def handle_action_not_allowed_exception(e):
        return jsonify({"error": e.message}), 400

    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify(error=str(e)), e.code
        return jsonify(error="An unexpected error occurred"), 500

    app.register_error_handler(ActionNotAllowedException, handle_action_not_allowed_exception)
    app.register_error_handler(Exception, handle_exception)
    return app


def create_game():
    lid = Lid()
    players = []
    player_count = get_player_count()
    for i in range(player_count):
        players.append(Player(Board(wall=Wall(), floor=Floor(lid)), f"Player {i + 1}"))
    return Game(players, Center(), 0, lid)


def get_player_count():
    if len(sys.argv) < 2:
        raise RuntimeError("Please provide a player count.")
    try:
        player_count = int(sys.argv[1])
        if player_count not in {2, 3, 4}:
            raise RuntimeError("Player count must be equal to 2, 3, or 4.")
        return player_count
    except ValueError:
        raise RuntimeError("Failed to read player count.")


if __name__ == '__main__':
    app = create_app()
    app.run()
