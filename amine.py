import random
import sys


class Amine:
  '''A minesweeper game'''
  
  mines = []
  clicked = []
  fields = []
  max_x = 8
  max_y = 8


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
    i = 0
    nums = ([1,1], [2,3], [5,5], [0,6], [7,3], [7,7], [0,7], [5,4], [4,5], [3,5])
    for i in nums:
      self.setMine(i)
    #while i < 10:
    #  random_num = [random.randint(0,self.max_x-1), random.randint(0,self.max_y-1)]

    #  if self.setMine(random_num):
    #    i = i+1

  
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
              sections = ('tl', 't', 'tr', 'l', 'r', 'bl', 'b', 'br')

              for section in sections:

                if neighbours[section]['mine'] == -1:
                  self.clickOnField([neighbours[section]['x'], neighbours[section]['y']])

            print self.printMine(i, j, 2, neighbours['sum']),

        else:
          print self.printMine(i, j, -1),

      print
      print self.max_x*6*'-'


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

    if x > 0: # az aktualis elem nem az elso sorban van
      prev_row = self.fields[x-1]

      if prev_row[y].has_key('ismine') and prev_row[y]['ismine']: # t
        neighbours['t']['mine'] = 1
        neighbours['sum'] = neighbours['sum'] + 1

      if y > 0: #nem elso sor nem elso oszlopa
        if prev_row[y-1].has_key('ismine' and prev_row[y-1]['ismine']): # tr
          neighbours['tl']['mine'] = 1
          neighbours['sum'] = neighbours['sum'] + 1
      else:
        neighbours['tl']['y'] = y

      if y < self.max_y - 1: #nem elso sor nem utolso oszlopa
        
        if prev_row[y+1].has_key('ismine') and prev_row[y+1]['ismine']: # tl
          neighbours['tr']['mine'] = 1
          neighbours['sum'] = neighbours['sum'] + 1
      else:
        neighbours['tr']['y'] = y

    else:
      neighbours['t']['x'] = neighbours['tl']['x'] = neighbours['tr']['x'] = x

      
    if x < self.max_x - 1: # nem utolso sor
      next_row = self.fields[x+1]

      if next_row[y].has_key('ismine') and next_row[y]['ismine']: # b
        neighbours['b']['mine'] = 1
        neighbours['sum'] = neighbours['sum'] + 1


      if y > 0: # nem utolso sor nem elso oszlopa
        
        if next_row[y-1].has_key('ismine') and next_row[y-1]['ismine']: # br
          neighbours['bl']['mine'] = 1
          neighbours['sum'] = neighbours['sum'] + 1

      else:
        neighbours['bl']['y'] = y


      if y < self.max_y - 1: #nem elso sor nem utolso oszlopa
        
        if next_row[y+1].has_key('ismine') and next_row[y+1]['ismine']: # bl
          neighbours['br']['mine'] = 1
          neighbours['sum'] = neighbours['sum'] + 1


      else:
        neighbours['br']['y'] = self.max_y - 1


    else:
      neighbours['b']['x'] = neighbours['bl']['x'] = neighbours['br']['x'] = self.max_x - 1


    if y > 0: #nem elso oszolop
      prev_col = self.fields[x][y-1]

      if prev_col.has_key('ismine') and prev_col['ismine']: # l
        self.fields[x][y-1]['mine'] = 1
        neighbours['l']['mine'] = 1
        neighbours['sum'] = neighbours['sum'] + 1

    else:
      neighbours['l']['y'] = 0

    if y < self.max_y - 1: #nem utolso oszlop
      next_col = self.fields[x][y+1]
      
      if next_col.has_key('ismine') and next_col['ismine']:
        neighbours['r']['mine'] = 1
        neighbours['sum'] = neighbours['sum'] + 1

    else:
      neighbours['r']['y'] = self.max_y - 1

    self.fields[x][y]['neighbours'] = neighbours['sum']
    return neighbours


miner = Amine()
miner.printMiner()
miner.start()
