#code by Iraikare
#graphics by João Ricardo
#modified by Pedro Vitor (Roger)

import pygame
from pygame.locals import *
import os
from random import randrange, choice, randint
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
velocidade_jogo = 8

fundo = pygame.transform.scale(pygame.image.load(os.path.join(diretorio_imagens,'cenario1f.png')), (LARGURA, ALTURA))
spritesheet = pygame.image.load(os.path.join(diretorio_imagens,'tudinho.png')).convert_alpha()
spritepredios = pygame.transform.scale(pygame.image.load(os.path.join(diretorio_imagens,'predios.png')), (LARGURA, ALTURA))

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons,'gameover1.wav'))
som_colisao.set_volume(0.2)
som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons,'score.wav'))
som_pontuacao.set_volume(0.2)

#music = pygame.mixer.music.load('sons/musca.wav')
#pygame.mixer.music.set_volume(0.13)
#pygame.mixer.music.play(-1)

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
    velocidade_jogo = 8
    personagem.velocidade_pulo = 15
    personagem.altura_pulo = 180
    personagem.rect.center = (490,430)
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

        self.altura_pulo = 180
        self.velocidade_pulo = 15

        self.index_lista = 0
        self.image = self.imagens_personagem[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = 370
        self.rect.center = (490,430)
        self.pulo = False
        self.framespeed = 0.2

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def movemento(self, vel):
        self.framespeed = 0.2
        if self.rect.topright[0] <= LARGURA:
            if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                if self.pulo:
                    self.rect.x += 4
                else:
                    self.rect.x += 8
        if self.rect.x >= -10:
            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
                if self.pulo:
                    self.rect.x -= 4
                else:
                    self.rect.x -= vel
                    self.framespeed = 0
                    self.index_lista = 0
        if self.pulo:
            self.framespeed = 0
            self.index_lista = 3
 
    def update(self, vel):
        self.movemento(vel)
        if start == True:
            
            if self.pulo == True:
                if self.rect.y <= self.altura_pulo:
                    self.pulo = False
                self.rect.y -= self.velocidade_pulo
            else:
                if self.rect.y < self.pos_y_inicial:
                    self.rect.y += self.velocidade_pulo
                else:
                    self.rect.y = self.pos_y_inicial

            self.index_lista += self.framespeed
            if self.index_lista > 4:
                self.index_lista = 0
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
            self.index_lista += 0.2
            if self.index_lista > 4:
                self.index_lista = 0
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
            self.rect.x -= velocidade_jogo

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
            self.rect.x -= velocidade_jogo // 8

class Predios(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritepredios
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = 0
    def update(self):
        if start == True:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo // 4
        
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
for i in range(2):
    predios = Predios((i-1)*LARGURA)
    todas_as_sprites.add(predios)
lixo = Lixo()
cerca = Cerca()
banco = Banco()
todas_as_sprites.add(lixo, cerca, banco, predios)
for i in range(3):
    zombie = Zombie(i)
    todas_as_sprites.add(zombie)
personagem = Personagem()
personagem_s = pygame.sprite.Group()
personagem_s.add(personagem)

grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(lixo, cerca, banco, zombie)

def janela_desenho():
    JANELA.blit(fundo, (0,0))
    grupo_obstaculos.draw(JANELA)
    todas_as_sprites.draw(JANELA)
    personagem_s.draw(JANELA)
    
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
    pause = False
    while rodando:
        relogio.tick(velocidade)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == KEYDOWN:
                start = True
                if event.key == K_SPACE or event.key == K_UP or event.key == K_w:
                    if colidiu == False and pause == False:
                        if personagem.rect.y != personagem.pos_y_inicial:
                            pass
                        else:
                            personagem.pular()
                if event.key == K_r and colidiu == True:
                    reiniciar_jogo()
                if event.key == K_p and colidiu == False:
                    if pause:
                        pause = False
                    else:
                        pause = True

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

        if colidiu:
            fimdejogo = True
        elif start and pause == False:
            pontos +=1
            todas_as_sprites.update()
            personagem_s.update(velocidade_jogo)

            if pontos %100 == 0:
                som_pontuacao.play()
                if velocidade_jogo >= 40:
                    velocidade_jogo += 0
                else:
                    velocidade_jogo += 1
                    personagem.altura_pulo += 2

    pygame.quit()

if __name__ == "__main__":
    main()
