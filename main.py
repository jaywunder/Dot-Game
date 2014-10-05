from PIL import ImageTk, Image, ImageDraw
from random import randint
import tkinter as tk
import pdb
import time

WIDTH = 480; HEIGHT = 640
Image.init()
#pdb.set_trace()


class DotGame(object):
    def __init__(self,dotAmount):
        self.dotAmount = dotAmount
        self.makeImage()
        self.main(self.dotAmount)
        self.failed = 0
        #self.img.show()
        

    def makeImage(self):
        #Make Images Name    Type   Size           R   G   B
        self.img = Image.new("RGB",(WIDTH,HEIGHT),(220,220,200))
        self.dot = Image.new("RGB",(10   ,10)    ,(0  ,0  ,0  ))
        self.coordList = [((0,1),(0,1))]

    def debug(self,state,x,y):
        if state == True:
            for linex in range(self.posx-20,self.posx+30):
                self.img.putpixel((linex,y+30),(255,0,0))
                self.img.putpixel((linex,y-20),(255,0,0))
            for liney in range(self.posy-20,self.posy+30):
                self.img.putpixel((x+30,liney),(255,0,0))
                self.img.putpixel((x-20,liney),(255,0,0))

    def checkArea(self,x,y):
        self.dotNear = False
        for coord in self.coordList:
            #print((coord[0][0],coord[0][1]),(coord[1][0],coord[1][1]))
            if   x-20 in range(coord[0][0],coord[0][1]) and y-20 in range(coord[1][0],coord[1][1]):
                self.dotNear = True

            elif x-20 in range(coord[0][0],coord[0][1]) and y+30 in range(coord[1][0],coord[1][1]): 
                self.dotNear = True
                
            elif x+30 in range(coord[0][0],coord[0][1]) and y-20 in range(coord[1][0],coord[1][1]):
                self.dotNear = True
                
            elif x+30 in range(coord[0][0],coord[0][1]) and y+30 in range(coord[1][0],coord[1][1]):
                self.dotNear = True
        if not self.dotNear:
            self.coordList.append(((x-20,x+30),(y-20,y+30)))
            #print(self.coordList)
            return True
        else:
            return False
                
        #print(self.coordList)

    def main(self,dotAmount):
        self.failed = 0
        for dot in range(dotAmount):
            self.posx = randint(70,410)
            self.posy = randint(40,600)
            self.debug(False,self.posx,self.posy)
            #print("start: (",self.posx,self.posy,')')
            if self.checkArea(self.posx,self.posy) == True:
                #self.dotList.append((self.posx,self.posy,self.posx+10,self.posy-10))
                self.img.paste(self.dot,(self.posx,self.posy))
            else:
                #print("check failed")
                self.failed += 1
                 
        #print(self.failed)
        self.img.save("image.png","PNG")

        if self.failed != 0:
            self.main(self.failed)


class Window(tk.Tk):
    def __init__(self,master=None):
        tk.Tk.__init__(self)
        self.configure(bg='#DCDCC8')
        self.wm_title("The Dot Game")
        #self.frame = tk.Frame(self,master,height=HEIGHT,width=WIDTH,relief='solid',borderwidth=3)
        self.lineState = False
        #Make Image
        self.img = Image.open(r'image.png')
        self.width, self.height = self.img.size
        #Canvas
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg='red', width=self.width, height=self.height)
        self.canvas.pack()

        self.resetButton = tk.Button(text="Reset",command=self.reset)
        self.newButton = tk.Button(text="New Game",command=self.new)
        self.newButton.pack()
        self.resetButton.pack()
        
        #Drawing format
        self.draw = ImageDraw.Draw(self.img)
        self.draw.rectangle([(WIDTH/2)-5,10,(WIDTH/2)+5,20],fill='red')
        
        #creating and packing gameImage 
        self.gameImage = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.width/2, self.height/2, image=self.gameImage)
        #print(self.img.format, self.img.size, self.img.mode)
        self.canvas.bind(sequence="<Button-1>",func=self.changeLineState)
        self.canvas.bind(sequence="<Motion>",func=self.drawLine)
        self.x0 = WIDTH/2
        self.y0 = 15
        
    def drawLine(self,event):
        if self.lineState == True:
            #self.draw.rectangle([event.x-2,event.y-2,event.x+2,event.y+2],fill='red')
            self.draw.line([self.x0,self.y0,event.x,event.y],fill='red')
            self.gameImage = ImageTk.PhotoImage(self.img)
            self.canvas.create_image(self.width/2, self.height/2, image=self.gameImage)
            self.x0 = event.x
            self.y0 = event.y

    def reset(self):
        self.img = Image.open(r'image.png')
        self.draw = ImageDraw.Draw(self.img)
        self.gameImage = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(self.width/2, self.height/2, image=self.gameImage)
        self.draw.rectangle([(WIDTH/2)-5,10,(WIDTH/2)+5,20],fill='red')
        self.canvas.bind(sequence="<Button-1>",func=self.changeLineState)
        self.canvas.bind(sequence="<Motion>",func=self.drawLine)
        self.x0 = WIDTH/2
        self.y0 = 15

    def new(self):
        Game = DotGame(20)
        self.destroy()
        self.__init__()
        #self.img = Image.open(r'image.png')
        #self.gameImage = ImageTk.PhotoImage(self.img)
        #self.canvas.create_image(self.width/2, self.height/2, image=self.gameImage)

    def changeLineState(self,event):
        if self.lineState == False:
            self.lineState = True
            self.draw.line([self.x0,self.y0,event.x,event.y],fill='red')

        else:
            self.lineState = False

def run():
    Window().mainloop()
if __name__ == "__main__":
    Game = DotGame(20)
    run()

