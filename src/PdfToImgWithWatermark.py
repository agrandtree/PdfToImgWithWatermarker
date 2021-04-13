import cv2
import numpy as np
import fitz
import os
from PIL import Image
import script

#必要库:PyMuPDF  cv2
#请设定 pdfpath,savepath,quality=20,zoomx=1 :: pdf路径,要保存图片的路径,保存图片的质量,图片的缩放
class PdfToWebp():
    def __init__(self,pdfpath,savepath,quality=100,zoom=1):
        self.paraweb=[cv2.IMWRITE_WEBP_QUALITY,quality]
        self.pdfdoc = fitz.open(pdfpath)
        self.zoom=zoom
        self.savepath=savepath

    #保存指定pdf页面,从0开始
    def saveOnePage(self,pg):
        if not os.path.exists(self.savepath):  # 判断存放图片的文件夹是否存在
            os.makedirs(self.savepath)  # 若图片文件夹不存在就创建
        page = self.pdfdoc[pg]
        rotate = int(0)
        zoom_x = zoom_y = self.zoom
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        pix = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pix = np.array(pix)
        pix = pix[:, :, ::-1].copy()
        cv2.imwrite(os.path.join(self.savepath, "{}.webp".format(pg)), pix, params=self.paraweb)
        return pix

    #获取一页pdf图片
    def getOnePage(self,pg):
        if not os.path.exists(self.savepath):  # 判断存放图片的文件夹是否存在
            os.makedirs(self.savepath)  # 若图片文件夹不存在就创建
        page = self.pdfdoc[pg]
        rotate = int(0)
        zoom_x = zoom_y = self.zoom
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        pix = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pix = np.array(pix)
        pix = pix[:, :, ::-1].copy()
        return pix

    #保存所有pdf页面到savepath
    def saveAllPage(self):
        if not os.path.exists(self.savepath):  # 判断存放图片的文件夹是否存在
            os.makedirs(self.savepath)  # 若图片文件夹不存在就创建
        for pg in range(self.pdfdoc.pageCount):
            page = self.pdfdoc[pg]
            rotate = int(0)
            zoom_x =zoom_y= self.zoom
            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pix = page.getPixmap(matrix=mat, alpha=False)
            pix = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            pix=np.array(pix)
            pix = pix[:, :, ::-1].copy()
            cv2.imwrite(os.path.join(self.savepath,"{}.webp".format(pg)), pix, params=self.paraweb)

    #以第一页的宽度为比例设置缩放系数, 缩放到指定的宽度, 一但设置width,那么原本初始化的zoom系数不再使用
    def setWidth(self,width):
        page = self.pdfdoc[0]
        oriwidth= page.getPixmap().width
        self.zoom=width/oriwidth

    def dctWaterMark(self,img,watermarkimg):
        DCTwriter = script.dctwm
        newim = DCTwriter.embed(img, watermarkimg)
        return newim

    def saveImg(self,img,name,quality):
        cv2.imwrite(os.path.join(self.savepath, "{}.webp".format(name)), img, params=[cv2.IMWRITE_WEBP_QUALITY,quality])

    def checkImgHasWartermark(self,img,watermarkimg):
        DCTwriter = script.dctwm
        sim = DCTwriter.extract(img, watermarkimg)
        print("打上水印的可能性为:",round(sim,2))

if __name__ == '__main__':
    #输入pdf转换为压缩后的webp图片到输出目录,图片的质量为100(质量更低的话占用空间更小),且要求图片尺寸是原尺寸的3倍
    cwd=os.getcwd()
    handle=PdfToWebp(os.path.join(cwd,"..","input","example.pdf"),os.path.join(cwd,"..","output"),20,3)
    #不考虑之前的缩放系数3, 而设置输出的图片宽一定是约为1000像素
    handle.setWidth(1000)
    #保存所有的pdf图片到路径
    handle.saveAllPage()
    #保存一张pdf图片到路径
    handle.saveOnePage(1)
    #获得水印图片
    watermarkimg=cv2.imread("../watermark/wm.jpg",cv2.IMREAD_GRAYSCALE)
    #给第一张pdf图片打dct盲水印
    pdfpage1=handle.getOnePage(0)
    im=handle.dctWaterMark(pdfpage1,watermarkimg)
    handle.saveImg(im,"0_watermark",quality=100)
    #查看刚才的图片是否打上水印
    ori=cv2.imread(os.path.join(cwd,"..","output","0_watermark.webp"))
    handle.checkImgHasWartermark(ori,watermarkimg)
