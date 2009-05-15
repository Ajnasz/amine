#!/usr/bin/python
import random
import sys


class Amine:
  '''A minesweeper game'''
  
  mines = []
  clicked = []
  fields = []
  max_x = 8
  max_y = 8
  max_mines = 10
  coveredField = []


  def __init__(self):
    self.mines = []
    self.genFields()
    self.genMines([1,1])
    # print self.mines


  def start(self):
    self.readClicks()

  
  def genFields(self):
    self.fields = []
    x = 0

    while x < self.max_x:
      self.fields.append([])
      y = 0

      while y < self.max_y:
        self.fields[x].append({'ismine': 0})
        y = y+1
        
      x = x+1
    
    
  def genMines(self, clicked):
    # nums = ([1,1], [2,3], [5,5], [0,6], [7,3], [7,7], [0,7], [5,4], [4,5], [3,5])
    # for i in nums:
    #   self.setMine(i)
    i = 0
    while i < self.max_mines:
      random_num = [random.randint(0,self.max_x-1), random.randint(0,self.max_y-1)]

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
      print '\033[1;31mSo LAME, You Died!\033[0m'
      return 0

    if self.getRemianing() == 0:
      print '\033[1;34mCool, You WIN!!!\033[0m'
      return 0

    return 1
  

  def getRemianing(self):
    remaining = 0
    for row in self.fields:

      for col in row:
        if not (col.has_key('clicked') and col['clicked']) and not (col.has_key('ismine') and col['ismine']):
          remaining = remaining + 1

    return remaining


  def readClicks(self):

    while(1):

      try:
        x = self.readX()
        y = self.readY()
        result = self.selectField([x, y])
        self.printMiner()

        if result == 1:
          self.readClicks()

        else:
          break

        return

      except (EOFError, KeyboardInterrupt):
        print '\nexit..'
        return
    

  def readX(self):
    try:
      x = input('X? ')
    except SyntaxError:
      self.readX()
      return -1

    while x < 0 or x > self.max_x:
      x = self.readX()
      
    return x
    

  def readY(self):
    try:
      y = input('Y? ')
    except SyntaxError:
      self.readY()
      return -1

    while y < 0 or y > self.max_y:
      y = self.readY()

    return y

  
  def printMine(self, x, y, field):
    output = ''
    if field.has_key('clicked') and field['clicked']:

      if field['ismine']:
        output = '\033[0;31m[xxx]\033[00m'

      elif field['neighbours'] > 0:
        output = '\033[0;32m[%s]\033[00m' % (str(field['neighbours']).center(3))

      else:
        output = '[---]'
    else:
      output = '\033[0;34m[%s,%s]\033[0m' % (x,y)

    return output


  def printMiner(self):

    for i, line in enumerate(self.fields):

      for j, row in enumerate(line):

        if not row.has_key('clicked') or not row['clicked'] == 1 or not row.has_key('ismine') or not row['ismine'] == 1:
          neighbours = self.getNeighbours([i,j])
          self.fields[i][j]['neighbours'] = neighbours['sum']
          if neighbours['sum'] == 0:
            # print 'neighbours: ', neighbours

            for neighbour in neighbours['neighbours']:
              if not self.fields[neighbour[0]][neighbour[1]].has_key('clicked') or not self.fields[neighbour[0]][neighbour[1]]['clicked']:
                self.selectField([neighbour[0], neighbour[1]])

        print self.printMine(i, j, self.fields[i][j]),

      print
      #print 'coveredFieldNum: ', self.coveredField
    print 'remaining: ', self.getRemianing()


  def getNeighbours(self, field):
    x = field[0]
    y = field[1]
    xcases = (x-1, x, x+1)
    ycases = (y-1, y, y+1)
    out = {
      'neighbours': [],
      'sum': 0
    }
    for xcase in xcases:

      for ycase in ycases:

        try:
          if not (xcase == x and ycase == y) and xcase >= 0 and ycase >= 0 and self.fields[xcase][ycase] :
            # print 'cases: ', xcase, ycase, self.fields[xcase][ycase]
            out['neighbours'].append((xcase, ycase))
            if self.fields[xcase][ycase].has_key('ismine') and self.fields[xcase][ycase]['ismine']:
              out['sum'] = out['sum'] + 1
        except (IndexError):
          pass
    #print out
    return out



miner = Amine()
miner.printMiner()
miner.start()
