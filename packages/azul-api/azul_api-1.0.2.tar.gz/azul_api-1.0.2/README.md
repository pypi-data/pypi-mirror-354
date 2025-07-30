# AzulApi

A API for Azul board game.

Original game: [https://en.wikipedia.org/wiki/Azul_(board_game)](Azul).

Library used: [![GitHub](https://img.shields.io/badge/GitHub-EvalVis/AzulGameEngine-black?style=flat&logo=github)](https://github.com/EvalVis/AzulGameEngine).

## Installing the project

Inside the directory this file is located in, run `pip install .`.

## Running the project

After installing the project run `python azul_api/main.py <number of players from 2 to 4>` from the directory this file is in.

## Functionality

To access the functionality documentation please run the service and visit `/docs` endpoint.

Alternatively read `main.py` which has Swagger documentation.

## Notes

`K` or `k` represents the black colour.

A wall cell filled with a lowercase letter means tile is not placed.

Example: `k` means can be placed on the wall cell but currently is not. `K` means black tile is placed on the wall cell.

## License

Please read a `LICENSE` file.