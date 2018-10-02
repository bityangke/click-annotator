import cv2
from PIL import Image, ImageTk
from xml.dom.minidom import parse
import xml.dom.minidom
import time
import tkinter as tk

#文件处理类型
class Processor:

    #通过路径读取图片
    def readImage(self, path):
        img = Image.open(path)
        return img.size, ImageTk.PhotoImage(img)

    #通过路径解析XML,返回字典
    def readXml(self, path):
        DOMTree = xml.dom.minidom.parse(path)
        collection = DOMTree.documentElement
        objects = collection.getElementsByTagName("object")

        annotates = {}
        name = ["xmin", "ymin", "xmax", "ymax"]
        for item in objects:
            box = []
            for e in name:
                box.append(item.getElementsByTagName(e)[0].childNodes[0].data)
            n = item.getElementsByTagName("name")[0].childNodes[0].data
            annotates[n] = box

        return annotates

    #测试图片读取
    def test(self, path):
        return cv2.imread(path)

if __name__ == '__main__':
    p = Processor()
    t1 = time.time()
    ipath = "VOCdevkit/VOC2007/JPEGImages/000001.jpg"
    xpath = "VOCdevkit/VOC2007/Annotations/000001.xml"
    img = p.test(ipath)
    annotates = p.readXml(xpath)
    t2 = time.time()
    print("time cost for each image: %f", t2-t1)
    print(annotates)
    cv2.imshow("img", img)
