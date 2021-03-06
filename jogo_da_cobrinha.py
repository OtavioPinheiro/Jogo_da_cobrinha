import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
# font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)


class Direcao(Enum):
    DIREITA = 1
    ESQUERDA = 2
    CIMA = 3
    BAIXO = 4


Ponto = namedtuple('Ponto', 'x, y')


# cores RGB
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
VELOCIDADE = 5

class JogoDaCobrinha:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # inicializar a tela
        self.tela = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Cobrinha')
        self.clock = pygame.time.Clock()

        # inicializar o estado do jogo
        self.direcao = Direcao.DIREITA

        self.cabeca = Ponto(self.w / 2, self.h / 2)
        self.cobra = [self.cabeca,
                      Ponto(self.cabeca.x - BLOCK_SIZE, self.cabeca.y),
                      Ponto(self.cabeca.x - (2*BLOCK_SIZE), self.cabeca.y)]
        self.pontuacao = 0
        self.comida = None
        self.velocidade = VELOCIDADE
        self._posicionar_comida()

    def _posicionar_comida(self):
        x = random.randint(0, (self.w - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.comida = Ponto(x, y)
        if self.comida in self.cobra:
            self._posicionar_comida()

    def etapas(self):
        # 1. entrada do usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if self.direcao == Direcao.DIREITA or self.direcao == Direcao.ESQUERDA:
                    if event.key == pygame.K_UP:
                        self.direcao = Direcao.CIMA
                    elif event.key == pygame.K_DOWN:
                        self.direcao = Direcao.BAIXO
                elif self.direcao == Direcao.CIMA or self.direcao == Direcao.BAIXO:
                    if event.key == pygame.K_RIGHT:
                        self.direcao = Direcao.DIREITA
                    elif event.key == pygame.K_LEFT:
                        self.direcao = Direcao.ESQUERDA

        # 2. mover
        # atualiza a cabeça
        self._mover(self.direcao)
        self.cobra.insert(0, self.cabeca)

        # 3. checar se o jogo acabou
        game_over = False
        if self._eh_colisao():
            game_over = True
            return game_over, self.pontuacao, self.velocidade

        # 4. posicionar nova comida ou só mover
        if self.cabeca == self.comida:
            self.pontuacao += 1
            self.velocidade += 1
            self._posicionar_comida()
        else:
            self.cobra.pop()

        # 5. atualizar o ui e o clock
        self._update_ui()
        self.clock.tick(self.velocidade)

        # 6. retornar se foi game over, a pontuação obtida e a velocidade atingida
        return game_over, self.pontuacao, self.velocidade

    def _eh_colisao(self):
        # bate nos limites da tela
        if self.cabeca.x > self.w - BLOCK_SIZE or self.cabeca.x < 0 or self.cabeca.y > self.h - BLOCK_SIZE or self.cabeca.y < 0:
            return True
        # bate nela mesma
        if self.cabeca in self.cobra[1:]:
            return True

        return False

    def _update_ui(self):
        self.tela.fill(BLACK)

        for pt in self.cobra:
            pygame.draw.rect(self.tela, BLUE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.tela, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.tela, RED, pygame.Rect(self.comida.x, self.comida.y, BLOCK_SIZE, BLOCK_SIZE))

        texto = font.render("Pontuação: " + str(self.pontuacao) + "     Velocidade: " + str(self.velocidade), True, WHITE)
        self.tela.blit(texto, [0, 0])
        pygame.display.flip()

    def _mover(self, direcao):
        x = self.cabeca.x
        y = self.cabeca.y
        if direcao == Direcao.DIREITA:
            x += BLOCK_SIZE
        elif direcao == Direcao.ESQUERDA:
            x -= BLOCK_SIZE
        elif direcao == Direcao.BAIXO:
            y += BLOCK_SIZE
        elif direcao == Direcao.CIMA:
            y -= BLOCK_SIZE

        self.cabeca = Ponto(x, y)

if __name__ == '__main__':
    jogo = JogoDaCobrinha()

    # O jogo fica em um laço
    while True:
        game_over, pontuacao, velocidade = jogo.etapas()

        if game_over == True:
            break
    print('Pontuação Final: --> ', pontuacao)
    print('Velocidade atingida: --> ', velocidade)

    # saí do laço quando der game over
    pygame.quit()
