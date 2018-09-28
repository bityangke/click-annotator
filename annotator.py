import tkinter as tk
from tool import *

#应用类型
class Application:
    
    #初始化窗口应用
    def __init__(self, config="800x700+500+100"):
        self.initData()
        self.initWindow()

    #初始化窗口内容
    def initWindow(self, config="800x700+500+100"):
        self.app = tk.Tk()
        self.app.geometry(config)

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

        self.pro = Processor()
        
    #响应点击开始标注按钮
    def onStart(self):
        self.guide.destroy()
        self.start.destroy()

        self.panel = tk.Label(image=None, width=500, height=500,
                        justify='center', bg='#fff')
        img = Image.open("VOCdevkit/VOC2007/JPEGImages/000001.jpg")
        self.loadImage()
        self.panel.grid(row=0)

        self.info = tk.StringVar()
        self.info.set("默认")
        self.message = tk.Message(self.app, textvariable=self.info,
                        width=100, pady=30)
        self.message.grid(row=1)

        self.last = tk.Button(self.app, text="last", bg='#76c61d',
                        font=("Arial", 14), width=10, command=self.onLeftKey)
        self.last.grid(row=2, column=1)
        self.next = tk.Button(self.app, text="next", bg='#76c61d',
                        font=("Arial", 14), width=10, command=self.onRightKey)

        self.next.grid(row=2, column=2)

        self.app.bind('<Left>', self.onLeftKey)
        self.app.bind('<Right>', self.onRightKey)
        self.app.bind('<ButtonRelease-1>', self.onClick)
    
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
        print(event.x, event.y)

    #加载图片
    def loadImage(self):
        path = self.dir + str(self.counter).zfill(6) + self.type
        img = self.pro.readImage(path)
        self.panel.config(image=img)
        self.panel.image = img
    
    #运行应用程序
    def run(self):
        self.app.mainloop()

if __name__ == '__main__':
    app = Application()
    app.run()
