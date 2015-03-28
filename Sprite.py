#class is to represent Sprite
class Sprite:

    def __init__(self, aList):
        self.pixels = aList;

    def draw(self,turt,x,y):
        move = y;
        turt.goto(x,y);
        for i in range (len(self.pixels)):
            for j in range (len(self.pixels[i])):
                turt.pendown();
                if(self.pixels[i][j] != ' '):
                    turt.pencolor(self.pixels[i][j]);
                turt.forward(1);
            move -= 1;
            turt.goto(x,move);
