本模块主要功能是将pdf导出为压缩比较高的图片,也可对图片打上dct水印,并可根据水印和图片判断图片是否打上水印.


使用方法:
  #输入pdf转换为压缩后的webp图片到输出目录,图片的质量为100(质量更低的话更小),且要求图片尺寸是原尺寸的3倍
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
