import cv2, pygame, sys

pygame.init()
screen = pygame.display.set_mode((1252,934)) #1252, 934是图片的尺寸
pygame.display.set_caption('hello world')
bg_img = pygame.image.load("..\\images\\bg.jpg").convert()
fg_img = pygame.image.load("..\\images\\fg.jpg").convert_alpha()
bg = cv2.imread("..\\images\\bg.jpg")
fg = cv2.imread("..\\images\\fg.jpg")
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
            
            result = cv2.matchTemplate(target , template, cv2.TM_SQDIFF_NORMED,-1)
            cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            screen.blit(bg_img, (0, 0)) 
            screen.blit(fg_img, (x-200, y-200), pygame.Rect(min_loc[0], min_loc[1], 400, 400))
    
            pygame.display.flip()
