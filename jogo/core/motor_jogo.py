import random
from jogo.mapa.mapa import MapaEmoji # Atualizado
from jogo.entidades.jogador import PersonagemEmoji # Atualizado
from jogo.entidades.monstro import MonstroEmoji, RatoEmoji # Atualizado
from typing import List, Optional

class MotorJogoEmoji: # Renomeado
    def __init__(self):
        self.mapa: MapaEmoji = MapaEmoji() # Atualizado
        self.jogador: PersonagemEmoji = PersonagemEmoji(x=1, y=1) # Atualizado
        self.monstros: List[MonstroEmoji] = [] # Atualizado

        # Instanciar monstros e adicioná-los à lista
        rato1 = RatoEmoji(x=5, y=5) # Atualizado
        rato2 = RatoEmoji(x=7, y=7) # Atualizado
        self.monstros.append(rato1)
        self.monstros.append(rato2)

    def _get_monstro_em(self, x: int, y: int) -> Optional[MonstroEmoji]:
        for monstro in self.monstros:
            if monstro.x == x and monstro.y == y:
                return monstro
        return None

    def mover_jogador(self, dx: int, dy: int) -> None:
        nova_x: int = self.jogador.x + dx
        nova_y: int = self.jogador.y + dy

        if not self.mapa.is_bloqueado(nova_x, nova_y):
            monstro_na_posicao = self._get_monstro_em(nova_x, nova_y)
            if monstro_na_posicao is None:
                self.jogador.mover(dx, dy)
            else:
                # Atualizado com Emoji do monstro
                print(f"Um {monstro_na_posicao.simbolo} bloqueia o caminho! Use 'x' para atacar.")

    def tentar_atacar(self) -> None:
        atacou_neste_turno = False
        for dy_adj in range(-1, 2):
            for dx_adj in range(-1, 2):
                if dx_adj == 0 and dy_adj == 0:
                    continue
                adj_x: int = self.jogador.x + dx_adj
                adj_y: int = self.jogador.y + dy_adj
                monstro_encontrado = self._get_monstro_em(adj_x, adj_y)

                if monstro_encontrado:
                    # Atualizado com Emojis
                    print(f"Você {self.jogador.ataque_emoji} ataca o {monstro_encontrado.simbolo} causando {self.jogador.ataque} de dano!")
                    monstro_encontrado.hp -= self.jogador.ataque
                    
                    if monstro_encontrado.hp <= 0:
                        # Atualizado com Emoji
                        print(f"O {monstro_encontrado.simbolo} morreu! 💀")
                        self.monstros.remove(monstro_encontrado)
                    
                    atacou_neste_turno = True
                    return 
        
        if not atacou_neste_turno:
            print("Nada para atacar aqui.")

    def turno_dos_monstros(self) -> bool:
        for monstro in list(self.monstros): 
            if monstro.hp <=0: 
                if monstro in self.monstros: 
                     self.monstros.remove(monstro)
                continue

            jogador_adjacente = False
            for dy_adj in range(-1, 2): 
                for dx_adj in range(-1, 2): 
                    if dx_adj == 0 and dy_adj == 0:
                        continue
                    if self.jogador.x == monstro.x + dx_adj and self.jogador.y == monstro.y + dy_adj:
                        jogador_adjacente = True
                        break
                if jogador_adjacente:
                    break
            
            if jogador_adjacente:
                # Atualizado com Emojis
                print(f"O {monstro.simbolo} ⚔️  ataca você {self.jogador.simbolo} causando {monstro.ataque} de dano!")
                self.jogador.hp -= monstro.ataque
                if self.jogador.hp <= 0:
                    # Atualizado com Emojis
                    print(f"Você {self.jogador.simbolo} morreu! 💀 Fim de Jogo.")
                    return False 
            else:
                monstro.mover_aleatoriamente(self.mapa, self.jogador, self.monstros)
        return True 


    def renderizar(self) -> None:
        print("\n" * 30) 

        for y, linha in enumerate(self.mapa.tiles):
            linha_renderizada: str = ""
            for x, tile in enumerate(linha):
                monstro_na_posicao = self._get_monstro_em(x,y)

                if self.jogador.x == x and self.jogador.y == y:
                    linha_renderizada += self.jogador.simbolo + " " # Adicionado espaço
                elif monstro_na_posicao:
                    linha_renderizada += monstro_na_posicao.simbolo + " " # Adicionado espaço
                else:
                    linha_renderizada += tile + " " # Adicionado espaço
            print(linha_renderizada)

        # Atualizado com Emojis e atributos de PersonagemEmoji
        print(f"\nJogador {self.jogador.simbolo} {self.jogador.hp_emoji} HP: {self.jogador.hp} {self.jogador.ataque_emoji} Ataque: {self.jogador.ataque}")
        for i, monstro in enumerate(self.monstros):
            # Atualizado com Emojis
            print(f"Monstro {monstro.simbolo} ❤️ HP: {monstro.hp} ⚔️ Ataque: {monstro.ataque} @ ({monstro.x},{monstro.y})")

        print(f"\nPosição do Jogador: ({self.jogador.x}, {self.jogador.y})")
        print("Use 'w', 'a', 's', 'd' para mover, 'x' para atacar, 'q' para sair.")

    def executar(self) -> None:
        rodando: bool = True
        while rodando:
            self.renderizar()
            comando: str = input("Comando: ").lower()

            if comando == 'q':
                rodando = False
            elif comando == 'w':
                self.mover_jogador(0, -1)
            elif comando == 's':
                self.mover_jogador(0, 1)
            elif comando == 'a':
                self.mover_jogador(-1, 0)
            elif comando == 'd':
                self.mover_jogador(1, 0)
            elif comando == 'x': 
                self.tentar_atacar()
            elif comando == '': 
                pass
            else:
                print("Comando inválido!")

            if self.jogador.hp <= 0 and rodando: # Verifica se o jogador morreu e o jogo ainda estava rodando
                # A mensagem de morte já é impressa em turno_dos_monstros ou tentar_atacar (se for o caso)
                # Garantir que o jogo pare aqui.
                rodando = False
                continue # Pula o turno dos monstros se o jogador morreu na sua própria ação ou ataque

            if rodando: 
                jogador_ainda_vivo = self.turno_dos_monstros()
                if not jogador_ainda_vivo:
                    rodando = False

        print("Jogo encerrado.")
