from PIL import Image
import os.path
import glob
def convertjpg(jpgfile,outdir,width=1000,height=750):
    img=Image.open(jpgfile)
    width = img.size[0] / 4 * 3
    height = img.size[1] / 4 * 3
    try:
        new_img=img.resize((width,height),Image.BILINEAR)
        new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))
    except Exception as e:
        print(e)
for jpgfile in glob.glob("F:/mango_new/resize_N_N/*.jpg"):
    convertjpg(jpgfile,"F:/mango_new/resize_N_N_N")