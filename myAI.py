import random
import colorfight
import functools

class myGame:
    def __init__(self):
        self.g = colorfight.Game()
        self.g.JoinGame('aaaaAI')

    def getCell(self, p):
        return self.g.GetCell(p[0], p[1])

    def getP(self, cell):
        return (cell.x, cell.y)

    def getMyCell(self):
        mycell = set()
        for x in range(self.g.width):
            for y in range(self.g.height):
                c = self.g.GetCell(x,y)
                if c.owner == self.g.uid:
                    #loc = (str(x),str(y))
                    mycell.add(self.getP(c))
        return mycell

    def getBaseCell(self):
        baseCell = set()
        for x in range(self.g.width):
            for y in range(self.g.height):
                c = self.g.GetCell(x,y)
                if c.buildType == 'base':
                    #loc = (str(x),str(y))
                    baseCell.add(self.getP(c))
        return baseCell

    def getMyBaseCell(self):
        myBaseCell = set()
        baseCell = self.getBaseCell()
        for bc in baseCell:
            if self.getCell(bc).owner == self.g.uid:
                myBaseCell.add(bc)
        return myBaseCell

    def getEnemyCell(self):
        enemycell = set()
        for x in range(self.g.width):
            for y in range(self.g.height):
                c = self.g.GetCell(x, y)
                if c.owner != self.g.uid and c.owner != 0:
                    #loc = (str(x), str(y))
                    enemycell.add(self.getP(c))
        return enemycell

    def getEmptyCell(self):
        emptyCell = set()
        for x in range(self.g.width):
            for y in range(self.g.height):
                c = self.g.GetCell(x, y)
                if c.owner != 0:
                    #loc = (str(x), str(y))
                    emptyCell.add(self.getP(c))
        return emptyCell

    def getGoldCell(self):
        goldCell = set()
        for x in range(self.g.width):
            for y in range(self.g.height):
                c = self.g.GetCell(x,y)
                if c.cellType == 'gold':
                    goldCell.add(self.getP(c))
        return goldCell

    def getEnergyCell(self):
        energyCell = set()
        for x in range(self.g.width):
            for y in range(self.g.height):
                c = self.g.GetCell(x,y)
                if c.cellType == 'energy':
                    energyCell.add(self.getP(c))
        return energyCell

    def getAdjCell(self, cc):
        a = (cc[0] + 1, cc[1])
        b = (cc[0] - 1, cc[1])
        c = (cc[0], cc[1] + 1)
        d = (cc[0], cc[1] - 1)
        '''
        a = self.g.GetCell(c.x + 1, c.y)
        b = self.g.GetCell(c.x - 1, c.y)
        c = self.g.GetCell(c.x, c.y + 1)
        d = self.g.GetCell(c.x, c.y - 1)
        '''
        adjCell = {a, b, c, d}
        #if None in {self.getCell(aa) for aa in adjCell}:
        #    adjCell.remove(None)
        return {x for x in adjCell if self.getCell(x) is not None}

    def getBorderCell(self):
        borderCell = set()
        myCell = self.getMyCell()
        for c in myCell:
            adjCell = self.getAdjCell(c)
            for d in adjCell:
                if d not in myCell:
                    borderCell.add(c)
                    break
        return borderCell

    '''
    def removeDuplicates(self, cellSet):
        for c in cellSet():
            if c.x == c.y
        list2 = []
        for i in range(cellList.size):
            if [cellList[i].x, cellList[i].y] in list2:
                cellList.remove()
        if ()
    '''

    def getAttackableCell(self):
        attackableCell = set()
        myCell = self.getMyCell()
        borderCell = self.getBorderCell()
        #print(borderCell)
        #print("border Cell: ")
        #print(borderCell)
        for c in borderCell:
            adjCell = self.getAdjCell(c)
            for d in adjCell:
                if d not in myCell and not self.getCell(d).isTaking:
                    attackableCell.add(d)
        #print((set(attackableCell + myCell)))
        #print("attackable Cell: ")
        #print(attackableCell | myCell)
        return attackableCell | myCell

    def buildGrid(self, initVal):
        grid = []
        for x in range(self.g.width):
            grid.append([])
            for y in range(self.g.height):
                grid[x].append(initVal)
        return grid

    def getBaseRank(self):
        baseRank = self.buildGrid(0)
        for x in range(self.g.width):
            for y in range(self.g.height):
                tmp = self.g.GetCell(x, y)
                if tmp.cellType == 'gold':
                    baseRank[x][y] += 10
                elif tmp.cellType == 'energy':
                    baseRank[x][y] += 10
                if tmp.owner == 0: #empty
                    baseRank[x][y] += 10
                if tmp.owner == self.g.uid and tmp.buildType == 'base':
                    # part 1: safe
                    flag = True
                    adjCells = self.getAdjCell((x, y))
                    for aa in adjCells:
                        if self.getCell(aa).owner != self.g.uid:
                            flag = False
                            break
                    if flag:
                        baseRank[x][y] -= 10
                    # part 2: very safe
                    flag = True
                    adjCells = functools.reduce(lambda a, b : a | b, [self.getAdjCell(xx) for xx in adjCells])
                    for aa in adjCells:
                        if self.getCell(aa).owner != self.g.uid:
                            flag = False
                            break
                    if flag:
                        baseRank[x][y] -= 20
        return baseRank

    def getCombatRank(self):
        combatRank = self.buildGrid(0)
        for x in range(self.g.width):
            for y in range(self.g.height):
                tmp = self.g.GetCell(x, y)
                if not tmp.isTaking:
                    combatRank[x][y] = (34 - tmp.takeTime) * 1.5
                if tmp.owner != self.g.uid:
                    for xx in self.getAdjCell((x, y)):
                        if self.getCell(xx).owner == self.g.uid:
                            combatRank[x][y] += (34 - tmp.takeTime) * 0.1
                #if tmp.owner == 0:
                    #print("Cell (" + str(tmp.x) + ", " + str(tmp.y) + ") cell is empty")

        return combatRank

    def mDist(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def getRangeRank(self):
        rangeRank = self.buildGrid(0)
        goldCells = self.getGoldCell()
        energyCells = self.getEnergyCell()
        myBaseCells = self.getMyBaseCell()
        baseCells = self.getBaseCell()
        for x in range(self.g.width):
            for y in range(self.g.height):
                for c in goldCells:
                    rangeRank[x][y] += (60 / (self.mDist((x, y), c) + 1)) ** 2 / 6
                for c in energyCells:
                    rangeRank[x][y] += (60 / (self.mDist((x, y), c) + 1)) ** 2 / 12
                for c in myBaseCells:
                    rangeRank[x][y] += (60 / (self.mDist((x, y), c) + 1)) ** 2 / 6
                for c in baseCells:
                    rangeRank[x][y] += (60 / (self.mDist((x, y), c) + 1)) ** 2 / 100
                rangeRank[x][y] = rangeRank[x][y] ** (1/2)
        return rangeRank

    def getTotalRank(self, ranks):
        totalRank = self.buildGrid(0)
        for i in range(self.g.width):
            for j in range(self.g.height):
                totalRank[i][j] = sum([x[i][j] for x in ranks])
                #print("%3lf" % totalRank[i][j] + " ", end ="")
                #print("ranks at (" + str(i) + ", " + str(j) + "): " + str(totalRank[i][j]))
            #print()
        return totalRank

    def rankAttackableCell(self, rank):
        cellSet = self.getAttackableCell()
        #print(cellSet)
        maxRank = random.sample(cellSet, 1)[0]
        #print("Attackable Cells 2: ")
        for c in cellSet:
            #print("(" + str(c[0]) + ", " + str(c[1]) + ") rank: " + str(rank[c[0]][c[1]]))
            if rank[c[0]][c[1]] > rank[maxRank[0]][maxRank[1]]:
                maxRank = c
        #print("the cell with maximum rank is at (" + str(maxRank[0]) + ", " + str(maxRank[1]) +
        #        "), rank: " + str(rank[maxRank[0]][maxRank[1]]))
        return maxRank

    def buildBase(self):
        if self.g.gold < 60 or len(self.getMyBaseCell()) >= 3:
            return None
        priorityCells = (self.getGoldCell() | self.getEnergyCell() & self.getMyCell()) - self.getMyBaseCell()
        secondaryCells = (self.getMyCell() - self.getMyBaseCell())
        #print(self.getBaseCell())
        #print(self.getMyBaseCell())
        #print(energyCells)
        build = True
        for e in priorityCells:
            adjCells = self.getAdjCell(e)
            adjCells = functools.reduce(lambda a, b : a | b, [self.getAdjCell(x) for x in adjCells])
            for adj in adjCells:
                if self.getCell(adj).owner != self.g.uid:
                    build = False
                    break
            if build:
                return e

        build = True
        for e in secondaryCells:
            adjCells = self.getAdjCell(e)
            #adjCells = functools.reduce(lambda a, b : a | b, [self.getAdjCell(x) for x in adjCells])
            #adjCells = functools.reduce(lambda a, b : a | b, [self.getAdjCell(x) for x in adjCells])
            #adjCells = functools.reduce(lambda a, b : a | b, [self.getAdjCell(x) for x in adjCells])
            for adj in adjCells:
                if self.getCell(adj).owner != self.g.uid:
                    build = False
                    break
            if build:
                return e
        return None

    def squareBlast(self):
        if self.g.energy > 70:
            for bc in self.getMyBaseCell():
                tmp = self.getAdjCell(bc)
                counter = 0
                for t in tmp:
                    if self.getCell(t).owner > 0 and self.getCell(t).owner != self.g.uid: #enemy
                        return bc

            for mc in self.getMyCell():
                tmp = self.getAdjCell(mc)
                counter = 0
                for t in tmp:
                    if self.getCell(t).owner > 0 and self.getCell(t).owner != self.g.uid: #enemy
                        return mc

            return None

    def main(self):
        test = 3
        while test:
            # Attack
            rank = self.getTotalRank([self.getBaseRank(), self.getCombatRank(), self.getRangeRank()])
            atk = self.rankAttackableCell(rank)
            print(self.g.AttackCell(atk[0], atk[1]))

            # Build Base
            base = self.buildBase()
            if base != None:
                print(self.g.BuildBase(*base))

            # square blast
            bl = self.squareBlast()
            if bl != None:
                print(self.g.Blast(*bl, "square"))

            self.g.Refresh()
            #test -= 1

a = myGame()
a.main()
