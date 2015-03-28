#main Class
#MineSweeper in Python
#Thong Dao

import csv;
import turtle;
import random;
from Mine import Mine;
from Sprite import Sprite;
from SafeSpot import SafeSpot;
turtle.tracer(0);

class MineSweeper:
    def __init__(self,width,height,prob,pixelCSV):
        self.height = height;
        self.width = width;
        self.queue = [];
        self.visited = [];
        self.spriteSetup(pixelCSV);
        self.gridSetup(prob);
        self.screenSetup()

    def spriteSetup(self, pixelCSV):
        count = 0;
        track = 1;
        self.spriteDict = {};
        self.spriteDict[0] = None;
        with open(pixelCSV, 'r') as c:
            reader = csv.reader(c);
            alist = [];
            for i in reader:
                if((count % 25 == 0) & (count > 0)):
                    if(count - 25 == 0):
                        self.spriteDict['mine'] = Sprite(alist[0:count-1]);
                    else:
                        self.spriteDict[track] = Sprite(alist[count-25:count-1]); 
                        track += 1;
                alist.append(i);
                count += 1;
            self.spriteDict[8] = Sprite(alist[200:224]);
    
    def gridSetup(self, prob):
        self.count = 0;
        self.c = 0;
        self.grid = [[] for t in range(self.height)];
        for i in range(len(self.grid)):
            for j in range(self.width):
                self.grid[i].append(None);
        for i in range(self.height):
            for j in range(self.width):
                ran = random.uniform(0.0, 1.0);
                if(ran <= prob):
                    m = Mine(self.spriteDict['mine']);
                    self.grid[i][j]  = m;
        for i in range(self.height):
            for j in range(self.width):
                count = 0;
                if(self.grid[i][j] == None):
                    self.count += 1;
                    try:
                        if(i - 1 >= 0):
                            if((isinstance(self.grid[i-1][j], Mine)) ):
                                count += 1;
                    except IndexError:
                        pass;
                    try:
                        if (i + 1 <= self.height):
                            if((isinstance(self.grid[i+1][j], Mine)) ):
                                count += 1;
                    except IndexError:
                        pass;
                    try:
                        if (j - 1 >= 0):
                            if((isinstance(self.grid[i][j-1], Mine)) ):
                                count += 1;
                    except IndexError:
                        pass;
                    try:
                        if(j+1 <= self.width):
                            if((isinstance(self.grid[i][j+1], Mine)) ):
                                count += 1;
                    except IndexError:
                        pass;
                    try:
                        if((i - 1 >= 0) & (j - 1 >= 0)):
                            if( (isinstance(self.grid[i-1][j-1], Mine)) ):
                                count += 1;
                    except IndexError:
                        pass;
                    try:
                        if((i + 1 <= self.height) & (j + 1 <= self.width)):
                            if((isinstance(self.grid[i+1][j+1], Mine)) ):
                                count += 1;
                    except IndexError:
                        pass;
                    try:
                        if((i - 1 >= 0) & (j + 1 <= self.width)):
                            if(isinstance(self.grid[i-1][j+1], Mine) ):
                                count += 1;
                    except IndexError:
                        pass;
                    try:
                        if((i + 1 <= self.height) & (j - 1 >= 0)):
                            if(isinstance(self.grid[i+1][j-1], Mine) ):
                                count += 1;
                    except IndexError:
                        pass;
                    
                    if(count > 0):
                        s = SafeSpot(count, self.spriteDict[count]);
                        self.grid[i][j] = s;
                    else:
                        s = SafeSpot(0, None);
                        self.grid[i][j] = s;
            
    def screenSetup(self):
        y = 0 - ((self.height * 25) // 2 );
        self.startX = 0 - ((self.width * 25) // 2);
        self.startY = (y-25) + (25*self.height);
        turtle.setup(self.width*50, self.height*75);
        t = turtle.Turtle();
        t.hideturtle();
        self.screen = turtle.Screen();
        self.drawer = t;
        for i in range(self.height):
            t.penup();
            t.setx(self.startX);
            t.sety(y);
            t.pendown();
            for e in range(self.width):
                for j in range(2):
                    t.forward(25);
                    t.right(90);
                    t.forward(25);
                    t.right(90);
                t.goto(t.xcor() + 25, t.ycor());
            y += 25;
        t.penup();
        self.screen.onclick(self.clicked);
        self.screen.listen();
        turtle.mainloop();
        
    def clicked(self, x, y):
       turtle.hideturtle();
       turtle.penup();
       turtle.goto(x, y);
       x = int(abs(turtle.xcor() - self.startX) // 25);
       y = int(abs(turtle.ycor() - self.startY) // 25);
       self.drawer.penup();
       if((y < self.width) & (x < self.height)):
            if(isinstance(self.grid[y][x], Mine)):
                xloc = self.startX + (25*x);
                yloc = self.startY - (25*y);
                self.grid[y][x].red = True;
                self.grid[y][x].draw(self.drawer,xloc, yloc);
                self.grid[y][x].red = False;
                self.drawallMines();
                self.screen.exitonclick();
            elif(isinstance(self.grid[y][x], SafeSpot)):
                if (self.grid[y][x].numAdjacent != 0):
                    self.c += 1;
                    xloc = self.startX + (25*x);
                    yloc = self.startY - (25*y);
                    self.grid[y][x].draw(self.drawer,xloc, yloc);
                else:
                    self.zeroClicked(y, x);
                if(self.c == self.count):
                    self.drawallMines();
                    self.screen.exitonclick();
            
    def checkVisited(self,x, y):
        for i in range(len(self.visited)):
            if((x == self.visited[i][0]) & (y == self.visited[i][1])):
                return True;
        else:
                return False;
                
    def zeroClicked(self, row, col):
        xloc = self.startX + (25*col);
        yloc = self.startY - (25*row);
        self.grid[row][col].draw(self.drawer,xloc, yloc);
        if(not self.checkVisited(row, col)):
            temp = [];
            temp.append(row);
            temp.append(col);
            self.visited.append(temp);
        if(row - 1 >= 0):
            if(self.grid[row-1][col].numAdjacent != 0):
                xloc = self.startX + (25*col);
                yloc = self.startY - (25*(row-1));
                self.grid[row-1][col].draw(self.drawer,xloc, yloc);
            else:
                if(not self.checkVisited(row-1, col)):
                    temp = [];
                    temp.append(row-1);
                    temp.append(col);
                    self.queue.append(temp);
        if (row + 1 < self.height):
            if(self.grid[row+1][col].numAdjacent != 0):
                xloc = self.startX + (25*col);
                yloc = self.startY - (25*(row+1));
                self.grid[row+1][col].draw(self.drawer,xloc, yloc);
            else:
                if(not self.checkVisited(row+1, col)):
                    temp = [];
                    temp.append(row+1);
                    temp.append(col);
                    self.queue.append(temp);
        if (col - 1 >= 0):
            if(self.grid[row][col-1].numAdjacent != 0):
                xloc = self.startX + (25*(col-1));
                yloc = self.startY - (25*row);
                self.grid[row][col-1].draw(self.drawer,xloc, yloc);
            else:
                if(not self.checkVisited(row, col-1)):
                    temp = [];
                    temp.append(row);
                    temp.append(col-1);
                    self.queue.append(temp);
        if(col+1 < self.width):
            if(self.grid[row][col+1].numAdjacent != 0):
                xloc = self.startX + (25*(col+1));
                yloc = self.startY - (25*row);
                self.grid[row][col+1].draw(self.drawer,xloc, yloc);
            else:
                if(not self.checkVisited(row, col+1)):
                    temp = [];
                    temp.append(row);
                    temp.append(col+1);
                    self.queue.append(temp);
        if((row - 1 >= 0) & (col - 1 >= 0)):
            if(self.grid[row-1][col-1].numAdjacent != 0):
                xloc = self.startX + (25*(col-1));
                yloc = self.startY - (25*(row-1));
                self.grid[row-1][col-1].draw(self.drawer,xloc, yloc);
            else:
                if(not self.checkVisited(row-1, col-1)):
                    temp = [];
                    temp.append(row-1);
                    temp.append(col-1);
                    self.queue.append(temp);

        if((row + 1 < self.height) & (col + 1 < self.width)):
            if(self.grid[row+1][col+1].numAdjacent != 0):
                xloc = self.startX + (25*(col+1));
                yloc = self.startY - (25*(row+1));
                self.grid[row+1][col+1].draw(self.drawer,xloc, yloc);
            else:
                if(not self.checkVisited(row+1, col+1)):
                    temp = [];
                    temp.append(row+1);
                    temp.append(col+1);
                    self.queue.append(temp);
                
        if((row - 1 >= 0) & (col + 1 < self.width)):
            if(self.grid[row-1][col+1].numAdjacent != 0):
                xloc = self.startX + (25*(col+1));
                yloc = self.startY - (25*(row-1));
                self.grid[row-1][col+1].draw(self.drawer,xloc, yloc);
            else:
                if(not self.checkVisited(row-1, col+1)):
                    temp = [];
                    temp.append(row-1);
                    temp.append(col+1);
                    self.queue.append(temp);
            
        if((row + 1 < self.height) & (col - 1 >= 0)):
            if(self.grid[row+1][col-1].numAdjacent != 0):
                xloc = self.startX + (25*(col-1));
                yloc = self.startY - (25*(row+1));
                self.grid[row+1][col-1].draw(self.drawer,xloc, yloc);
            else:
                if(not self.checkVisited(row+1, col-1)):
                    temp = [];
                    temp.append(row+1);
                    temp.append(col-1);
                    self.queue.append(temp);
                    
        while(len(self.queue) > 0):
            item = self.queue.pop(0);
            self.zeroClicked(item[0], item[1]);
        return;
            
            
        
    def drawallMines(self):
        for i in range(self.width):
            for j in range(self.height):
                if(isinstance(self.grid[i][j], Mine)):
                    xloc = self.startX + (25*j);
                    yloc = self.startY - (25*i);
                    self.grid[i][j].draw(self.drawer,xloc, yloc);

#call the main method
#MineSweeper(20,20, 0.2, 'sprites.csv');



                
        
        
            
