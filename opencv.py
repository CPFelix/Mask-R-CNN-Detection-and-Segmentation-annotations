# coding=utf-8
from PIL import Image
from PIL import ImageEnhance
import os

dir = 'F:/mango_new/all/dataArg/images/'

#删除无关文件
my_file = dir + 'desktop.ini'
if os.path.exists(my_file):
    os.remove(my_file)

filelist = []
filenames = os.listdir(dir)  # 返回指定目录下的所有文件和目录名
for fn in filenames:
    fullfilename = os.path.join(dir, fn)  # os.path.join--拼接路径
    filelist.append(fullfilename)  # filelist里存储每个图片的路径
for i in range(0, len(filelist)):
    img = filelist[i]  # 获取当前图片的路径
    # image = cv2.imread(img)  #读取图片
    # rows, cols = image.shape[:2]
    # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 270, 1)  # 旋转
    # dst = cv2.warpAffine(image, M, (cols, rows))
    # cv2.imshow("img", dst)
    image = Image.open(img)

    # 亮度减弱
    enh_bri = ImageEnhance.Brightness(image)
    brightness = 0.8
    image_brightened = enh_bri.enhance(brightness)
    image_brightened.save(dir + filenames[i][:-4] + '_brightL.jpg')
    # 亮度增强
    enh_bri = ImageEnhance.Brightness(image)
    brightness = 1.5
    image_brightened = enh_bri.enhance(brightness)
    image_brightened.save(dir + filenames[i][:-4] + '_brightH.jpg')

    # 色度减弱
    enh_col = ImageEnhance.Color(image)
    color = 0.8
    image_colored = enh_col.enhance(color)
    # image_colored.show()
    image_colored.save(dir + filenames[i][:-4] + '_colorL.jpg')
    # 色度增强
    enh_col = ImageEnhance.Color(image)
    color = 1.2
    image_colored = enh_col.enhance(color)
    # image_colored.show()
    image_colored.save(dir + filenames[i][:-4] + '_colorH.jpg')

    # 对比度增强
    enh_con = ImageEnhance.Contrast(image)
    contrast = 1.5
    image_contrasted = enh_con.enhance(contrast)
    # image_contrasted.show()
    image_contrasted.save(dir + filenames[i][:-4] + '_contrast.jpg')

    # 对比度增强
    enh_con = ImageEnhance.Contrast(image)
    contrast = 1.8
    image_contrasted = enh_con.enhance(contrast)
    # image_contrasted.show()
    image_contrasted.save(dir  + filenames[i][:-4] + '_contrastH.jpg')

    # 锐度增强
    enh_sha = ImageEnhance.Sharpness(image)
    sharpness = 2.0
    image_sharped = enh_sha.enhance(sharpness)
    # image_sharped.show()
    image_sharped.save(dir  + filenames[i][:-4] + '_sharp.jpg')
    # 锐度增强
    enh_sha = ImageEnhance.Sharpness(image)
    sharpness = 3.0
    image_sharped = enh_sha.enhance(sharpness)
    # image_sharped.show()
    image_sharped.save(dir + filenames[i][:-4] + '_sharpH.jpg')

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


