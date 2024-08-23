import math
import cv2
import numpy
from PIL import ImageEnhance
import os
import numpy as np
from PIL import Image
import random
 
 
def brightnessEnhancement(root_path,img_name):#亮度增强
    image = Image.open(os.path.join(root_path, img_name))
    enh_bri = ImageEnhance.Brightness(image)
    brightness = 1.0+0.3*random.uniform(-1,1)
    #brightness = 1.2
    image_brightened = enh_bri.enhance(brightness)
    return image_brightened
 
 
def contrastEnhancement(root_path, img_name):  # 对比度增强
    image = Image.open(os.path.join(root_path, img_name))
    enh_con = ImageEnhance.Contrast(image)
    contrast = 1.0+0.3*random.uniform(-1,1)
    #contrast = 1.5
    image_contrasted = enh_con.enhance(contrast)
    return image_contrasted
 
def rotation(root_path, img_name):
    img = Image.open(os.path.join(root_path, img_name))
    random_angle = np.random.randint(-2, 2)*90
    if random_angle==0:
     rotation_img = img.rotate(-90) #旋转角度
    else:
        rotation_img = img.rotate( random_angle,expand=True)  # 旋转角度
    # rotation_img.save(os.path.join(root_path,img_name.split('.')[0] + '_rotation.jpg'))
    return rotation_img
 
def flip(root_path,img_name):   #翻转图像
    img = Image.open(os.path.join(root_path, img_name))
    filp_img = img.transpose(Image.FLIP_LEFT_RIGHT)
    # filp_img.save(os.path.join(root_path,img_name.split('.')[0] + '_flip.jpg'))
    return filp_img
 
def fangshe_bianhuan(root_path,img_name): #仿射变化扩充图像
    img = Image.open(os.path.join(root_path, img_name))
 
    img = cv2.cvtColor(numpy.asarray(img) , cv2.COLOR_RGB2BGR)
 
    h, w = img.shape[0], img.shape[1]
    m = cv2.getRotationMatrix2D(center=(w // 2, h // 2), angle=-30, scale=0.5)
    r_img = cv2.warpAffine(src=img, M=m, dsize=(w, h), borderValue=(0, 0, 0))
 
    r_img = Image.fromarray(cv2.cvtColor(r_img, cv2.COLOR_BGR2RGB))
    return r_img
 
def cuoqie(root_path,img_name): #错切变化扩充图像
    img = Image.open(os.path.join(root_path, img_name))
 
    img = cv2.cvtColor(numpy.asarray(img) , cv2.COLOR_RGB2BGR)
 
    h, w = img.shape[0], img.shape[1]
    origin_coord = np.array([[0, 0, 1], [w, 0, 1], [w, h, 1], [0, h, 1]])
 
    theta = 30  # shear角度
    tan = math.tan(math.radians(theta))
 
    # x方向错切
    m = np.eye(3)
    m[0, 1] = tan
    shear_coord = (m @ origin_coord.T).T.astype(int)
    shear_img = cv2.warpAffine(src=img, M=m[:2],
                               dsize=(np.max(shear_coord[:, 0]), np.max(shear_coord[:, 1])),
                               borderValue=(0, 0, 0))
 
 
 
    c_img = Image.fromarray(cv2.cvtColor(shear_img, cv2.COLOR_BGR2RGB))
    return c_img
 
def hsv(root_path,img_name):#HSV数据增强
    h_gain , s_gain , v_gain = 0.5 , 0.5 , 0.5
    img = Image.open(os.path.join(root_path, img_name))
 
    img = cv2.cvtColor(numpy.asarray(img) , cv2.COLOR_RGB2BGR)
 
    r = np.random.uniform(-1, 1, 3) * [h_gain, s_gain, v_gain] + 1  # random gains
    hue, sat, val = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
    dtype = img.dtype  # uint8
 
    x = np.arange(0, 256, dtype=np.int16)
    lut_hue = ((x * r[0]) % 180).astype(dtype)
    lut_sat = np.clip(x * r[1], 0, 255).astype(dtype)
    lut_val = np.clip(x * r[2], 0, 255).astype(dtype)
 
    img_hsv = cv2.merge((cv2.LUT(hue, lut_hue), cv2.LUT(sat, lut_sat), cv2.LUT(val, lut_val))).astype(dtype)
    aug_img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    aug_img = Image.fromarray(cv2.cvtColor(aug_img, cv2.COLOR_BGR2RGB))
    return aug_img
 
def pingyi(root_path,img_name):#平移扩充图像，根图像移动的像素距离可自行调整，具体方法如下注释所示
    img = Image.open(os.path.join(root_path, img_name))
    img = cv2.cvtColor(numpy.asarray(img) , cv2.COLOR_RGB2BGR)
 
    cols , rows= img.shape[0], img.shape[1]
    M = np.float32([[1, 0, 50], [0, 1, 30]])#50为x即水平移动的距离，30为y 即垂直移动的距离
    dst = cv2.warpAffine(img, M, (cols, rows),borderValue=(0,255,0))
    pingyi_img = Image.fromarray(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
    return pingyi_img
import shutil
import os

def changetxt(src_path, dst_dir, new_filename=None):
    """
    复制一个文本文件到指定的目标目录，并允许指定新文件名。

    参数:
    src_path : str
        源文本文件的路径。
    dst_dir : str
        目标目录的路径。
    new_filename : str, optional
        复制后的新文件名。如果未指定，则使用源文件的文件名。
    """
    # 如果没有提供新文件名，则使用源文件名
    if new_filename is None:
        new_filename = os.path.basename(src_path)
    
    # 构造目标文件的完整路径
    dst_path = os.path.join(dst_dir, new_filename)
    
    try:
        # 使用shutil.copy()函数复制文件
        shutil.copy(src_path, dst_path)
        print(f"文件已从 {src_path} 复制到 {dst_path}")
    except IOError as e:
        # 如果发生IO错误，打印错误信息
        print(f"复制文件时发生错误: {e}")
    except Exception as e:
        # 其他可能的错误
        print(f"未知错误，复制文件失败：{e}")

# 使用示例：
# copy_and_save_txt('path/to/source.txt', 'path/to/destination/', 'new_filename.txt')
def duibi(i,name):
    saveName=name[:-4]+"duibi"+str(i)+".jpg"
    saveImage=contrastEnhancement(imageDir,name)
    saveImage.save(os.path.join(saveDir,saveName))
    changetxt(txtDir+name[:-4]+".txt",newtxt,name[:-4]+"duibi"+str(i)+".txt")
def liangdu(i,name):
    saveName2 = name[:-4]+"liangdu"+str(i)+".jpg"
    saveImage2 = brightnessEnhancement(imageDir, name)
    saveImage2.save(os.path.join(saveDir, saveName2))
    changetxt(txtDir+name[:-4]+".txt",newtxt,name[:-4]+"liangdu"+str(i)+".txt")
def hsvb(i,name):
    saveName6 = name[:-4]+"hsv"+str(i)+".jpg"
    saveImage = hsv(imageDir, name)
    saveImage.save(os.path.join(saveDir, saveName6))
    changetxt(txtDir+name[:-4]+".txt",newtxt,name[:-4]+"hsv"+str(i)+".txt")

def createImage(imageDir,saveDir,num):#主函数，8种数据扩充方式，每种扩充一张
   
   for name in os.listdir(imageDir):
       for i in range(num):
            duibi(i,name)
            hsvb(i,name)
            liangdu(i,name)
      
'''
      saveName=name+"duibi"+".jpg"
      saveImage=contrastEnhancement(imageDir,name)
      saveImage.save(os.path.join(saveDir,saveName))
      changetxt(txtDir+name[:-4]+".txt",newtxt,name+"duibi"+".txt")
      #saveName1 = "flip" + str(i) + ".jpg"
      #saveImage1 = flip(imageDir,name)
      #saveImage1.save(os.path.join(saveDir, saveName1))
      saveName2 = name+"liangdu"+".jpg"
      saveImage2 = brightnessEnhancement(imageDir, name)
      saveImage2.save(os.path.join(saveDir, saveName2))
      #saveName3 = "rotate" + str(i) + ".jpg"
      #saveImage = rotation(imageDir, name)
      #saveImage.save(os.path.join(saveDir, saveName3))
      #saveName4 = "fangshe" + str(i) + ".jpg"
      #saveImage = fangshe_bianhuan(imageDir, name)
      #saveImage.save(os.path.join(saveDir, saveName4))
      #saveName5 = "cuoqie" + str(i) + ".jpg"
      #saveImage = cuoqie(imageDir, name)
      #saveImage.save(os.path.join(saveDir, saveName5))
      saveName6 = name+"hsv"+".jpg"
      saveImage = hsv(imageDir, name)
      saveImage.save(os.path.join(saveDir, saveName6))
     # saveName6 = "pingyi" + str(i) + ".jpg"  #不需要平移变换的，可以注释掉 这三行代码 135 136 137行
      #saveImage = pingyi(imageDir, name)     #不需要平移变换的，可以注释掉 这三行代码
      #saveImage.save(os.path.join(saveDir, saveName6)) #不需要平移变换的，可以注释掉 这三行代码
 '''
 
imageDir="smallimage" #要改变的图片的路径文件夹  在当前文件夹下，建立文件夹即可
txtDir="labels/"  ##/不可省略
newtxt="morelabels/"   
num=2      ####变换次数
saveDir="moreimage"   #数据增强生成图片的路径文件夹
print('文件的初始文件夹为：' + imageDir)
print('----------------------------------------')
print('文件的转换后存入的文件夹为：' + saveDir)
print('----------------------------------------')
print('开始转换')
print('----------------------------------------')
createImage(imageDir,saveDir,num)
print('----------------------------------------')
print("数据扩充完成")