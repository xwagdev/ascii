class Jogador:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.hp: int = 150  # Valor base para o Knight
        self.ataque: int = 10 # Valor base para o Knight
        self.simbolo: str = "@" # Ou '⚔️'

    def mover(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
