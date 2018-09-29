# -*- coding:utf-8 -*-
# !/usr/bin/env python
#同时标注轮廓和关键点
#同时根据segment中的点计算面积
import argparse
import json
import matplotlib.pyplot as plt
import skimage.io as io
import cv2
from labelme import utils
import numpy as np
import glob
import PIL.Image
import getArea1

class labelme2coco(object):
    def __init__(self,labelme_json=[],save_json_path=''):
        '''
        :param labelme_json: 所有labelme的json文件路径组成的列表
        :param save_json_path: json保存位置
        '''
        self.labelme_json=labelme_json
        self.save_json_path=save_json_path
        self.images=[]
        self.categories=[]
        self.annotations=[]
        # self.data_coco = {}
        self.label=[]
        self.annID=1
        self.height=0
        self.width=0

        self.save_json()

    def data_transfer(self):
        for num,json_file in enumerate(self.labelme_json):
            with open(json_file,'r') as fp:
                data = json.load(fp)  # 加载json文件
                self.images.append(self.image(data,num))
                for shapes in data['shapes']:
                    label=shapes['label'].split('_')
                    if label[0] != 'keypoints':   #把label是keypoints的标签不做处理
                        #label=['mango','objectIndex']
                        if label[0] not in self.label:
                            self.categories.append(self.categorie(label))
                            self.label.append(label[0])
                        points=shapes['points']
                        for point in points:
                            point[0] = point[0]
                            point[1] = point[1]
                        #self.annotations.append(self.annotation(points,label,num))
                        self.annID+=1
                    else:
                        f_points = shapes['points']
                        k_points = []
                        i = 0
                        for point in f_points:
                            point[0] = point[0]
                            point[1] = point[1]
                            point.append(2)
                            k_points.extend(point)
                            i = i + 1
                        #points = k_point
                        num_keypoints = i
                        #label = 'mango'
                        self.annotations.append(self.annotation(points, label, num,k_points,num_keypoints))




    def image(self,data,num):
        image={}
        img = utils.img_b64_to_array(data['imageData'])  # 解析原图片数据
        # img=io.imread(data['imagePath']) # 通过图片路径打开图片
        # img = cv2.imread(data['imagePath'], 0)
        height, width = img.shape[:2]
        img = None
        image['height']=height
        image['width'] = width
        image['id']=num+1
        image['file_name'] = data['imagePath'].split('\\')[-1]

        self.height=height
        self.width=width

        return image

    def categorie(self,label):
        categorie={}
        categorie['supercategory'] = label[0]
        categorie['id']=len(self.label)+1 # 0 默认为背景
        #print(len(self.label))
        categorie['name'] = label[0]
        categorie['keypoints'] = ['P1','P2','P3']
        categorie['skeleton'] = [[1,2],[2,3]]
        return categorie


    def annotation(self, points, label, num, k_points, num_keypoints):
            annotation = {}
        #if label[0] != 'keypoints':
            annotation['segmentation']=[list(np.asarray(points).flatten())]
            annotation['iscrowd'] = 0
            annotation['image_id'] = num+1
            # annotation['bbox'] = str(self.getbbox(points)) # 使用list保存json文件时报错（不知道为什么）
            # list(map(int,a[1:-1].split(','))) a=annotation['bbox'] 使用该方式转成list
            annotation['bbox'] = list(map(float,self.getbbox(points)))

            annotation['category_id'] = self.getcatid(label) + 2
            annotation['id'] = self.annID - 1
            #return annotation
        #else:
            annotation['keypoints'] = k_points
            annotation['num_keypoints'] = num_keypoints

            areaPoint = []
            for point in points:
                areaPoint.append(point)
            Apoints = list(areaPoint)
            annotation['area'] = getArea1.checkio(Apoints)
            return annotation


    def getcatid(self,label):
        for categorie in self.categories:
            if label[0]==categorie['name']:
                return categorie['id']
        return -1

    def getbbox(self,points):
        # img = np.zeros([self.height,self.width],np.uint8)
        # cv2.polylines(img, [np.asarray(points)], True, 1, lineType=cv2.LINE_AA)  # 画边界线
        # cv2.fillPoly(img, [np.asarray(points)], 1)  # 画多边形 内部像素值为1
        polygons = points
        mask = self.polygons_to_mask([self.height,self.width], polygons)
        return self.mask2box(mask)

    def mask2box(self, mask):
        '''从mask反算出其边框
        mask：[h,w]  0、1组成的图片
        1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
        '''
        # np.where(mask==1)
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]
        # 解析左上角行列号
        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        # 解析右下角行列号
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)

        # return [(left_top_r,left_top_c),(right_bottom_r,right_bottom_c)]
        # return [(left_top_c, left_top_r), (right_bottom_c, right_bottom_r)]
        # return [left_top_c, left_top_r, right_bottom_c, right_bottom_r]  # [x1,y1,x2,y2]
        return [left_top_c, left_top_r, right_bottom_c-left_top_c, right_bottom_r-left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式

    def polygons_to_mask(self,img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

    def data2coco(self):
        data_coco={}
        data_coco['images']=self.images
        data_coco['categories']=self.categories
        data_coco['annotations']=self.annotations
        return data_coco

    def save_json(self):
        self.data_transfer()
        self.data_coco = self.data2coco()
        # 保存json文件
        json.dump(self.data_coco, open(self.save_json_path, 'w'), indent=4)  # indent=4 更加美观显示

labelme_json=glob.glob('F:/mango_new/haiming/labeled/train/*.json')
# labelme_json=['./1.json']
save_json_path = 'F:/mango_new/haiming/labeled/mango_train.json'
labelme2coco(labelme_json,save_json_path)
