import ImageDraw

class Utils:
        def __init__(self,img):
                self.img = img

        # x,y are the center coordinates
        # r is the radius
        def drawCircle(self,x,y,r):
                draw = ImageDraw.Draw(self.img)
                box = ((x-r,y-r),(x+r,y+r))
                draw.ellipse(box,outline = 128)
                del draw
                return self.img
