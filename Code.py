import pyxel as px
import random as rng
import Sort

class app:
    def __init__(self):
        self.SizeX = 32
        self.SizeY = 32
        self.entities = []
        self.UIentities = []
        for i in range(1):
            self.entities.append(Water(self, rng.randint(0, self.SizeX - 1), rng.randint(0, self.SizeY - 1), 1))
        for i, e in enumerate(self.entities):
            for E in self.entities[i + 1:]:
                if e.PosX == E.PosX and e.PosY == E.PosY:
                    self.entities.remove(E)
        for e in self.entities:
            e.Create_Sand()
        for i in range(50):
            self.entities.append(Bush(self))
        for i in range(100):
            self.entities.append(Woodle(self, (rng.randint(100, 200) / 100), (rng.randint(100, 200)), (rng.randint(75, 100)), (rng.randint(75, 100))))
        self.UIentities.append(Mouse(self))
        px.init(self.SizeX * 8, self.SizeY * 8, fps = 50)
        px.load("recursos.pyxres")
        greens = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2]
        self.background = [[rng.choice(greens) for i in range(self.SizeX * 8)] for j in range(self.SizeY * 8)]
        self.Amount_Woodles = 0
        px.run(self.update, self.draw)

    def update(self):
        for e in self.entities:
            e.update()
        for E in self.UIentities:
            E.update()

    def draw(self):
        self.Amount_Woodles = 0
        for i in range(self.SizeX * 8):
            for j in range(self.SizeY * 8):
                px.pset(i, j, self.background[i][j])
        for e in self.entities:
            if isinstance(e, Woodle):
                e.draw_shadow()
        for e in self.entities:
            e.draw()
        for e in self.entities:
            if isinstance(e, Woodle):
                self.Amount_Woodles += 1
        px.text(2, self.SizeY * 8 - 7, f"Woodles: {self.Amount_Woodles}", 5)
        for E in self.UIentities:
            E.draw()
    
    def Collides(self, Entity1, Entity2):
        s1X, s1Y, e1X, e1Y = Entity1.hitbox()
        s2X, s2Y, e2X, e2Y = Entity2.hitbox()
        OverlapX = (max(s1X, s2X) <= min(e1X, e2X))
        OverlapY = (max(s1Y, s2Y) <= min(e1Y, e2Y))
        return OverlapX and OverlapY
    
    def Closest_Points(self, Entity1, Entity2):
        s1X, s1Y, e1X, e1Y = Entity1.hitbox()
        s2X, s2Y, e2X, e2Y = Entity2.hitbox()
        if s2X > e1X:
            closest_x2 = s2X
        elif e2X < s1X:
            closest_x2 = e2X
        else:
            closest_x2 = max(s1X, s2X)
        if s2Y > e1Y:
            closest_y2 = s2Y
        elif e2Y < s1Y:
            closest_y2 = e2Y
        else:
            closest_y2 = max(s1Y, s2Y)
        if s1X > e2X:
            closest_x1 = s1X
        elif e1X < s2X:
            closest_x1 = e1X
        else:
            closest_x1 = max(s1X, s2X)
        if s1Y > e2Y:
            closest_y1 = s1Y
        elif e1Y < s2Y:
            closest_y1 = e1Y
        else:
            closest_y1 = max(s1Y, s2Y)
        return (closest_x2 - closest_x1, closest_y2 - closest_y1)

    def Average(self, num1, num2):
        return (num1 + num2) / 2
    
class Mouse:
    def __init__(self, app):
        self.app = app
        self.showUI = False 
        self.entity = None

    def update(self):
        if px.btnp(px.MOUSE_BUTTON_LEFT):
            for e in self.app.entities:
                if isinstance (e, Woodle) or isinstance(e, Bush):
                    if self.app.Collides(self, e):
                        self.showUI = True
                        self.entity = e
                        break
                    else:
                        self.showUI = False
        if self.entity in self.app.entities:
            pass
        else:
            self.showUI = False

    def draw(self):
        if self.showUI:
            if isinstance(self.entity, Woodle):
                px.blt(0, 0, 0, 16, 0, 80, 40, 0)
                if self.entity.Is_Baby:
                    px.blt(2, 2, 0, 8, 40, 8, 8, 0)
                else:
                    px.blt(1, 1, 0, 8, 0, 8, 8, 0)
            if isinstance(self.entity, Bush):
                px.blt(0, 0, 0, 96, 0, 21, 16, 0)
        if self.showUI: 
            if isinstance(self.entity, Woodle):
                if self.entity.Is_Baby:
                    px.blt(self.entity.PosX + 1, self.entity.PosY + 1, 0, 0, 72, 7, 6, 0)
                else:
                    px.blt(self.entity.PosX, self.entity.PosY, 0, 0, 32, 7, 6, 0)
                if self.entity.Gender == "Male":
                    px.blt(8, 1, 0, 8, 24, 8, 8, 0)
                else:
                    px.blt(8, 1, 0, 8, 32, 8, 8, 0)
                px.rect(2, 10, round(self.entity.Thirst / 5), 4, 6)
                px.rect(round(self.entity.Max_Thirst / 5) + 2, 10, 20 - round(self.entity.Max_Thirst / 5), 4, 5)
                px.rect(2, 18, round(self.entity.Hunger / 5), 4, 9)
                px.rect(round(self.entity.Max_Hunger / 5) + 2, 18, 20 - round(self.entity.Max_Hunger / 5), 4, 5)
                px.rect(2, 26, round(self.entity.Mating / 5), 4, 11)
                px.text(32, 2, f"Speed:{self.entity.Speed}", 5)
                px.text(32, 9, f"Sight:{self.entity.Sight}", 5)
                px.text(32, 16, f"{self.entity.Age} years old", 5)
                px.text(32, 23, f"{self.entity.objective}", 5)
            if isinstance(self.entity, Bush):
                if self.entity.Max_Cherries == 6:
                    px.blt(self.entity.PosX - 1, self.entity.PosY - 1, 1, 8, 24, 10, 10, 0)
                if self.entity.Max_Cherries == 5:
                    px.blt(self.entity.PosX - 1, self.entity.PosY - 1, 1, 8, 34, 10, 10, 0)
                if self.entity.Max_Cherries == 4:
                    px.blt(self.entity.PosX - 1, self.entity.PosY - 1, 1, 8, 44, 10, 10, 0)
                if self.entity.Max_Cherries == 3:
                    px.blt(self.entity.PosX - 1, self.entity.PosY - 1, 1, 8, 54, 9, 10, 0)
                px.rect(2, 10, self.entity.Amount_Cherries * 2, 4, 9)
                if self.entity.Max_Cherries == 5:
                    px.rect(12, 10, 2, 4, 5)
                if self.entity.Max_Cherries == 4:
                    px.rect(10, 10, 4, 4, 5)
                if self.entity.Max_Cherries == 3:
                    px.rect(8, 10, 6, 4, 5)
        px.blt(px.mouse_x - 3, px.mouse_y - 3, 0, 0, 0, 7, 7, 0)
    def hitbox(self):
        return px.mouse_x, px.mouse_y, px.mouse_x, px.mouse_y

class Woodle:
    def __init__(self, app, speed, sight, max_thirst, max_hunger, PosX = None, PosY = None):
        self.app = app
        if rng.randint(0, 1) == 0:
            self.Gender = "Male"
        else:
            self.Gender = "Female"
        self.Frustration = 0
        self.Max_Thirst = max_thirst
        self.Thirst = self.Max_Thirst
        self.Max_Hunger = max_hunger
        self.Hunger = self.Max_Hunger
        self.Mating = rng.randint(0, 50)
        self.Age = 0
        self.Speed = speed
        self.Sight = sight
        self.Speed -= self.Sight / 1000
        if self.Speed < 1:
            self.Speed = 1 + rng.randint(0, 10) / 100
        self.Sight -= self.Speed * 5
        if self.Sight < 100:
            self.Sight = 100 + rng.randint(0, 10)
        self.Sight = round(self.Sight)
        self.Speed = round(self.Speed, 2)
        self.Death_Age = rng.randint(60, 90)
        self.Is_Baby = False
        if PosX is None:
            self.Birth_Frame = 0
            self.Age = rng.randint(10, 20)
            collides_with_water = True
            while collides_with_water:
                self.PosX = rng.randint(0, self.app.SizeX * 8 - 7)
                self.PosY = rng.randint(0, self.app.SizeY * 8 - 6)
                collides_with_water = False
                for e in self.app.entities:
                    if isinstance(e, Water):
                        if self.app.Collides(self, e):
                            collides_with_water = True
                            break
        else:
            self.PosX = PosX
            self.PosY = PosY
            self.Is_Baby = True
            self.Birth_Frame = px.frame_count
        if self.Age < 14:
            self.Is_Baby = True
        self.objective = ""
        self.Move = [0, 0]
        self.Sprite = [8, 0]
        self.Rem_Steps = 0
        self.Last_Dir = None
        self.List_All_Bushes = []
        for e in self.app.entities:
            if isinstance(e, Bush):
                dx, dy = self.app.Closest_Points(self, e)
                self.List_All_Bushes.append([e, dx, dy, abs(dx) + abs(dy), True])
        self.List_All_Bushes = Sort.QuickSort(self.List_All_Bushes, 3)
    
    def Find_Water(self):
        closest_water = []
        Min_Distance = self.app.SizeX * self.app.SizeY
        for e in self.app.entities:
            if isinstance(e, Water):
                dx, dy = self.app.Closest_Points(self, e)
                if abs(dx) + abs(dy) < Min_Distance:
                    Min_Distance = abs(dx) + abs(dy)
                    closest_water = [dx, dy]
        if abs(closest_water[0]) + abs(closest_water[1]) <= self.Sight:
            return closest_water
        else:
            return [None, None]
    
    def update(self):
        self.objective = "Nothing"
        self.Thirst -= 0.1 * self.Speed * (self.app.Amount_Woodles / 100)
        self.Hunger -= 0.025 * self.Speed * (self.app.Amount_Woodles / 100)
        if (px.frame_count - self.Birth_Frame) % 100 == 0:
            self.Age += 1
        if not self.Is_Baby:
            self.Mating += 0.1 / (rng.randint(100, 200) / 50)
            if self.Mating >= 100:
                self.Mating = 100
        if self.Age > 13:
            self.Is_Baby = False
        self.Frustration -= 0.1
        if self.Thirst < 0 or self.Hunger < 0 or self.Age == self.Death_Age:
            self.app.entities.remove(self)
        maxrandom_number = 5
        if (self.Hunger < 50 and self.Hunger < self.Thirst) or self.Hunger < 10:
            self.objective = "Find Food"
            if px.frame_count % (round(1.5 / self.Speed * 2)) == 0:
                for self.Bush_Index in range(len(self.List_All_Bushes)):
                    bush, MoveX, MoveY, Distance, Valid = self.List_All_Bushes[self.Bush_Index]
                    if bush.Amount_Cherries > 0 and Valid:
                        break
                if Distance <= self.Sight:
                    if MoveX is not None:
                        if rng.randint(0, 1) == 0:
                            if MoveX > 0:
                                self.Move = [1, 0]
                                self.Sprite = [0, 8]
                                self.Last_Dir = "right"
                            elif MoveX < 0:
                                self.Move = [-1, 0]
                                self.Sprite = [8, 8]
                                self.Last_Dir = "left"
                        else:
                            if MoveY > 0:
                                self.Move = [0, 1]
                                self.Sprite = [8, 16]
                                self.Last_Dir = "down"
                            elif MoveY < 0:
                                self.Move = [0, -1]
                                self.Sprite = [0, 16]
                                self.Last_Dir = "up"
                        if abs(MoveX) < 3 and abs(MoveY) < 3:
                            self.Hunger = self.Max_Hunger
                            self.Sprite = [8, 0]
                            bush.Amount_Cherries -= 1
                            for i in range(len(self.List_All_Bushes)):
                                self.List_All_Bushes[i][4] = True
                        self.Rem_Steps = 1
        if (self.Thirst < 50 and self.Thirst < self.Hunger) or self.Thirst < 10:
            self.objective = "Find Water"
            if px.frame_count % (round(1.5 / self.Speed * 2)) == 0:
                MoveX, MoveY = self.Find_Water()
                if MoveX is not None:
                    if rng.randint(0, 1) == 0:
                        if MoveX > 0:
                            self.Move = [1, 0]
                            self.Sprite = [0, 8]
                            self.Last_Dir = "right"
                        elif MoveX < 0:
                            self.Move = [-1, 0]
                            self.Sprite = [8, 8]
                            self.Last_Dir = "left"
                    else:
                        if MoveY > 0:
                            self.Move = [0, 1]
                            self.Sprite = [8, 16]
                            self.Last_Dir = "down"
                        elif MoveY < 0:
                            self.Move = [0, -1]
                            self.Sprite = [0, 16]
                            self.Last_Dir = "up"
                    if abs(MoveX) < 3 and abs(MoveY) < 3:
                        self.Thirst = self.Max_Thirst
                        self.Sprite = [8, 0]
                    self.Rem_Steps = 1
        if maxrandom_number != 0:
            if px.frame_count % (round(maxrandom_number / (self.Speed * 2))) == 0:
                if self.Rem_Steps > 0:
                    self.Rem_Steps -= 1
                    if not self.can_move(self.Move):
                        if self.Mating == 100:
                            for e in self.app.entities:
                                if isinstance(e, Woodle):
                                    if self.app.Collides(self, e):
                                        if e.Mating == 100:
                                            if self.Gender == "Male" and e.Gender == "Female":
                                                self.Mating == 0
                                            if self.Gender == "Female" and e.Gender == "Male":
                                                self.app.entities.append(Woodle(self.app, self.app.Average(self.Speed, e.Speed), self.app.Average(self.Sight, e.Sight), self.app.Average(self.Max_Thirst, e.Max_Thirst), self.app.Average(self.Max_Hunger, e.Max_Hunger), self.PosX, self.PosY))
                        if self.objective == "Find Food":
                            self.Frustration += 15
                            if self.Frustration >= 100:
                                self.List_All_Bushes[self.Bush_Index][4] = False
                                self.Frustration = 15
                        self.Rem_Steps = 0
                    else:
                        if self.Hunger < 50:
                            for i, b in enumerate(self.List_All_Bushes):
                                dx, dy = self.app.Closest_Points(self, self.List_All_Bushes[i][0])
                                self.List_All_Bushes[i][1] = dx
                                self.List_All_Bushes[i][2] = dy
                                self.List_All_Bushes[i][3] = abs(dx) + abs(dy)
                            self.List_All_Bushes = Sort.InsertSort(self.List_All_Bushes, 3)
                else:
                    match rng.randint(0, maxrandom_number):
                        case 0:
                            if not self.Last_Dir == "left":
                                self.Move = [1, 0]
                                self.Sprite = [0, 8]
                                self.Last_Dir = "right"
                        case 1:
                            if not self.Last_Dir == "up":
                                self.Move = [0, 1]
                                self.Sprite = [8, 16]
                                self.Last_Dir = "down"
                        case 2:
                            if not self.Last_Dir == "right":
                                self.Move = [-1, 0]
                                self.Sprite = [8, 8]
                                self.Last_Dir = "left"
                        case 3:
                            if not self.Last_Dir == "down":
                                self.Move = [0, -1]
                                self.Sprite = [0, 16]
                                self.Last_Dir = "up"
                        case 4:
                            if self.Last_Dir is not None:
                                self.Move = [0, 0]
                                self.Sprite = [8, 0]
                                self.Last_Dir = None
                        case 5:
                            if self.Last_Dir is not None:
                                self.Move = [0, 0]
                                self.Sprite = [8, 0]
                                self.Last_Dir = None
                    self.Rem_Steps = rng.randint(2, 5)
        else:
            match self.Last_Dir:
                case "right":
                    self.Move = [-1, 0]
                case "down":
                    self.Move = [0, -1]
                case "left":
                    self.Move = [1, 0]
                case "up":
                    self.Move = [0, 1]
            self.PosX += self.Move[0]
            self.PosY += self.Move[1]
            self.Rem_Steps = 0

    def draw(self):
        if self.Is_Baby:
            px.blt(self.PosX + 1, self.PosY + 1, 0, self.Sprite[0], self.Sprite[1] + 40, 8, 8, 0)
        else:
            px.blt(self.PosX, self.PosY, 0, self.Sprite[0], self.Sprite[1], 8, 8, 0)
    
    def draw_shadow(self):
        if self.Is_Baby:
            px.blt(self.PosX, self.PosY, 0, 0, 64, 8, 8, 0)
        else:
            px.blt(self.PosX, self.PosY, 0, 0, 24, 8, 8, 0)
    
    def hitbox(self):
        return (self.PosX + 1, self.PosY + 1, self.PosX + 5, self.PosY + 4)
        
    def can_move(self, dir): 
        self.PosX += dir[0]
        self.PosY += dir[1]
        for e in self.app.entities:
            if isinstance(e, Water):
                if self.app.Collides(self, e):
                    self.PosX -= dir[0]
                    self.PosY -= dir[1]
                    return False
        if self.PosX <= 0:
            self.PosX -= dir[0]
            self.PosY -= dir[1]
            return False
        if self.PosX >= px.width - 6:
            self.PosX -= dir[0]
            self.PosY -= dir[1]
            return False
        if self.PosY <= 0:
            self.PosX -= dir[0]
            self.PosY -= dir[1]
            return False
        if self.PosY >= px.height - 5:
            self.PosX -= dir[0]
            self.PosY -= dir[1]
            return False
        return True
    
class Bush:
    def __init__(self, app):
        self.app = app
        self.Max_Cherries = rng.randint(3, 6)
        self.Amount_Cherries = self.Max_Cherries
        self.Growth_Rate = (rng.randint(200, 400))
        collides_with_water = True
        while collides_with_water:
            self.PosX = rng.randint(0, self.app.SizeX * 8 - 8)
            self.PosY = rng.randint(0, self.app.SizeY * 8 - 8)
            collides_with_water = False
            for e in self.app.entities:
                if isinstance(e, Water):
                    if self.app.Collides(self, e):
                        collides_with_water = True
                        break

    def update(self):
        if px.frame_count % self.Growth_Rate == 0:
            self.Amount_Cherries += 1
            if self.Amount_Cherries > self.Max_Cherries:
                self.Amount_Cherries = self.Max_Cherries
        
    def draw(self):
        if self.Max_Cherries == 3:
            px.blt(self.PosX, self.PosY, 1, 0, 48, 8, 8, 0)
            if self.Amount_Cherries == 3:
                px.pset(self.PosX + 2, self.PosY + 3, 9)
                px.pset(self.PosX + 4, self.PosY + 5, 9)
                px.pset(self.PosX + 2, self.PosY + 6, 9)
            if self.Amount_Cherries == 2:
                px.pset(self.PosX + 2, self.PosY + 3, 9)
                px.pset(self.PosX + 4, self.PosY + 5, 9)
            if self.Amount_Cherries == 1:
                px.pset(self.PosX + 2, self.PosY + 3, 9)
        if self.Max_Cherries == 4:
            px.blt(self.PosX, self.PosY, 1, 0, 40, 8, 8, 0)
            if self.Amount_Cherries == 4:
                px.pset(self.PosX + 5, self.PosY + 3, 9)
                px.pset(self.PosX + 4, self.PosY + 6, 9)
                px.pset(self.PosX + 3, self.PosY + 1, 9)
                px.pset(self.PosX + 2, self.PosY + 4, 9)
            if self.Amount_Cherries == 3:
                px.pset(self.PosX + 5, self.PosY + 3, 9)
                px.pset(self.PosX + 4, self.PosY + 6, 9)
                px.pset(self.PosX + 3, self.PosY + 1, 9)
            if self.Amount_Cherries == 2:
                px.pset(self.PosX + 5, self.PosY + 3, 9)
                px.pset(self.PosX + 4, self.PosY + 6, 9)
            if self.Amount_Cherries == 1:
                px.pset(self.PosX + 5, self.PosY + 3, 9)
        if self.Max_Cherries == 5:
            px.blt(self.PosX, self.PosY, 1, 0, 32, 8, 8, 0)
            if self.Amount_Cherries == 5:
                px.pset(self.PosX + 4, self.PosY + 5, 9)
                px.pset(self.PosX + 1, self.PosY + 4, 9)
                px.pset(self.PosX + 3, self.PosY + 7, 9)
                px.pset(self.PosX + 4, self.PosY + 2, 9)
                px.pset(self.PosX + 6, self.PosY + 5, 9)
            if self.Amount_Cherries == 4:
                px.pset(self.PosX + 4, self.PosY + 5, 9)
                px.pset(self.PosX + 1, self.PosY + 4, 9)
                px.pset(self.PosX + 3, self.PosY + 7, 9)
                px.pset(self.PosX + 4, self.PosY + 2, 9)
            if self.Amount_Cherries == 3:
                px.pset(self.PosX + 4, self.PosY + 5, 9)
                px.pset(self.PosX + 1, self.PosY + 4, 9)
                px.pset(self.PosX + 3, self.PosY + 7, 9)
            if self.Amount_Cherries == 2:
                px.pset(self.PosX + 4, self.PosY + 5, 9)
                px.pset(self.PosX + 1, self.PosY + 4, 9)
            if self.Amount_Cherries == 1:
                px.pset(self.PosX + 4, self.PosY + 5, 9)
        if self.Max_Cherries == 6:
            px.blt(self.PosX, self.PosY, 1, 0, 24, 8, 8, 0)
            if self.Amount_Cherries == 6:
                px.pset(self.PosX + 6, self.PosY + 4, 9)
                px.pset(self.PosX + 2, self.PosY + 2, 9)
                px.pset(self.PosX + 2, self.PosY + 6, 9)
                px.pset(self.PosX + 4, self.PosY + 1, 9)
                px.pset(self.PosX + 5, self.PosY + 6, 9)
                px.pset(self.PosX + 3, self.PosY + 4, 9)
            if self.Amount_Cherries == 5:
                px.pset(self.PosX + 6, self.PosY + 4, 9)
                px.pset(self.PosX + 2, self.PosY + 2, 9)
                px.pset(self.PosX + 2, self.PosY + 6, 9)
                px.pset(self.PosX + 4, self.PosY + 1, 9)
                px.pset(self.PosX + 5, self.PosY + 6, 9)
            if self.Amount_Cherries == 4:
                px.pset(self.PosX + 6, self.PosY + 4, 9)
                px.pset(self.PosX + 2, self.PosY + 2, 9)
                px.pset(self.PosX + 2, self.PosY + 6, 9)
                px.pset(self.PosX + 4, self.PosY + 1, 9)
            if self.Amount_Cherries == 3:
                px.pset(self.PosX + 6, self.PosY + 4, 9)
                px.pset(self.PosX + 2, self.PosY + 2, 9)
                px.pset(self.PosX + 2, self.PosY + 6, 9)
            if self.Amount_Cherries == 2:
                px.pset(self.PosX + 6, self.PosY + 4, 9)
                px.pset(self.PosX + 2, self.PosY + 2, 9)
            if self.Amount_Cherries == 1:
                px.pset(self.PosX + 6, self.PosY + 4, 9)
    
    def hitbox(self):
        return self.PosX, self.PosY, self.PosX + 8, self.PosY + 8

class Water:
    def __init__(self, app, PosX, PosY, Generation):
        self.app = app
        self.PosX = PosX
        self.PosY = PosY
        if rng.randint(0, 10) == 0 and Generation > 17:
            self.PosX = rng.randint(0, self.app.SizeX - 1)
            self.PosY = rng.randint(0, self.app.SizeY - 1)
        self.Gen = Generation
        self.sprite = [0, 0]
        self.sand = ["up", "down", "right", "left"]
        if self.Gen < 20:
            self.Create_Water()

    def update(self):
        if px.frame_count % 10 == 0:
            if self.sprite == [0, 0]:
                self.sprite = [8, 0]
            elif self.sprite == [8, 0]:
                self.sprite = [0, 8]
            elif self.sprite == [0, 8]:
                self.sprite = [8, 8]
            elif self.sprite == [8, 8]:
                self.sprite = [0, 16]
            elif self.sprite == [0, 16]:
                self.sprite = [8, 16]
            elif self.sprite == [8, 16]:
                self.sprite = [0, 0]

    def draw(self):
        if self.sprite == [0, 0]:
            px.blt(self.PosX * 8, self.PosY * 8, 1, 0, 0, 8, 8)
        elif self.sprite == [8, 0]:
            px.blt(self.PosX * 8, self.PosY * 8, 1, 8, 0, 8, 8)
        elif self.sprite == [0, 8]:
            px.blt(self.PosX * 8, self.PosY * 8, 1, 0, 8, 8, 8)
        elif self.sprite == [8, 8]:
            px.blt(self.PosX * 8, self.PosY * 8, 1, 8, 8, 8, 8)
        elif self.sprite == [0, 16]:
            px.blt(self.PosX * 8, self.PosY * 8, 1, 0, 16, 8, 8)
        elif self.sprite == [8, 16]:
            px.blt(self.PosX * 8, self.PosY * 8, 1, 8, 16, 8, 8)
        if "up" in self.sand:
            px.blt(self.PosX * 8, self.PosY * 8, 1, 16, 0, 8, 8, 0)
        if "right" in self.sand:
            px.blt(self.PosX * 8, self.PosY * 8, 1, 24, 0, 8, 8, 0)
        if "down" in self.sand:
            px.blt(self.PosX * 8, self.PosY * 8, 1, 16, 8, 8, 8, 0)
        if "left" in self.sand:
            px.blt(self.PosX * 8, self.PosY * 8, 1, 24, 8, 8, 8, 0)
    
    def hitbox(self):
        return self.PosX * 8 + 1, self.PosY * 8 + 1, self.PosX * 8 + 6, self.PosY * 8 + 6
    
    def Create_Sand(self):
        self.sand = ["up", "down", "right", "left"]
        for e in self.app.entities:
            if isinstance(e, Water):
                if self.PosY - 1 >= 0:
                    if self.PosY - 1 == e.PosY and self.PosX == e.PosX:
                        if "up" in self.sand:
                            self.sand.remove("up")
                if self.PosX + 1 < self.app.SizeX:
                    if self.PosX + 1 == e.PosX and self.PosY == e.PosY:
                        if "right" in self.sand:
                            self.sand.remove("right")
                if self.PosY + 1 < self.app.SizeY:
                    if self.PosY + 1 == e.PosY and self.PosX == e.PosX:
                        if "down" in self.sand:
                            self.sand.remove("down")
                if self.PosX - 1 >= 0:
                    if self.PosX - 1 == e.PosX and self.PosY == e.PosY:
                        if "left" in self.sand:
                            self.sand.remove("left")
    
    def Create_Water(self):
        amount = 0
        if rng.randint(0, 4) == 0:
            if self.PosX - 1 >= 0:
                self.app.entities.append(Water(self.app, self.PosX - 1, self.PosY, self.Gen + 1))
                amount += 1
        if rng.randint(0, 4) == 0:
            if self.PosX + 1 < self.app.SizeX:
                self.app.entities.append(Water(self.app, self.PosX + 1, self.PosY, self.Gen + 1))
                amount += 1
        if rng.randint(0, 4) == 0:
            if self.PosY - 1 >= 0:
                self.app.entities.append(Water(self.app, self.PosX, self.PosY - 1, self.Gen + 1))
                amount += 1
        if rng.randint(0, 4) == 0:
            if self.PosY + 1 < self.app.SizeY:
                self.app.entities.append(Water(self.app, self.PosX, self.PosY + 1, self.Gen + 1))
                amount += 1
        if amount == 0:
            random = rng.randint(0, 3)
            if random == 0:
                self.app.entities.append(Water(self.app, self.PosX - 1, self.PosY, self.Gen + 1))
            if random == 1:
                self.app.entities.append(Water(self.app, self.PosX + 1, self.PosY, self.Gen + 1))
            if random == 2:
                self.app.entities.append(Water(self.app, self.PosX, self.PosY - 1, self.Gen + 1))
            if random == 3:
                self.app.entities.append(Water(self.app, self.PosX, self.PosY + 1, self.Gen + 1))

app()