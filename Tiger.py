import numpy as np
import random
import pygame
import time

class Cage:

  blue = (0, 0, 255)
  red = (255, 0, 0)
  green = (0, 255, 0)
  white = (255, 255, 255)
  black = (0, 0, 0)
  orange = (255, 165, 0)
  pink = (255, 192, 203)

  def __init__(self, dis, dis_width, dis_height, N):
      self.matrix = self.get_matrix(N)
      self.dis = dis
      self.width = dis_width
      self.height = dis_height
      self.N = N
      self.frame = self.height / 10

  def get_matrix(self, N):
      matrix = [['none' for j in range(N)] for i in range(N)]
      for i in range(N):
          for j in range(N):
              matrix[i][j] = np.random.choice(['bullet', 'care', 'hole', 'none'], replace = True, p = [0.2, 0.1, 0.1, 0.6])
      return matrix

  def Draw(self, dis_height):

    dis_height = self.height
    frame = self.frame
    N = self.N

    self.dis.fill(white)
    celllen = (dis_height-2*frame)/N

    for i in range(N+1):
        pygame.draw.line(self.dis, black, [frame, frame + i*celllen], [dis_height-frame, frame + i*celllen], 3)
        pygame.draw.line(self.dis, black, [frame + i*celllen, frame], [frame + i*celllen, dis_height-frame], 3)
        
    for i in range(N):
        for j in range(N):
            if self.matrix[i][j] == 'hole':
                pygame.draw.rect(self.dis, blue, [frame + celllen*i, frame + celllen*j, celllen, celllen])

    for i in range(N):
        for j in range(N):
            if self.matrix[i][j] == 'bullet':
                im = pygame.image.load('bullet.png')
                im = pygame.transform.scale(im, (2*celllen/3, 2*celllen/3))

                x = frame + celllen/6 + celllen*i
                y = frame + celllen/6 + celllen*j

                self.dis.blit(im, (x,y))
                
            if self.matrix[i][j] == 'care':
                im = pygame.image.load('care.png')
                im = pygame.transform.scale(im, (celllen/2, celllen/2))

                x = frame + celllen/4 + celllen*i
                y = frame + celllen/4 + celllen*j

                self.dis.blit(im, (x,y))

  def Message(self, msg):
      mesg = font_style.render(msg, True, red)
      exitmesg = font_style.render('Press Q for exit', True, black)
      restartmesg = font_style.render('Press C for restart', True, black)
      self.dis.blit(mesg, [dis_width / 3, dis_height / 4])
      self.dis.blit(exitmesg, [dis_width / 3, dis_height / 2])
      self.dis.blit(restartmesg, [dis_width / 3, 2*dis_height / 3])

  def GameClose(self, loser, human):
      GameOver = False
      GameClose = True
      self.dis.fill(white)
      if human.nickname == loser.nickname:
        self.Message('You lose!')
        pygame.display.update()
      else:
        self.Message('You win!')
        pygame.display.update()
      for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_q:
                  GameOver = True
                  GameClose = False
              if event.key == pygame.K_c:
                  GameLoop()
      return GameOver, GameClose

class Human:
  def __init__(self, name, age, nickname, attack, bullets, health, position, stop):
    self.name = name
    self.age = age
    self.nickname = nickname
    self.attack = attack
    self.bullets = bullets
    self.health = health 
    self.position = position 
    self.stop = stop 
  
  def CheckPoint(self, cage):
    i = self.position[0]
    j = self.position[1]

    if cage.matrix[i][j] == 'bullet':
        self.bullets += 1
        cage.matrix[i][j] = 'none'

    if cage.matrix[i][j] == 'care':
        self.health += 10
        cage.matrix[i][j] = 'none'

    if cage.matrix[i][j] == 'hole':
        self.stop = True
        self.health -= 2

  def Draw(self, cage):

      frame = cage.frame

      celllen = (cage.height - 2*frame)/cage.N
        
      im = pygame.image.load('human.png')
      im = pygame.transform.scale(im, (2*celllen/3, 2*celllen/3))

      x = frame + celllen/6 + celllen*self.position[0]
      y = frame + celllen/6 + celllen*self.position[1]

      cage.dis.blit(im, (x,y))


  def Your_score(self, cage):
    dis_height = cage.height
    frame = cage.frame

    value = score_font.render(self.nickname + ' health: ' + str(self.health), True, black)
    cage.dis.blit(value, [dis_height, 3/2*frame])
    value = score_font.render(self.nickname + ' bullets: ' + str(self.bullets), True, black)
    cage.dis.blit(value, [dis_height, 2*frame])


  def Go(self, event):

    Go = False
    NeedToCheckHuman = not self.stop
         
    if self.stop == False:
        if event.key == pygame.K_LEFT and self.position[0] > 0:
            Go = True
            self.position[0] -= 1
        if event.key == pygame.K_RIGHT and self.position[0] < N-1:
            Go = True
            self.position[0] += 1
        if event.key == pygame.K_UP and self.position[1] > 0:
            Go = True
            self.position[1] -= 1
        if event.key == pygame.K_DOWN and self.position[1] < N-1:
            Go = True
            self.position[1] += 1

    NeedToCheckHuman = not self.stop
    if NeedToCheckHuman == False:
        Go = True
    self.stop = False

    return Go, NeedToCheckHuman

class Tiger:
  def __init__(self, age, nickname, attack, health, position, stop):
    self.age = age
    self.nickname = nickname
    self.attack = attack
    self.health = health
    self.position = position
    self.stop = stop

  def CheckPoint(self, cage):
    i = self.position[0]
    j = self.position[1]
    if cage.matrix[i][j] == 'care':
        self.health += 7
        cage.matrix[i][j] = 'none'

  def Draw(self, cage):

      frame = cage.frame

      celllen = (cage.height - 2*frame)/cage.N
        
      im = pygame.image.load('tiger.png')
      im = pygame.transform.scale(im, (2*celllen/3, 2*celllen/3))

      x = frame + celllen/6 + celllen*self.position[0]
      y = frame + celllen/6 + celllen*self.position[1]

      cage.dis.blit(im, (x,y))


  def Your_score(self, cage):
      value = score_font.render(self.nickname + ' health: ' + str(self.health), True, black)
      cage.dis.blit(value, [cage.height, cage.frame])


  def Go(self, human, cage):

      frame = cage.frame
      celllen = (cage.height - 2*frame)/cage.N

      tiger_x = frame + celllen/4 + celllen * self.position[0]
      tiger_y = frame + celllen/4 + celllen * self.position[1]

      human_x = frame + celllen/4 + celllen * human.position[0]
      human_y = frame + celllen/4 + celllen * human.position[1] 

      if self.stop == False:
          if abs(tiger_x - human_x) <= abs(tiger_y - human_y):
              if tiger_y - human_y < 0:
                  tiger_y += celllen
                  self.position[1] += 1
              if tiger_y - human_y > 0:
                  tiger_y -= celllen
                  self.position[1] -= 1
          else:
              if tiger_x - human_x < 0:
                  tiger_x += celllen
                  self.position[0] += 1
              if tiger_x - human_x > 0:
                  tiger_x -= celllen
                  self.position[0] -= 1
            
      self.stop = False

def Attack(human, tiger):
  ti = tiger.position[0]
  tj = tiger.position[1]
  hi = human.position[0]
  hj = human.position[1] 

  if human.bullets > 0:
    if abs(ti - hi) == 1 and tj == hj or abs(tj - hj) == 1 and ti == hi or abs(ti - hi) == 1 and abs(tj - hj) == 1 or ti == hi and tj == hj:
      if tiger.health >= human.attack:
        tiger.health -= human.attack
      else:
        tiger.health = 0
      human.bullets -= 1
      tiger.stop = True

  if ti == hi and tj == hj:
    if human.health >= tiger.attack:
      human.health -= tiger.attack
    else:
      human.health = 0

def CheckGameOver(tiger, human):
  if tiger.health <= 0:
    return tiger, True
  if human.health <= 0:
    return human, True
  else:
    return human, False

def Rand(N):
  return random.randint(0, N-1)

pygame.init()
dis_width = 900
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
 
pygame.display.set_caption('Tiger vs Human')
 
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
orange = (255, 165, 0)
pink = (255, 192, 203)

N = 7

score_font = pygame.font.SysFont("comicsansms", 20)
font_style = pygame.font.SysFont("bahnschrift", 35)


def GameLoop():

  tigerpostion = [Rand(N), Rand(N)]
  humanposition = [Rand(N), Rand(N)]
  while humanposition == tigerpostion:
    humanposition = [Rand(N), Rand(N)]

  cage = Cage(dis, dis_width, dis_height, N)
  tiger = Tiger(4, 'Pampushka', 5, 40, tigerpostion, False)
  human = Human('Gleb', 42, 'Slider', 3, 6, 10, humanposition, False)

  GameOver = False
  GameClose = False

  cage.Draw(dis_height)
  tiger.Draw(cage)
  human.Draw(cage)
  tiger.CheckPoint(cage)
  human.CheckPoint(cage)
  human.Your_score(cage)
  tiger.Your_score(cage)
  pygame.display.update()

  while not GameOver:

    while GameClose == True:
      GameOver, GameClose = cage.GameClose(loser, human)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
            GameOver = True

      if event.type == pygame.KEYDOWN:
        Go, NeedToCheckHuman = human.Go(event)
        if NeedToCheckHuman:
          human.CheckPoint(cage)

        if Go == True:
          tiger.Go(human, cage)
        tiger.CheckPoint(cage)

        if Go == True:
          Attack(human, tiger)

        cage.Draw(dis_height)
        tiger.Draw(cage)
        human.Draw(cage)

        human.Your_score(cage)
        tiger.Your_score(cage)

        pygame.display.update()

        loser, GameClose = CheckGameOver(tiger, human)
        if GameClose == True:
          time.sleep(2)

  pygame.quit()
  quit()

GameLoop()
