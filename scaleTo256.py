#coding: UTF-8

from PIL import Image
import os

####指定######
dirname = "trainB" #画像ファイル保存されているフォルダ名
##############

path = "/home/ubtaiki/git/CycleGAN/datasets/character/" + dirname
imgNames = os.listdir(path)
save_path = "256pixel/" + dirname

if not os.path.isdir(save_path):  #保存するフォルダ存在しないとき、フォルダ作成
    os.mkdir(save_path)

def readImg(imgName):
    try: #tryを使ってエラーでプログラムが止まっちゃうのを回避します。
        img_src = Image.open(path + "/" + imgName)
    except: #ゴミを読み込んだらこれちゃうで！って言います。
        print("{} is not image file!".format(imgName))
        img_src = 1
    return img_src

for imgName in imgNames: #1つの画像ずつ
    img_src = readImg(imgName)
    if img_src == 1:continue
    else:
        resizedImg = img_src.resize((256,256)) #
        resizedImg.save(save_path + "/" + "256_256_" + imgName)

print "finish"