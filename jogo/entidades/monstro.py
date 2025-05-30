from typing import List
# Importa a classe PersonagemEmoji do módulo jogador
from jogo.entidades.jogador import PersonagemEmoji


class MonstroEmoji:  # Renomeado de Monstro
    def __init__(self, x: int, y: int, simbolo: str, hp: int, ataque: int):
        self.x: int = x
        self.y: int = y
        self.simbolo: str = simbolo
        self.hp: int = hp
        self.ataque: int = ataque

    def mover_aleatoriamente(self, mapa, jogador: PersonagemEmoji, outros_monstros: List['MonstroEmoji']) -> None:
        """Tenta mover o monstro aleatoriamente para uma casa adjacente válida."""
        import random

        tentativas_direcao = [
            (0, -1), (0, 1), (-1, 0), (1, 0),  # Cardeais
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonais
        ]
        random.shuffle(tentativas_direcao)

        for dx, dy in tentativas_direcao:
            nova_x = self.x + dx
            nova_y = self.y + dy

            # 1. Verifica se está dentro dos limites do mapa
            if not (0 <= nova_y < len(mapa.tiles) and 0 <= nova_x < len(mapa.tiles[0])):
                continue

            # 2. Verifica se é uma parede
            if mapa.is_bloqueado(nova_x, nova_y):
                continue

            # 3. Verifica se a posição está ocupada pelo jogador
            if jogador.x == nova_x and jogador.y == nova_y:
                continue

            # 4. Verifica se a posição está ocupada por outro monstro
            ocupado_por_outro_monstro = False
            for outro_monstro in outros_monstros:
                if outro_monstro is self:  # Não verifica colisão consigo mesmo
                    continue
                if outro_monstro.x == nova_x and outro_monstro.y == nova_y:
                    ocupado_por_outro_monstro = True
                    break
            if ocupado_por_outro_monstro:
                continue
            
            # Se todas as verificações passaram, move o monstro
            self.x = nova_x
            self.y = nova_y
            return  # Movido com sucesso


class RatoEmoji(MonstroEmoji):  # Renomeado de Rato e herda de MonstroEmoji
    def __init__(self, x: int, y: int):
        # Alterado o símbolo para o emoji de rato e garante herança de MonstroEmoji
        super().__init__(x=x, y=y, simbolo='🐀', hp=5, ataque=2)
