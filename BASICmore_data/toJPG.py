import cv2 as cv
import os
 
data = ('smallimage')#输入放置图片的文件夹，当前文件夹下 新建个文件夹，放入即可这里写文件夹的名字
daddir = './'
 
old_path = daddir + data + '\\'
new_path = 'newimage'#新文件夹用来存储转换之后的图片的   当前文件夹下 新建个文件夹，放入即可这里写文件夹的名字
if not os.path.exists(new_path):
    os.mkdir(new_path)
print('开始转换' )
print('转换后的文件存入 ' + new_path + '文件夹中')
 
path_list = os.listdir(old_path)
path_list.sort()
for filename in path_list:
    portion = os.path.splitext(filename)
    src = cv.imread(old_path + filename)
    cv.imwrite(new_path + '\\' + portion[0] + '.jpg', src)
 
print('转换完毕，文件已经存入 ' + new_path + ' 中')