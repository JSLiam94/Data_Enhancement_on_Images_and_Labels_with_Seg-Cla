import os

# 定义文件夹路径
folders = [
    'assets',
    'BASICmore_data/labels',
    'BASICmore_data/moreimage',
    'BASICmore_data/morelabels',
    'BASICmore_data/smallimage',
    'Mosicdata',
    'mydata/dataSet',
    'mydata/labels',
    'utils',
    'VOCdevkit/VOC2007/Annotations',
    'VOCdevkit/VOC2007/JPEGImages',
    'VOCdevkit/VOC2007/labels',
    'VOCdevkit_out/VOC2007/Annotations',
    'VOCdevkit_out/VOC2007/JPEGImages',
    'VOCdevkit_out/VOC2007/labels'
]

# 遍历文件夹列表，创建每个文件夹
for folder in folders:
    # 检查文件夹是否存在
    if not os.path.exists(folder):
        # 如果文件夹不存在，则创建它
        os.makedirs(folder)
        print(f"文件夹 '{folder}' 已创建。")
    else:
        print(f"文件夹 '{folder}' 已存在，无需创建。")