import pygame
from pygame.sprite import Sprite
from random import randint
from pngdebug import get_resource_path

class Star(Sprite):
    """出现星星的类"""
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.star_scale=randint(50,100)

        # 加载星星图像并取得其rect值
        self.image=pygame.image.load(get_resource_path('images\\STAR.png'))
        self.scaled_image=pygame.transform.scale(self.image,(self.star_scale,self.star_scale))
        self.image=self.scaled_image
        self.rect=self.image.get_rect()

        # 星星位置
        
