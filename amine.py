#!/usr/bin/python
__doc__ = '''
  A minesweeper game
'''
__license__ = 'http://www.gnu.org/licenses/gpl-2.0.html'
__author__ = 'Lajos Koszti <ajnasz@ajnasz.hu>'
__copyright__ = 'Copyright 2009, Lajos Koszti'

import sys, measuretime, os
from random import randint 


class Amine:


  def __init__(self, x = 8, y = 8, mines = 10):
    self.max_x = x
    self.max_y = y
    self.max_mines = mines

    self.mines = []
    self.genFields()
    self.showInitData()
    # print self.mines

  
  mines = []
  clicked = []
  fields = []
  message = ''

  def start(self):
    self.measureTime = measuretime.MeasureTime()
    self.measureTime.start()
    self.readCoords(1)


  def showInitData(self):
    print 'x: %d, y: %d, mines: %d' % (self.max_x, self.max_y, self.max_mines)
    pass

  
  def genFields(self):
    self.fields = []
    x = 0

    while x < self.max_x:
      self.fields.append([])
      y = 0

      while y < self.max_y:
        self.fields[x].append({'ismine': 0, 'clicked': 0, 'neighbours': -1})
        y = y+1
        
      x = x+1

    
  def genMines(self, click):
    # nums = ([1,1], [2,3], [5,5], [0,6], [7,3], [7,7], [0,7], [5,4], [4,5], [3,5])
    # for i in nums:
    #   self.setMine(i)
    i = 0
    while i < self.max_mines:
      random_num = [randint(0,self.max_x-1), randint(0,self.max_y-1)]

      if random_num != click:
        if self.setMine(random_num):
          i = i+1

  
  def setMine(self, mine):

    if len(self.fields[mine[0]][mine[1]]) == 1 and not self.fields[mine[0]][mine[1]].has_key('ismine') or not self.fields[mine[0]][mine[1]]['ismine']:
      self.fields[mine[0]][mine[1]]['ismine'] = 1 # 1 = mine, 2 = marked, 0 = not mine
      return 1

    return 0


  def setGreenField(self, pos):
    self.fields[mine[0]][mine[1]]['ismine'] = 0
        

  def selectField(self, click):
    self.fields[click[0]][click[1]]['clicked'] = 1

    if self.fields[click[0]][click[1]]['ismine']:
      self.message = '\033[1;31mSo LAME, You Died!\033[0m'
      return 1

    if self.getRemaining() == 0:
      self.message = '\033[1;32mCool, You WIN!\033[0m'
      self.message += '\nElapsed time: %d sec' % (int(self.measureTime.finish()))
      return 2

    return 0
  

  def getRemaining(self):
    remaining = 0
    for row in self.fields:

      for col in row:

        if not (col.has_key('clicked') and col['clicked']) and not (col.has_key('ismine') and col['ismine']):
          remaining = remaining + 1

    return remaining


  def readCoords(self, first=0):
    '''
    Reads the coordinates from the terminal
    if the 'first' parameter is true, then the
    mines will be generated in that step, the
    first selected field won't be a mine
    '''

    while(1):

      try:
        x = self.readX()
        y = self.readY()

        if first:
          self.genMines([x,y])
          # TODO should be removed, because it's just a
          #   workaround to show the fully cleaned minefield
          #   after the first selection too
          self.printMiner() 

        isEnd = self.selectField([x, y])
        self.printMiner(isEnd)

        if not isEnd:
          self.readCoords()

        else:
          break

        return

      except (EOFError, KeyboardInterrupt):
        print '\nexit..'
        return
    

  def readX(self):
    '''
    Reads the X coordinate from the terminal
    and checks that the coordinate is valid,
    if not, then asks again for it.
    '''
    try:
      x = input('X? ')
    except SyntaxError:
      self.readX()
      return -1

    while x < 0 or x >= self.max_x:
      print 'Wrong X coordinate, it should be between 0 and %d' % (self.max_x-1)
      x = self.readX()
      
    return x
    

  def readY(self):
    '''
    Reads the Y coordinate from the terminal
    and checks that the coordinate is valid,
    if not, then asks again for it
    '''
    try:
      y = input('Y? ')
    except SyntaxError:
      self.readY()
      return -1

    while y < 0 or y >= self.max_y:
      print 'Wrong Y coordinate, it should be between 0 and %d' % (self.max_y-1)
      y = self.readY()

    return y

  
  def printField(self, x, y, field, force=0):
    '''
    Prints a field, depending on it's current state
    '''

    output = ''
    if force or (field.has_key('clicked') and field['clicked']):

      if field['ismine']:
        if force and force == 2:
          output = '\033[0;35m[xxx]\033[00m'
        else:
          output = '\033[0;31m[xxx]\033[00m'


      elif field['neighbours'] > 0:
        output = '\033[0;32m[%s]\033[00m' % (str(field['neighbours']).center(3))

      else:
        output = '[---]'
    else:
      output = '\033[0;34m[%s,%s]\033[0m' % (x,y)

    return output


  def printMiner(self, isEnd=0):
      
    os.system(['clear','cls'][os.name == 'nt'])
    if self.message:
      print self.message
      self.message = ''

    for i, line in enumerate(self.fields):

      for j, row in enumerate(line):

        if row['neighbours'] == -1 and (not row['clicked'] or not row['ismine']):
          neighbours = self.getNeighbours([i,j])
          self.fields[i][j]['neighbours'] = neighbours['sum']

          if neighbours['sum'] == 0:

            for neighbour in neighbours['neighbours']:
              if not self.fields[neighbour[0]][neighbour[1]]['clicked']:
                self.selectField([neighbour[0], neighbour[1]])

        print self.printField(i, j, self.fields[i][j], isEnd),

      print
    print 'remaining: ', self.getRemaining()


  def getNeighbours(self, field):
    x = field[0]
    y = field[1]
    cases = ((x-1, x, x+1), (y-1, y, y+1))
    out = {
      'neighbours': [],
      'sum': 0
    }
    for xcase in cases[0]:

      for ycase in cases[1]:

        try:
          if not (xcase == x and ycase == y) and xcase >= 0 and ycase >= 0 and self.fields[xcase][ycase]:
            # print 'cases: ', xcase, ycase, self.fields[xcase][ycase]
            out['neighbours'].append((xcase, ycase))
            if self.fields[xcase][ycase].has_key('ismine') and self.fields[xcase][ycase]['ismine']:
              out['sum'] = out['sum'] + 1
        except (IndexError):
          pass
    #print out
    return out



try:
  x = int(sys.argv[1])
except:
  x = 8

try:
  y = int(sys.argv[2])
except:
  y = 8

try:
  mines = int(sys.argv[3])
except:
  mines = 10

miner = Amine(x, y, mines)
miner.start()
