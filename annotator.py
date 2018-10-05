import tkinter as tk
from tool import *
from PIL import Image, ImageTk

#应用类型
class Application:
    
    #初始化窗口应用
    def __init__(self, config="800x700+500+100"):
        self.app = tk.Tk()
        self.app.geometry(config)
        self.app.title("click annotator")
        
        self.initData()
        self.initWindow()

    #初始化窗口内容
    def initWindow(self):
        
        #创建顶部占位框
        self.placeholder = tk.Canvas(self.app, height=70)
        self.placeholder.pack(fill='x')
        
        #创建顶部导航栏
        self.navi = tk.Frame(self.app, pady=30)
        self.navi.pack()
        font = ('黑体', 28, 'bold')
        self.navis = []
        navi_text = ['点击.', '.校正.', '.标注']
        width = [5, 6, 5]
        color = [self.RED, self.GREEN, self.GREEN]
        for (i, text) in enumerate(navi_text):
            self.navis.append(tk.Label(self.navi, width=width[i], font=font,
                                fg=color[i], text=text))
            self.navis[i].pack(side='left')
            self.navis[i].bind('<ButtonRelease-1>', self.clickNavi)
        
        #创建说明文字
        font = ('宋体', 18)
        self.info = tk.Message(self.app, textvariable=self.guide_variable,
                        font=font, width=500)
        self.info.pack()
        
        self.start = tk.Button(self.app, text="开始", bg='#76c61d',
                         font=("times", 16), width=10, command=self.onStart)
        self.start.pack()

    #销毁初始化的窗口
    def destroyInit(self):
        self.placeholder.destroy()
        self.navi.destroy()
        for i in range(len(self.navis)):
            self.navis[i].destroy()
        self.navis = None
        self.info.destroy()
        self.start.destroy()

    #导航切换动作
    def clickNavi(self, event):
        for i in range(len(self.navis)):
            if self.navis[i] == event.widget:
                self.navis[i].configure(fg=self.RED)
                self.guide_variable.set(self.guide_text[i])
            else:
                self.navis[i].configure(fg=self.GREEN)
    
    #初始化数据
    def initData(self):
        self.GRAY = '#f7f5ef'
        self.GREEN = '#3CB371'
        self.ORANGE = '#FFA500'
        self.RED = '#FF6347'

        self.guide_text = [
            '    给定一张图片和需要标注的目标,请用鼠标点击目标所在的位置.',
            '    根据系统给出的目标边界框的推测,校正边界框的位置.',
            '    如果认为系统给出的目标边界框推测正确,请点击确认按钮,完成标注.']
        self.guide_variable = tk.StringVar()
        self.guide_variable.set(self.guide_text[0])
        
        self.dir = "VOCdevkit/VOC2007/JPEGImages/"
        self.counter = 1
        self.type = ".jpg"
        self.image = None
        self.size = None

        self.pro = Processor()
        
    #响应点击开始标注按钮
    def onStart(self):
        self.destroyInit()

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
        self.oval = self.panel.create_oval(sx,sy,ex, ey, fill = "yellow",
                        tags="ovals")
        self.app.after(500, self.deleteOvals)

    def deleteOvals(self):
        self.panel.delete("ovals")

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
