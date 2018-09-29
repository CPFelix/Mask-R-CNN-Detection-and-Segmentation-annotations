# Mask-R-CNN-Detection-and-Segmentation-annotations
Mask R-CNN Detection and Segmentation annotations way

检测分割在一起标注，使用labelme软件。
Labelme在Windows下的安装
1) 打开Anaconda命令行工具
2) 执行 conda create --name=labelme python=3.6
3) 执行activate labelme
4) 执行 conda install pyyaml
5) 执行 pip install labelme
6) 执行 labelme 

安装完成后就可以进行标注。标注完会对应每个图片生成一个json文件，里面就是每张图的标注信息。

分好训练集和验证集，就可以分别生成最后所用的训练标注文件和测试标注文件。
使用写好的python代码将json文件转换成coco数据集格式的文件即可。

我将代码做了一些修改，诸如标注区域面积的计算、图片名的获得等。

原版大神代码传送门：
https://github.com/wucng/TensorExpand/blob/master/TensorExpand/Object%20detection/Data_interface/MSCOCO/labelme2COCO.py

