import random # Adicionado para movimento aleatório do monstro
from jogo.mapa.mapa import Mapa
from jogo.entidades.jogador import Jogador
from jogo.entidades.monstro import Monstro, Rato # Importar Rato
from typing import List

class MotorJogo:
    def __init__(self):
        self.mapa: Mapa = Mapa()
        self.jogador: Jogador = Jogador(x=1, y=1) # Posição inicial do jogador
        self.monstros: List[Monstro] = [] # Lista para armazenar monstros

        # Instanciar monstros e adicioná-los à lista
        rato1 = Rato(x=5, y=5)
        rato2 = Rato(x=7, y=7)
        self.monstros.append(rato1)
        self.monstros.append(rato2)

    def _get_monstro_em(self, x: int, y: int) -> Monstro | None:
        """Retorna o monstro na posição (x,y) ou None se não houver."""
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
                # Agora, em vez de apenas bloquear, informamos que pode atacar
                print(f"Um {monstro_na_posicao.simbolo} bloqueia o caminho! Use 'x' para atacar.")

    def tentar_atacar(self) -> None:
        """Tenta atacar um monstro adjacente."""
        atacou_neste_turno = False
        # Itera sobre as 8 posições adjacentes (incluindo diagonais)
        for dy_adj in range(-1, 2): # Renomeado para evitar conflito com dx, dy de mover_jogador
            for dx_adj in range(-1, 2): # Renomeado para evitar conflito
                if dx_adj == 0 and dy_adj == 0: # Pula a própria posição do jogador
                    continue

                adj_x: int = self.jogador.x + dx_adj
                adj_y: int = self.jogador.y + dy_adj
                
                monstro_encontrado = self._get_monstro_em(adj_x, adj_y)

                if monstro_encontrado:
                    monstro_encontrado.hp -= self.jogador.ataque
                    print(f"Você ataca o {monstro_encontrado.simbolo} causando {self.jogador.ataque} de dano!")
                    
                    if monstro_encontrado.hp <= 0:
                        print(f"O {monstro_encontrado.simbolo} morreu!")
                        self.monstros.remove(monstro_encontrado)
                    
                    atacou_neste_turno = True
                    return # Ataca apenas um monstro por turno
        
        if not atacou_neste_turno:
            print("Nada para atacar aqui.")

    def turno_dos_monstros(self) -> bool:
        """Processa o turno de cada monstro. Retorna False se o jogador morrer."""
        for monstro in list(self.monstros): # Itera sobre uma cópia da lista
            if monstro.hp <=0: # Monstro pode ter morrido no mesmo turno (ex: ataque do jogador)
                if monstro in self.monstros: # Garante que não foi removido
                     self.monstros.remove(monstro)
                continue

            # Verifica se o jogador está adjacente ao monstro
            jogador_adjacente = False
            for dy_adj in range(-1, 2): # Renomeado
                for dx_adj in range(-1, 2): # Renomeado
                    if dx_adj == 0 and dy_adj == 0:
                        continue
                    if self.jogador.x == monstro.x + dx_adj and self.jogador.y == monstro.y + dy_adj:
                        jogador_adjacente = True
                        break
                if jogador_adjacente:
                    break
            
            if jogador_adjacente:
                self.jogador.hp -= monstro.ataque
                print(f"O {monstro.simbolo} ataca você causando {monstro.ataque} de dano!")
                if self.jogador.hp <= 0:
                    print("Você morreu! Fim de Jogo.") # Mensagem aqui
                    return False # Jogador morreu
            else:
                # Movimento aleatório do monstro (Bônus)
                # Passa o mapa, o jogador e a lista de outros monstros para verificação de colisão
                monstro.mover_aleatoriamente(self.mapa, self.jogador, self.monstros)
        return True # Jogador continua vivo


    def renderizar(self) -> None:
        # Limpa a tela (simplesmente imprime muitas linhas em branco)
        print("\n" * 30)

        # Renderiza o mapa
        for y, linha in enumerate(self.mapa.tiles):
            linha_renderizada: str = ""
            for x, tile in enumerate(linha):
                # Verifica se há um monstro nesta posição
                monstro_na_posicao = self._get_monstro_em(x,y)

                if self.jogador.x == x and self.jogador.y == y:
                    linha_renderizada += self.jogador.simbolo
                elif monstro_na_posicao:
                    linha_renderizada += monstro_na_posicao.simbolo
                else:
                    linha_renderizada += tile
            print(linha_renderizada)

        # Informações adicionais
        print(f"\nJogador HP: {self.jogador.hp} Ataque: {self.jogador.ataque}")
        for i, monstro in enumerate(self.monstros):
            print(f"Monstro {i+1} ({monstro.simbolo}): HP {monstro.hp} Ataque: {monstro.ataque} @ ({monstro.x},{monstro.y})")

        print(f"\nPosição do Jogador: ({self.jogador.x}, {self.jogador.y})")
        print("Use 'w', 'a', 's', 'd' para mover, 'q' para sair.")

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
            elif comando == 'x': # Novo comando para atacar
                self.tentar_atacar()
            elif comando == '': # Permite renderizar novamente ao pressionar Enter
                pass
            else:
                print("Comando inválido!")

            if self.jogador.hp <= 0:
                # Esta verificação é para o caso do jogador morrer por alguma ação própria (raro neste contexto)
                # A morte principal pelo ataque dos monstros é verificada após turno_dos_monstros
                print("Você morreu! Fim de Jogo.")
                rodando = False
                # Não precisa de 'continue' aqui pois o loop vai parar

            if rodando: # Só executa o turno dos monstros se o jogo ainda estiver rodando
                jogador_ainda_vivo = self.turno_dos_monstros()
                if not jogador_ainda_vivo:
                    # A mensagem "Você morreu! Fim de Jogo." já foi impressa por turno_dos_monstros
                    rodando = False

        print("Jogo encerrado.")
