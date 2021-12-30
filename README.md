# 基于归一化平方误差匹配(NMRS)的昨日重现
成员及分工
* 王瑞鑫 （PB18061328）
    - coding design
* 陈扬 （PB18071532）
    - debug readme-writing  
## 问题描述
* 众所周知，土卫六aka.泰坦星，是一个风景秀美、人杰地灵的风水宝地。  
[![fg.jpg](https://i.postimg.cc/2ymfC63z/fg.jpg)](https://postimg.cc/jw81XRz9)  
然而有限的自然资源资源终究无法满足无限的贪婪和欲望。如今的泰坦星，早已变得，满目疮痍。  
[![bg.jpg](https://i.postimg.cc/7YYp9j2Q/bg.jpg)](https://postimg.cc/0rFW2WZp)  
现在，就让我们借助发达的技(xiàn)术(shí)手(bǎo)段(shí)来回顾这个帝国昔日的荣光吧！  
* 我们希望调用[pygame]([pygame](https://www.pygame.org/))，通过获取鼠标的位置，融合并匹配同一场景的不同时间（现实状态）。

 
## 原理分析
市面上比较常见的图像拼接手段都是基于SIFT等方法进行特征提取然后再做配准，最初我们采取的也是这个方法，起先得到了还算看得过去的结果。然而好景不长，在一次测试中出现了……非常离谱的结果。复盘原因发现是由于SIFT提取的特征对尺度缩放和旋转都能保持不变性的优良性质，而后的配准也是基于这个性质对匹配好的特征点为基准进行拼接，这就导致了在拼接过程中可能会对图片施以相应的变换。而在我们的例子中这种变换明显是多余的，所以我们就把目光转移到了不做尺度变换而是仅仅关注图片的位置匹配的算法。最终我们选择了通过计算平方误差来配准。  
#### NMRS算法原理简介：
* 模板匹配的是一种非常实用的方法。Opencv中集成了一个模板匹配算法，用户调用cv2.matchtemplate函数就可以实现该功能。该接口只能匹配到与目标一样大小的区域，即适用的条件为：被匹配对象与模板一样大，且不旋转。所以它的应用场景，需要外部控制待测物，使得拍摄到的图片，前后大小不变，且不旋转，就适合直接应用该接口。其中“归一化相关系数匹配法”效果相对更好。
* 评估图像的归一化均方误差 (NMRS) 作为滤波过程中去噪有效性和图像结构/细节保留的度量。 NMSE 表示过滤后的图像与真实图像的相似程度（在这种情况下，NMSE = 0）。


## 代码实现
代码实现主要分为两部分，一部分是画图，把前景图和背景图显示在屏幕上，并能根据鼠标位置动态调整。  
```python
pygame.init()
screen = pygame.display.set_mode((1252,934)) #1252, 934是图片的尺寸
pygame.display.set_caption('hello world')
bg_img = pygame.image.load("bg.jpg").convert()
fg_img = pygame.image.load("fg.jpg").convert_alpha()
bg = cv2.imread("bg.jpg")
fg = cv2.imread("fg.jpg")
screen.blit(bg_img, (0, 0)) 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            
            x, y = event.pos
            if x < 200: x = 200
            if y < 200: y = 200
            if x > 1251 - 200: x = 1251 - 200
            if y > 934 - 200: y = 934 - 200
            target = bg[:]
            template = fg[y-200:y+200, x-200:x+200]
```  
另一部分则是匹配，即找出当前鼠标选中区域在另一张图中对应的范围。
```python
            result = cv2.matchTemplate(target , template, cv2.TM_SQDIFF_NORMED,-1)
            cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            screen.blit(bg_img, (0, 0)) 
            screen.blit(fg_img, (x-200, y-200), pygame.Rect(min_loc[0], min_loc[1], 400, 400))
    
            pygame.display.flip()

```
## 效果展示
如下所示：
* GIF：由于gif分辨率过高，分成两个文件上传：[demo1.gif](https://postimg.cc/G8tdLbvj) 、 [demo2.gif](https://postimg.cc/1fGhZ8LQ)
* MP4：[/result/recording_demo.mp4](https://github.com/USTC-Computer-Vision-2021/project-cv34/blob/main/recording_demo.mp4)
## 工程结构  
    ├─code
    │   └─main.py
    ├─images
    │   ├─bg.jpg(before image)
    │   └─fg.jpg(after image)
    └─result   
       └─output.gif(实例中截取为两个gif-demo1.gif、demo2.gif)   
## 运行说明
* version  
    python3.9.7  
    pygame2.1.2  
    opencv4.5.3  
* install  
    conda config --add channels conda-forge  
    conda install pygame  
    conda install opencv  
    python cv.py  ##运行
