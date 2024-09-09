# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import getcwd

sets = ['train', 'val', 'test']
classes = ["Good", "Broken", "Flashover"]  # 改成自己的类别
abs_path = os.getcwd()
print(abs_path)

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h

def convert_annotation(image_id, out_file_path):
    in_file = open('VOCdevkit_out/VOC2007/Annotations/%s.xml' % (image_id), encoding='UTF-8')
    out_file = open('mydata/labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    has_valid_annotation = False
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if int(difficult) == 1:
            continue
        has_valid_annotation = True
        #cls_id = classes.index(cls) 此为使用字典来确定id，现修改为直接读取之前写入xml的id
        cls_id = cls
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()
for image_set in sets:
    if not os.path.exists('mydata/labels/'):
        os.makedirs('mydata/labels/')
    image_ids = open('mydata/dataSet/%s.txt' % (image_set)).read().strip().split()
    for image_id in image_ids:
        image_path = abs_path + '/VOCdevkit_out/VOC2007/JEPGImages/%s.jpg' % (image_id)
        list_file_path = 'Mosicdata/%s.txt' % (image_set)
        with open(list_file_path, 'a') as list_file:
            list_file.write(image_path + '\n')
        xml_file_path = 'VOCdevkit_out/VOC2007/Annotations/%s.xml' % (image_id)
        if os.path.exists(xml_file_path):
            with open(xml_file_path, 'r') as in_file:
                tree = ET.parse(in_file)
                root = tree.getroot()
                has_valid_objects = False
                for obj in root.iter('object'):
                    difficult = obj.find('difficult').text
                    cls = obj.find('name').text
                    if int(difficult) == 1:
                        continue
                    has_valid_objects = True
                    break
                if has_valid_objects:
                    convert_annotation(image_id, 'mydata/labels/%s.txt' % (image_id))
