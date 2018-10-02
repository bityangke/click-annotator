import tkinter as tk
from tool import *
from PIL import Image, ImageTk

#应用类型
class Application:
    
    #初始化窗口应用
    def __init__(self, config="800x700+500+100"):
        self.initData()
        self.initWindow()

    #初始化窗口内容
    def initWindow(self, config="900x800+500+100"):
        self.app = tk.Tk()
        self.app.geometry(config)
        self.app.title("click annotator")

        guideInfo = "点击开始后进入图片标注，根据文字点击图片中相应的目标物体！"
        self.guide = tk.Message(self.app, text=guideInfo, font=("times", 28),
                                width=500, pady=100)
        self.guide.pack()
        
        self.start = tk.Button(self.app, text="开始", bg='#76c61d',
                         font=("times", 16), width=10, command=self.onStart)
        self.start.pack()
        

    #初始化数据
    def initData(self):
        self.dir = "VOCdevkit/VOC2007/JPEGImages/"
        self.counter = 1
        self.type = ".jpg"
        self.image = None
        self.size = None

        self.pro = Processor()
        
    #响应点击开始标注按钮
    def onStart(self):
        self.guide.destroy()
        self.start.destroy()

        self.placeholder = tk.Canvas(self.app, width=175, height=30)
        self.placeholder.grid(row=0, column=0)
        
        self.panel = tk.Canvas(self.app, width=550, height=550, bg='#cecece')
        self.loadImage()
        self.panel.grid(row=1, column=1, columnspan=2)

        self.info = tk.StringVar()
        self.info.set(str(self.counter).zfill(6) + self.type)
        self.message = tk.Message(self.app, textvariable=self.info,
                        width=100, pady=20)
        self.message.grid(row=2, column=1, columnspan=2)

        self.last = tk.Button(self.app, text="last", bg='#76c61d',
                        font=("Arial", 14), width=10, command=self.onLeftKey)
        self.last.grid(row=3, column=1)
        self.next = tk.Button(self.app, text="next", bg='#76c61d',
                        font=("Arial", 14), width=10, command=self.onRightKey)

        self.next.grid(row=3, column=2)

        self.app.bind('<Left>', self.onLeftKey)
        self.app.bind('<Right>', self.onRightKey)
        self.panel.bind('<ButtonRelease-1>', self.onClick)
        
    #响应键盘左键点击
    def onLeftKey(self, event=None):
        self.counter = max(1, self.counter-1)
        self.loadImage()
        self.info.set(str(self.counter).zfill(6) + self.type)

    #响应键盘右键点击
    def onRightKey(self, event=None):
        self.counter = min(9963, self.counter+1)
        self.loadImage()
        self.info.set(str(self.counter).zfill(6) + self.type)

    #响应鼠标左键点击
    def onClick(self, event):
        sx, ex = event.x - 3, event.x + 3
        sy, ey = event.y - 3, event.y + 3
        self.panel.create_oval(sx,sy,ex, ey, fill = "yellow", tags = "oval")

    #加载图片
    def loadImage(self):
        self.panel.delete("all")
        path = self.dir + str(self.counter).zfill(6) + self.type
        self.size, self.image = self.pro.readImage(path)
        x = (550 - self.size[0]) / 2
        y = (550 - self.size[1]) / 2
        self.panel.create_image(x, y, anchor='nw', image=self.image)
    
    #运行应用程序
    def run(self):
        self.app.mainloop()

if __name__ == '__main__':
    app = Application()
    app.run()
