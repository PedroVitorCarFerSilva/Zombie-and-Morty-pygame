#code by Iraikare
#graphics by João Ricardo

import pygame
from pygame.locals import *
import os
from random import randrange, choice
pygame.font.init()
pygame.mixer.init()
pygame.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal,'imagensjogo')
diretorio_sons = os.path.join(diretorio_principal,'sons')

LARGURA, ALTURA = 1100, 600
JANELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Zombie and Morty")

branco = (255, 255, 255)
preto = (0,0,0)
vermelho = (255, 0, 0)
marrom = (209, 169, 161)
velocidade = 40
pontos = 0
velocidade_jogo = 7

fundo = pygame.transform.scale(pygame.image.load(os.path.join(diretorio_imagens,'cenario1f.png')), (LARGURA, ALTURA))
spritesheet = pygame.image.load(os.path.join(diretorio_imagens,'tudinho.png')).convert_alpha()

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons,'gameover1.wav'))
som_colisao.set_volume(0.2)
som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons,'score.wav'))
som_pontuacao.set_volume(0.2)

start = False
colidiu = False
escolha_obstaculo = choice([0,1,2])
fimdejogo = False

FONTE = pygame.font.SysFont('biome', 35)
FONTE2 = pygame.font.SysFont('biome', 25)
FONTE3 = pygame.font.SysFont('impact', 90)
FONTE4 = pygame.font.SysFont('biome', 45)

continuar = FONTE4.render(f"aperte 'r' para reiniciar", 1, branco)
game_over = FONTE3.render(f"GAME OVER", 1, vermelho)
comeco = FONTE2.render(f"Aperte qualquer tecla para iniciar!", 1, branco)
legenda = FONTE2.render(f"Aperte a tecla 'espaço' para pular!", 1, branco)

def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo, fimdejogo
    pontos = 0
    velocidade_jogo = 7
    colidiu = False
    fimdejogo = False
    personagem.rect.y = 370
    personagem.pulo = False
    lixo.rect.x = LARGURA
    cerca.rect.x = LARGURA
    banco.rect.x = LARGURA
    escolha_obstaculo = choice([0,1,2])

class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'pulo1.wav'))
        self.som_pulo.set_volume(0.2)
        self.imagens_personagem = []
        for i in range(4):
            img = spritesheet.subsurface((i*64,0), (64,64))
            img = pygame.transform.scale(img,(64*2, 64*2))
            self.imagens_personagem.append(img)

        self.index_lista = 0
        self.image = self.imagens_personagem[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = 370
        self.rect.center = (490,430)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()
 
    def update(self):
        if start == True:
            if self.pulo == True:
                if self.rect.y <= 190:
                    self.pulo = False
                self.rect.y -= 15
            else:
                if self.rect.y < self.pos_y_inicial:
                    self.rect.y += 15
                else:
                    self.rect.y = self.pos_y_inicial

            if self.index_lista > 2:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_personagem[int(self.index_lista)]

class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_zombie = []
        for i in range(4,8):
            img = spritesheet.subsurface((i*64,0), (64,64))
            img = pygame.transform.scale(img,(64*2.5, 64*2.5))
            self.imagens_zombie.append(img)

        self.index_lista = 0
        self.image = self.imagens_zombie[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.y = 343
        self. rect.x = pos_x * 90
 
    def update(self):
        if start == True:
            if self.index_lista > 2:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_zombie[int(self.index_lista)]

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.subsurface((8*64,0), (64,64))
        self.rect = self.image.get_rect()
        self.rect.y = 460
        self.rect.x = pos_x * 64
    def update(self):
        if start == True:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= 10

class Nuvens(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.subsurface((15*64,0), (64,64))
        self.image = pygame.transform.scale(self.image,(64*3, 64*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(5, 15, 10)
        self.rect.x = pos_x * (128*2)
    def update(self):
        if start == True:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo
        
class Lixo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.subsurface((14*64, 0), (64, 64))
        self.image = pygame.transform.scale(self.image, (64*2.5, 64*2.5))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = ((LARGURA, 460))
        self.rect.x = LARGURA
    def update(self):
        if start == True:
            if self.escolha == 0:
                if self.rect.topright[0] < 0:
                    self.rect.x = LARGURA
                self.rect.x -= velocidade_jogo

class Cerca(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.subsurface((10*64, 0), (64, 64))
        self.image = pygame.transform.scale(self.image, (64*2.5, 64*4))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = ((LARGURA, 465))
        self.rect.x = LARGURA
    def update(self):
        if start == True:
            if self.escolha == 1:
                if self.rect.topright[0] < 0:
                    self.rect.x = LARGURA
                self.rect.x -= velocidade_jogo

class Banco(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.subsurface((13*64, 0), (64, 64))
        self.image = pygame.transform.scale(self.image, (64*2.2, 64*2.5))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = ((LARGURA, 450))
        self.rect.x = LARGURA
    def update(self):
        if start == True:
            if self.escolha == 2:
                if self.rect.topright[0] < 0:
                    self.rect.x = LARGURA
                self.rect.x -= velocidade_jogo

todas_as_sprites = pygame.sprite.Group()
for i in range(5):
    nuvens = Nuvens(i)
    todas_as_sprites.add(nuvens)
for i in range(20):
    chao = Chao(i)
    todas_as_sprites.add(chao)  
lixo = Lixo()
cerca = Cerca()
banco = Banco()
todas_as_sprites.add(lixo, cerca, banco)
for i in range(3):
    zombie = Zombie(i)
    todas_as_sprites.add(zombie)
personagem = Personagem()
todas_as_sprites.add(personagem)

grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(lixo, cerca, banco)

def janela_desenho():
    JANELA.blit(fundo, (0,0))
    grupo_obstaculos.draw(JANELA)
    todas_as_sprites.draw(JANELA)
    
    global pontos
    pontostxt =  FONTE.render("pontos: " + str(pontos), 1, branco)
    JANELA.blit(pontostxt, (15,15))

    if fimdejogo == True:
      JANELA.blit(game_over, ((LARGURA//2+50), 120))
      JANELA.blit(continuar, ((LARGURA//2+60), 220))

    if start == False:
        JANELA.blit(comeco, ((15), (ALTURA-50)))
        JANELA.blit(legenda, (15,(ALTURA - 30)))
    pygame.display.flip()

def main():
    global colidiu
    global start
    relogio = pygame.time.Clock()
    rodando = True
    while rodando:
        relogio.tick(velocidade)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == KEYDOWN:
                start = True
                if event.key == K_SPACE and colidiu == False:
                    if personagem.rect.y != personagem.pos_y_inicial:
                        pass
                    else:
                        personagem.pular()
                if event.key == K_r and colidiu == True:
                    reiniciar_jogo()

        colisoes = pygame.sprite.spritecollide(personagem, grupo_obstaculos, False, pygame.sprite.collide_mask)

        janela_desenho()

        global escolha_obstaculo
        if lixo.rect.topright[0] <= 0 or cerca.rect.topright[0] <= 0 or banco.rect.topright[0] <= 0:
            escolha_obstaculo = choice([0,1,2])
            lixo.rect.x = LARGURA
            cerca.rect.x = LARGURA
            banco.rect.x = LARGURA
            lixo.escolha = escolha_obstaculo
            cerca.escolha = escolha_obstaculo
            banco.escolha = escolha_obstaculo
        
        global pontos
        global velocidade_jogo
        global fimdejogo
        if colisoes and colidiu == False:
            som_colisao.play()
            colidiu = True

        if colidiu == True:
            fimdejogo = True
        elif start == True:
            pontos +=1
            todas_as_sprites.update()   

        if pontos %100 == 0 and colidiu == False and start == True:
            som_pontuacao.play()
            if velocidade_jogo >= 30:
                velocidade_jogo += 0
            else:
                velocidade_jogo += 1

    pygame.quit()

if __name__ == "__main__":
    main()