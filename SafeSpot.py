#Class is to represent a SafeSpot
class SafeSpot:
    def __init__(self,numAdjacent,sprite):
        self.sprite = sprite;
        self.numAdjacent = numAdjacent;
        self.drawn = False;
        self.count = 0;

    def draw(self,turt,x,y):
        if(self.sprite != None):
            if( not self.drawn):
                self.sprite.draw(turt,x,y);
                self.drawn = True;
        else:
            turt.penup();
            turt.goto(x, y);
            turt.pendown();
            turt.fillcolor("grey")
            turt.begin_fill()
            for i in range(2):
                turt.forward(25);
                turt.right(90);
                turt.forward(25);
                turt.right(90);
            turt.end_fill()

    def __str__(self):
        res = "";
        if(self.drawn):
            res = "<" + str(self.numAdjacent) + ">";
        else:
            res = str(self.numAdjacent);
        return res;

    def __repr__(self):
        res = self.__str__();
        return res;
