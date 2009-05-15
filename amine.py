import random
import sys


class Amine:
  '''A minesweeper game'''
  
  mines = []
  clicked = []
  fields = []
  maxX = 8
  maxY = 8


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

    while x < self.maxX:
      self.fields.append([])
      y = 0

      while y < self.maxY:
        self.fields[x].append({'ismine': 0})
        y = y+1
        
      x = x+1
    
    
  def genMines(self, clicked):
    i = 0

    while i < 10:
      random_num = [random.randint(0,self.maxX-1), random.randint(0,self.maxY-1)]

      if self.setMine(random_num):
        i = i+1

  
  def setMine(self, mine):

    if len(self.fields[mine[0]][mine[1]]) == 1:
      self.fields[mine[0]][mine[1]]['ismine'] = 1 # 1 = mine, 2 = marked, 0 = not mine
      return 1

    return 0


  def setGreenField(self, pos):
    self.fields[mine[0]][mine[1]]['ismine'] = 0
        

  def clickOnField(self, click):
      self.fields[click[0]][click[1]]['clicked'] = 1

      if self.fields[click[0]][click[1]]['ismine']:
        print 'YU BiCCS DIED'
        return 0

      return 1
  

  def readClicks(self):

    while(1):

      try:
        x = self.readX()
        y = self.readY()
        result = self.clickOnField([x, y])
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
    x = input('X? ')

    while x < 0 or x > 8:
      self.readX()
      
    return x
    

  def readY(self):
    y = input('Y? ')

    while y < 0 or y > 8:
      self.readY()

    return y

  
  def printMine(self, x, y, type, neighbours=0):
    output = ''

    if type == 1: # type == 1, its a mine
      output = '[xxx]'

    elif type == 2:
      output = '[%s]' % (str(neighbours).center(3))

    elif type == 0:
      output = '[---]'

    else:
      output = '[%s,%s]' % (x,y)

    return output


  def printMiner(self):

    for i, line in enumerate(self.fields):

      for j, row in enumerate(line):


        if row.has_key('clicked') and row['clicked'] == 1:
          if row.has_key('ismine') and row['ismine'] == 1:
            print self.printMine(i, j, 1),

          else:
            neighbours = self.getNeighbours([i,j])
            if neighbours['sum'] == 0:
              if neighbours['tl']['mine'] != -1:
                self.clickOnField([neighbours['tl']['x'], neighbours['tl']['y']])

              if neighbours['t']['mine'] != -1:
                self.clickOnField([neighbours['t']['x'], neighbours['t']['y']])

              if neighbours['tr']['mine'] != -11:
                self.clickOnField([neighbours['tr']['x'], neighbours['tr']['y']])

              if neighbours['l']['mine'] != -1:
                self.clickOnField([neighbours['l']['x'], neighbours['l']['y']])

              if neighbours['r']['mine'] != -1:
                self.clickOnField([neighbours['r']['x'], neighbours['r']['y']])

              if neighbours['bl']['mine'] != -1:
                try:
                  self.clickOnField([neighbours['bl']['x'], neighbours['bl']['y']])
                except:
                  print neighbours['bl']['mine']
                  exit

              if neighbours['b']['mine'] != -1:
                self.clickOnField([neighbours['b']['x'], neighbours['b']['y']])

              if neighbours['br']['mine'] != -1:
                self.clickOnField([neighbours['br']['x'], neighbours['br']['y']])

            print self.printMine(i, j, 2, neighbours['sum']),

        else:
          print self.printMine(i, j, -1),

      print


  def getNeighbours(self, field):
    x = field[0]
    y = field[1]
    neighbours = {
      'tl': {
        'x': x-1,
        'y': y-1,
        'mine': -1
      },
      't': {
        'x': x-1,
        'y': y-1,
        'mine': -1
      },
      'tr': {
        'x': x-1,
        'y': y-1,
        'mine': -1
      },
      'l': {
        'x': x,
        'y': y-1,
        'mine': -1
      },
      'r': {
        'x': x,
        'y': y+1,
        'mine': -1
      },
      'bl': {
        'x': x-1,
        'y': y+1,
        'mine': -1
      },
      'b': {
        'x': x,
        'y': y+1,
        'mine': -1
      },
      'br': {
        'x': x+1,
        'y': y+1,
        'mine': -1
      },
      'sum': 0
    }

    if x > 0:
      if self.fields[x-1][y].has_key('ismine') and self.fields[x-1][y]['ismine'] == 1:
        neighbours['sum'] = neighbours['sum']+1
        neighbours['l']['mine'] = 1
      else:
        neighbours['l']['mine'] = 0

      if y > 0:
        if self.fields[x-1][y-1].has_key('ismine') and self.fields[x-1][y-1]['ismine'] == 1:
          neighbours['sum'] = neighbours['sum']+1
          neighbours['tl']['mine'] = 1
        else:
          neighbours['tl']['mine'] = 0

      if y < self.maxY-2:
        if self.fields[x-1][y+1].has_key('ismine') and self.fields[x-1][y+1]['ismine'] == 1:
          neighbours['sum'] = neighbours['sum']+1
          neighbours['tr']['mine'] = 1
        else:
          neighbours['tr']['mine'] = 0

    if x < self.maxX-2:

      if self.fields[x+1][y].has_key('ismine') and self.fields[x+1][y]['ismine'] == 1:
        neighbours['sum'] = neighbours['sum']+1
        neighbours['b']['mine'] = 1
      else:
        neighbours['b']['mine'] = 0

      if y > 0:
        if self.fields[x+1][y-1].has_key('ismine') and self.fields[x+1][y-1]['ismine'] == 1:
          neighbours['sum'] = neighbours['sum']+1
          neighbours['bl']['mine'] = 1
        else:
          neighbours['bl']['mine'] = 0

      if y < self.maxY-2:
        if self.fields[x+1][y+1].has_key('ismine') and self.fields[x+1][y+1]['ismine'] == 1:
          neighbours['sum'] = neighbours['sum']+1
          neighbours['br']['mine'] = 1
        else:
          neighbours['br']['mine'] = 0
      
    if y > 0:
      if self.fields[x][y-1].has_key('ismine') and self.fields[x][y-1]['ismine'] == 1:
        neighbours['sum'] = neighbours['sum']+1
        neighbours['t']['mine'] = 1
      else:
        neighbours['t']['mine'] = 0

    if y < self.maxY-2:
      if self.fields[x][y+1].has_key('ismine') and self.fields[x][y+1]['ismine'] == 1:
        neighbours['sum'] = neighbours['sum']+1
        neighbours['b']['mine'] = 1
      else:
        neighbours['b']['mine'] = 0

    self.fields[x][y]['neighbours'] = neighbours['sum']
    return neighbours


miner = Amine()
miner.printMiner()
miner.start()
