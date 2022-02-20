import sys
import random
from collections import deque as queue


lyingDaggerTicksLeft = 0
lyingBonusTicksLeft = 0
DaggerTicksLeft = 0
BonusTicksLeft = 0

while True:
    #taking initial parameters w, h, p, t
    line = input()
    parameters = [None] * 4
    for i in range(0, 4):
        parameters[i] = int(line.split()[i])
    w, h, p, t = parameters[0], parameters[1], parameters[2], parameters[3]
    
    #printing w, h, p, t parameters
    # print(w, h, p, t, file=sys.stderr, flush=True)
    
    #taking game map
    Map = []
    for line_idx in range(h):
        line = input()
        map_line = list(line)
        
        if "d" in map_line: 
            if lyingDaggerTicksLeft == 0: 
                lyingDaggerTicksLeft = 14
            else: 
                lyingDaggerTicksLeft -= 1
        
        if "b" in map_line: 
            if lyingBonusTicksLeft == 0: 
                lyingBonusTicksLeft = 14
            else: 
                lyingBonusTicksLeft -= 1
    
        Map.append(map_line)
        
    #printing the map in the console
    # for map_line in Map:
        # print(map_line, file=sys.stderr, flush=True)
       
    #number of entities 
    n = int(input())

    #taking entities values
    Entities = []
    for entitiy_line_idx in range(n):
        line = input()
        entity_line = list(line.split())
        Entities.append(entity_line)
        
    #printing the entities in the console
    for entity_line in Entities:
        print(entity_line, file=sys.stderr, flush=True)

    enemyEntities = []
    enemyCount = 0

    for entity_line in Entities:
        if ((entity_line[0] == 'p') and (entity_line[1] == str(p))):
            PlayerX = int(entity_line[3])
            PlayerY = int(entity_line[2])
            PlayerKnifeStatus = int(entity_line[4])
            PlayerBonusStatus = int(entity_line[5])
            if PlayerKnifeStatus == 1: 
                if DaggerTicksLeft == 0: 
                    DaggerTicksLeft = 14
                else: 
                    DaggerTicksLeft -= 1
            print("DaggerTicksLeft: ", DaggerTicksLeft, file=sys.stderr, flush=True)
            
            if PlayerBonusStatus == 1: 
                if BonusTicksLeft == 0: 
                    BonusTicksLeft = 14
                else: 
                    BonusTicksLeft -= 1
            print("BonusTicksLeft: ", BonusTicksLeft, file=sys.stderr, flush=True)
            
                    
        if ((entity_line[0] == 'm')):
            MonsterX = int(entity_line[3])
            MonsterY = int(entity_line[2])
            enemyEntities.append((MonsterX, MonsterY))
            enemyCount += 1

    #took all of the input info------------------------------
    
    dRow = [-1, 0, 1, 0]
    dCol = [0, 1, 0, -1]

    monsterRange = 2 #This should be constant for the monster's guaranteed kill range

    def isValid(seen, row, col):
        # If cell lies out of bounds
        if (row < 0 or col < 0 or row >= h or col >= w):
            return False
            
        # If cell is already visited
        if ((row, col) in seen):
            return False

        if (Map[row][col] == "!"):
            return False
        if PlayerKnifeStatus == 0 or DaggerTicksLeft < 3: 
            if(min(EnemyBFS((row,col)))<=2):
                return False
            # for enemy in enemyEntities:
            #     MonsterX = enemy[0]
            #     MonsterY = enemy[1]
            #     for x in range(-abs(monsterRange),abs(monsterRange)+1):   #This loop checks for the monster's killzone
            #         for y in range(-abs(monsterRange),abs(monsterRange)+1):
            #             if(abs(x)+abs(y)<=abs(monsterRange)):
            #                 if (row == MonsterX + x and col == MonsterY + y):
    
            #                     # print("VIZHU MONSTRA", file=sys.stderr, flush=True)
            #                     # print("VM row: ", row, "col: ", col, file=sys.stderr, flush=True)
            #                     # print("MonsterX: ", MonsterX, "MonsterY: ", MonsterY, file=sys.stderr, flush=True)
            #                     # print("MonsterX + x: ", MonsterX + x, "MonsterY + y: ", MonsterY + y, file=sys.stderr, flush=True)
            #                     # print("x: ", x, "y: ", y, file=sys.stderr, flush=True)
    
            #                     if(abs(x)+abs(y)==2):
            #                         if((abs(x) > 0 and abs(y) > 0) and (Map[MonsterX+x][MonsterY] == "!" and Map[MonsterX][MonsterY+y] == "!")):
            #                             return True
            #                         if(x==0 and Map[MonsterX][MonsterY+int(y/2)] == "!"):
            #                             return True
            #                         if(y==0 and Map[MonsterX+int(x/2)][MonsterY] == "!"):
            #                             return True
                                
            #                     return False

        return True
    
    # Function to perform the BFS traversal
    def BFS(start):
        print("start: ", start, file=sys.stderr, flush=True)
        q = queue([[start]])
        seen = set([start])
     
        # Iterate while the queue is not empty
        while (len(q) > 0):
            # print("q: ", q, file=sys.stderr, flush=True)
            path = q.popleft()
            x, y = path[-1]
            # print(grid[x][y], end = " ", file=sys.stderr, flush=True)
            # print("x: ", x, "y: ", y, file=sys.stderr, flush=True)
            # print("grid[x][y]: ", grid[x][y], file=sys.stderr, flush=True)
            
            if(Map[x][y] == 'd' and lyingDaggerTicksLeft > 5):
                print("dx: ", x, "dy: ", y, file=sys.stderr, flush=True)
                # print("q: ", q, file=sys.stderr, flush=True)
                print("path: ", path, file=sys.stderr, flush=True)
                return path

            if(Map[x][y] == 'b' and lyingBonusTicksLeft > 5):
                print("dx: ", x, "dy: ", y, file=sys.stderr, flush=True)
                # print("q: ", q, file=sys.stderr, flush=True)
                print("path: ", path, file=sys.stderr, flush=True)
                return path

            #"TypeError: 'NoneType' object is not subscriptable" This exception happens when there are no coins left on the map (I think)
            if(Map[x][y] == '#'):
                if(enemyCount>0):
                    walls = 0
                    for i in range(4):
                        adjx = x + dRow[i]
                        adjy = y + dCol[i]
                        if(not (adjx < 0 or adjy < 0 or adjx >= h-1 or adjy >= w-1)):
                            if(Map[adjx][adjy]=='!'):
                                walls+=1
                    if((walls == 3 and min(EnemyBFS((x, y)))>4) or walls<3):
                        print("#x: ", x, "#y: ", y, file=sys.stderr, flush=True)
                        # print("q: ", q, file=sys.stderr, flush=True)
                        print("path: ", path, file=sys.stderr, flush=True)
                    
                        return path
                else:
                    print("#x: ", x, "#y: ", y, file=sys.stderr, flush=True)
                    # print("q: ", q, file=sys.stderr, flush=True)
                    print("path: ", path, file=sys.stderr, flush=True)

            # Go to the adjacent cells
            for i in range(4):
                adjx = x + dRow[i]
                adjy = y + dCol[i]
                if (isValid(seen, adjx, adjy)):
                    q.append(path + [(adjx, adjy)])
                    seen.add((adjx, adjy))
                    # print("valid squares X: ", adjx, "Y:", adjy, file=sys.stderr, flush=True)

    def panicBFS(start):
        print("PanicBFS start: ", start, file=sys.stderr, flush=True)
        q = queue([[start]])
        seen = set([start])
     
        # Iterate while the queue is not empty
        while (len(q) > 0):
            path = q.popleft()
            x, y = path[-1]

            if(Map[x][y] == '.' and (x, y) != start and not isValid(seen, x, y)): 
                print("panicx: ", x, "panicy: ", y, file=sys.stderr, flush=True)
                print("panicpath: ", path, file=sys.stderr, flush=True)
                return path
        # Go to the adjacent cells
            for i in range(4):
                adjx = x + dRow[i]
                adjy = y + dCol[i]
                if (isValid(seen, adjx, adjy)):
                    q.append(path + [(adjx, adjy)])
                    seen.add((adjx, adjy))
                    # print("valid squares X: ", adjx, "Y:", adjy, file=sys.stderr, flush=True)

    #Valid enemy turns
    def isValidEnemy(seen, row, col):
        if (row < 0 or col < 0 or row >= h or col >= w):
            return False
            
        # If cell is already visited
        if ((row, col) in seen):
            return False

        if (Map[row][col] == "!"):
            return False
        return True

    def EnemyBFS(start):
        print("Enemy BFS started", file = sys.stderr, flush=True)
        distances = []

        # Iterate while the queue is not empty
        
        for index,enemy in enumerate(enemyEntities):
            q = queue([[start]])
            seen = set([start])
            
            print("Enemy:", index, file = sys.stderr, flush=True)

            MonsterX = enemy[0]
            MonsterY = enemy[1]
            while (len(q) > 0):
                path = q.popleft()
                x, y = path[-1]
                if(MonsterX == x and MonsterY == y):
                    distances.append(len(path)-1)
                    print("Distance to enemy: ", distances[index], file=sys.stderr, flush=True)
                    break
                for i in range(4):
                    adjx = x + dRow[i]
                    adjy = y + dCol[i]
                    if (isValidEnemy(seen, adjx, adjy)):
                        # print("valid enemy squares X: ", adjx, "Y:", adjy, file=sys.stderr, flush=True)
                        q.append(path + [(adjx, adjy)])
                        seen.add((adjx, adjy))
        return distances
                    
    path = BFS((PlayerX, PlayerY))
    #BFS-----------------------------------------------------------------
    
    if path is None: 
        print("PATH IS NONE", file=sys.stderr, flush=True)
        PanicPath = panicBFS((PlayerX, PlayerY))
        
        if PanicPath is None:
            print("PANICPATH IS NONE", file=sys.stderr, flush=True)
            closestEnemyDist = 999999
            closestEnemy = (0, 0)
            for enemy in enemyEntities: 
                # print("EENENNENEMY: ", enemy, file=sys.stderr, flush=True)
                # print("(PlayerX, PlayerY): ", (PlayerX, PlayerY), file=sys.stderr, flush=True)
                diff = tuple(map(lambda i, j: i - j, enemy, (PlayerX, PlayerY)))
                # print("diff[0]: ", diff[0], " diff[1]: ", diff[1], file=sys.stderr, flush=True)
                dist = abs(diff[0]) + abs(diff[1])
                closestEnemyDist = min(closestEnemyDist, dist)
                if dist == closestEnemyDist: 
                    closestEnemy = enemy
            print("closestEnemy: ", closestEnemy, file=sys.stderr, flush=True)
            action_idx = 2
            
            distanceFromClosestEnemy = tuple(map(lambda i, j: i - j, closestEnemy, (PlayerX, PlayerY)))
            if (distanceFromClosestEnemy[0] == -1 and
                distanceFromClosestEnemy[1] == -1):
                    action_idx = 0
            elif (distanceFromClosestEnemy[0] == -1 and
                  distanceFromClosestEnemy[1] == 1):
                    action_idx = 1
            elif (distanceFromClosestEnemy[0] == 1 and
                  distanceFromClosestEnemy[1] == -1):
                    action_idx = 0
            elif (distanceFromClosestEnemy[0] == 1 and
                  distanceFromClosestEnemy[1] == 1):
                    action_idx = 3
            print("I JOOK: ", actions[action_idx], file=sys.stderr, flush=True)
            print(actions[action_idx], flush=True)
            
        else: 
            next_move = tuple(map(lambda i, j: i - j, PanicPath[1], (PlayerX, PlayerY)))
            print("Panic x,y - path[1]: ", next_move, file=sys.stderr, flush=True)
            action_idx = 2
            if(next_move[0] != 0): 
                if next_move[0] == 1: 
                    action_idx = 4
                else: 
                    action_idx = 1
            else:
                if next_move[1] == 1: 
                    action_idx = 3
                else: 
                    action_idx = 0
            
            # this will choose one of random actions
            actions = ["left", "up", "stay", "right", "down"]
            #random_index = random.randint(0, len(actions) - 1)
        
            print("Panic action: ", actions[action_idx], file=sys.stderr, flush=True)
            # print(actions[random_index], flush=True)
            print(actions[action_idx], flush=True)
    
        
    else:
        next_move = tuple(map(lambda i, j: i - j, path[1], (PlayerX, PlayerY)))
        print("x,y - path[1]: ", next_move, file=sys.stderr, flush=True)
        action_idx = 2
        if(next_move[0] != 0): 
            if next_move[0] == 1: 
                action_idx = 4
            else: 
                action_idx = 1
        else:
            if next_move[1] == 1: 
                action_idx = 3
            else: 
                action_idx = 0
        
        # this will choose one of random actions
        actions = ["left", "up", "stay", "right", "down"]
        #random_index = random.randint(0, len(actions) - 1)
    
        print("action: ", actions[action_idx], file=sys.stderr, flush=True)
        # print(actions[random_index], flush=True)
        print(actions[action_idx], flush=True)