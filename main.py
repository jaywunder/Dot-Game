from PIL import Image, ImageTk,GifImagePlugin
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
        self.img.save("image.gif","GIF")
        #self.img.load()
        #self.dot.load()
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
        self.img.save("image.gif","GIF")

        if self.failed != 0:
            self.main(self.failed)

class Window(tk.Frame):
    def __init__(self,master=None):
        #self.img = img
        tk.Frame.__init__(self,master,height=HEIGHT,width=WIDTH,relief='solid',borderwidth=3)
        self.pack()
        self.createWidgets()
        self.lineState = False

    def createWidgets(self):
        self.img = Image.open('/Users/JacobWunder/Desktop/image.gif')
        self.gameImage = ImageTk.PhotoImage(self.img)
        
        #self.canvas.create_image((WIDTH/2,HEIGHT/2),image=self.gameImage)
        self.canvas = tk.Canvas(self,height=HEIGHT,width=WIDTH,image=self.gameImage)
        self.canvas.pack()
        
        self.lineImage = Image.new("RGB",(5,5),(256,256,256)) #(250,250,230)
        self.gameImage.paste(self.lineImage,(10,10))
        
        self.canvas.bind(sequence="<ButtonPress-1>",func=self.startLine)
        tk.Frame.bind(sequence="<Motion>",func=self.drawLine)
        
    def startLine(self,event):
        #self.gameImage.putpixel((event.x,event.y),0)
        print((event.x,event.y))
        self.canvas.update()
        if self.lineState == False:
            self.lineState = True
            print(self.lineState)
            
        elif self.lineState == True:
            self.lineState = False
            self.gameImage.show()
            print(self.lineState)
        
    def drawLine(self,event):
        while self.lineState == True:
            self.img.paste(self.lineImage,(event.x,event.y))
            

def windowLoop(window):
    while True:
        window.geometry('%dx%d+%d+%d' % (WIDTH+14,HEIGHT+14,100,100))
        time.sleep(0.1)
        
if __name__ == "__main__":
    root = tk.Tk()
    Game = DotGame(20)
    GameWindow = Window(master=root)
    root.mainloop()
    windowLoop(root)
