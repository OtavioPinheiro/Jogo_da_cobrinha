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
VELOCIDADE = 40

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
                if event.key == pygame.K_a:
                    self.direcao = Direcao.ESQUERDA
                elif event.key == pygame.K_d:
                    self.direcao = Direcao.ESQUERDA
                elif event.key == pygame.K_w:
                    self.direcao = Direcao.CIMA
                elif event.key == pygame.K_s:
                    self.direcao = Direcao.BAIXO

        # 2. mover

        # 3. checar se o jogo acabou

        # 4. posicionar nova comida ou só mover

        # 5. atualizar o ui e o clock
        self._update_ui()
        self.clock.tick(VELOCIDADE)

        # 6. retornar para game over e pontuação
        game_over = False
        return game_over, self.pontuacao

    def _update_ui(self):
        self.tela.fill(BLACK)

        for pt in self.cobra:
            pygame.draw.rect(self.tela, BLUE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.tela, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.tela, RED, pygame.Rect(self.comida.x, self.comida.y, BLOCK_SIZE, BLOCK_SIZE))

        texto = font.render("Pontuação: " + str(self.pontuacao), True, WHITE)
        self.tela.blit(texto, [0, 0])
        pygame.display.flip()

if __name__ == '__main__':
    jogo = JogoDaCobrinha()

    # O jogo fica em um laço
    while True:
        game_over, pontuacao = jogo.etapas()

        if game_over == True:
            break
    print('Pontuação Final', pontuacao)

    # saí do laço quando der game over
    pygame.quit()
