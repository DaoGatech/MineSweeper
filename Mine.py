#class to represent a Mine
class Mine:
    def __init__(self,sprite):
        self.drawn = False;
        self.sprite = sprite;
        self.red = False;

    def draw(self,turt,x,y):
        if(not self.drawn):
            if(self.red):
                turt.goto(x, y);
                turt.fillcolor("red");
                turt.begin_fill();
                self.sprite.draw(turt,x,y);
                turt.end_fill();
            else:
                self.sprite.draw(turt,x,y);
            self.drawn = True;

    def __str__(self):
        return "BOOM";

    def __repr__(self):
        res = self.__str__();
        return res;
