

功能: 将pdf页面导出为压缩比较高的webp格式图片, 并可对指定图片打上dct水印, 也可根据水印和图片判断图片是否打上水印。

依赖库: fitz

测试样例:

cwd=os.getcwd()

输入pdf路径, 输出目录,图片的质量, 图片尺寸缩放倍率来创建操作柄

handle=PdfToWebp(os.path.join(cwd,"..","input","example.pdf"),os.path.join(cwd,"..","output"),20,3)

设置输出的图片宽一定约为1000像素

handle.setWidth(1000)

保存所有的压缩后的pdf图片到路径

handle.saveAllPage()

保存指定某页pdf图片到路径

handle.saveOnePage(1)

获得水印图片

watermarkimg=cv2.imread("../watermark/wm.jpg",cv2.IMREAD_GRAYSCALE)

给第一张pdf图片打dct盲水印

pdfpage1=handle.getOnePage(0)

im=handle.dctWaterMark(pdfpage1,watermarkimg)

handle.saveImg(im,"0_watermark",quality=100)

查看刚才的图片是否打上水印

ori=cv2.imread(os.path.join(cwd,"..","output","0_watermark.webp"))

handle.checkImgHasWartermark(ori,watermarkimg)



