import pygame
from pygame.sprite import Sprite
from pngdebug import get_resource_path

class Alien(Sprite):
    """初始化单个外星人并设置其起始位置"""

    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        #加载外星人图像并设置其rect属性
        self.image=pygame.image.load(get_resource_path('images\\ALIEN(2).png'))
        
        #调整图像大小
        self.scaled_image=pygame.transform.scale(self.image,(50,36))
        self.image=self.scaled_image
        self.rect=self.image.get_rect()
        #每个外星人最初都在屏幕左上角附近
        self.rect.x=self.rect.width/4
        self.rect.y=self.rect.height/4

        #存储外星人精确水平位置
        self.x=float(self.rect.x)

    def update(self):
        """向右移动外星人"""
        self.x+=self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x=self.x
    
    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回Ture"""
        screen_rect=self.screen.get_rect()
        return (self.rect.right>=screen_rect.right) or (self.rect.left<=0)
    
