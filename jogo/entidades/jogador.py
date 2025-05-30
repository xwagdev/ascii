class PersonagemEmoji: # Renomeado de Jogador
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.hp: int = 150
        self.ataque: int = 10
        self.simbolo: str = "🛡️"  # Emoji para o Knight/Jogador
        self.hp_emoji: str = "❤️"    # Emoji para HP
        self.ataque_emoji: str = "⚔️" # Emoji para Ataque

    def mover(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
