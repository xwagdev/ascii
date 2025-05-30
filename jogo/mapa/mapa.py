from typing import List

class MapaEmoji:  # Renomeado de Mapa
    def __init__(self):
        self.tiles: List[List[str]] = []
        self._gerar_mapa_simples()

    def _gerar_mapa_simples(self) -> None:
        # Substituindo '#' por "🧱" e '.' por "🟫"
        # Construindo a lista de listas diretamente com os Emojis
        mapa_emojis = [
            ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
            ["🧱", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🧱"],
            ["🧱", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🧱"],
            ["🧱", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🧱"],
            ["🧱", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🧱"],
            ["🧱", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🧱"],
            ["🧱", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🧱"],
            ["🧱", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🧱"],
            ["🧱", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🟫", "🧱"],
            ["🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱", "🧱"],
        ]
        self.tiles = mapa_emojis

    def get_tile(self, x: int, y: int) -> str:
        if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[y]):
            return self.tiles[y][x]
        # Retorna um Emoji neutro ou vazio se fora do mapa, para evitar erros com `list()`
        return "⬛" # Um bloco preto, por exemplo, ou poderia ser ""

    def is_bloqueado(self, x: int, y: int) -> bool:
        tile = self.get_tile(x, y)
        # Modificado para verificar o novo Emoji de parede
        return tile == "🧱"
