from typing import List

class Mapa:
    def __init__(self):
        self.tiles: List[List[str]] = []
        self._gerar_mapa_simples()

    def _gerar_mapa_simples(self) -> None:
        mapa_simples = [
            list("##########"),
            list("#........#"),
            list("#........#"),
            list("#........#"),
            list("#........#"),
            list("#........#"),
            list("#........#"),
            list("#........#"),
            list("#........#"),
            list("##########"),
        ]
        self.tiles = mapa_simples

    def get_tile(self, x: int, y: int) -> str:
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[y]):
            return self.tiles[y][x]
        return ""  # Retorna string vazia para coordenadas fora do mapa

    def is_bloqueado(self, x: int, y: int) -> bool:
        tile = self.get_tile(x, y)
        return tile == "#"
