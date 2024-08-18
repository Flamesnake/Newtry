import sys
from time import sleep

import pygame
from settings import Settings
from game_stats import Gamestats
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from button import Button
from scoreboard import Scoreboard
from random import randint


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock=pygame.time.Clock()
        self.settings=Settings()
        self.screen=pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        #想要全屏显示启用以下代码
        # self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width=self.screen.get_rect().width
        # self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #创建一个用于统计游戏信息的实例
        self.stats=Gamestats(self)
        self.sb=Scoreboard(self)
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self.stars=pygame.sprite.Group()

        self._creat_fleet()
        self._initial_star()
        #游戏状态
        self.game_active=False
        #创建play按钮
        self.play_button=Button(self,"Play")
        
    def run_game(self):
        """开始游戏主循环"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """相应按键和鼠标事件"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    self._check_keydown_events(event)                   
                elif event.type==pygame.KEYUP:
                    self._check_keyup_events(event) 
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_pos=pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
    
    def _check_play_button(self,mouse_pos):
        """在玩家单击play按钮时开始新游戏"""
        button_clicked= self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            #重置游戏统计信息
            self.stats.reset_stats()
            self.game_active=True
            self.sb.prep_level()
            self.sb.prep_score()
            self.sb.prep_ships()

            #清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            #创建一个新的外星舰队
            self._creat_fleet()
            self.ship.center_ship()
            #隐藏光标
            pygame.mouse.set_visible(False)
    
    def _check_keydown_events(self,event):
         """响应按下"""
         if event.key==pygame.K_RIGHT:
            #向右移动飞船
            self.ship.moving_right=True
         elif event.key==pygame.K_LEFT:
            #向左移动飞船
            self.ship.moving_left=True
         elif event.key==pygame.K_SPACE:
             self._fire_bullet()
        

    def _check_keyup_events(self,event):
         """响应抬起"""
         if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
         elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False
    
    def _fire_bullet(self):
        """创建一颗子弹,并将其加入编组bullets"""
        if len(self.bullets)<self.settings.bullet_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """更新子弹位置并删除已经消失的子弹"""
        #更新子弹位置
        self.bullets.update()

        #删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collision()
        
    
    def _check_bullet_alien_collision(self):
        """检查是否有子弹击中了外星人"""
        # 如果是，就删除相应的子弹和外星人
        collisions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True)
        if collisions:
            self.stats.score+=self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #删除现有子弹并创建一个新外星编队
            self.bullets.empty()
            self._creat_fleet()
            self.settings.increase_speed()
            #提高等级
            self.stats.level+=1
            self.sb.prep_level()

    def _creat_fleet(self):
        """创建一个外星舰队"""
        #创建一个外星人,再不断添加，直到没有空间添加外星人为止
        #外星人间距为外星人宽度和高度
        alien=Alien(self)
        #self.aliens.add(alien)
        alien_width,alien_height=alien.rect.size

        current_x,current_y=alien_width,alien_height
        while current_y < (self.settings.screen_height-500):
            while current_x<(self.settings.screen_width-2*alien_width):
                self._creat_alien(current_x,current_y)
                current_x+=2*alien_width
            #添加完一行外星人后重置x
            current_x=alien_width
            current_y+=2*alien_height
    
    def _creat_alien(self,x_position,y_position):
        """创建一个外星人并将其加入外星编队"""
        new_alien=Alien(self)
        new_alien.x=x_position
        new_alien.y=y_position
        new_alien.rect.x=new_alien.x
        new_alien.rect.y=new_alien.y
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """更新外星舰队中所有外星人位置"""
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            # print("Ship Hit!")
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """在外星人达到边缘时采取某些措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1
    def _creat_star(self):
        """初始化星星"""
        new_star=Star(self)
        new_star.rect.x=randint(0,self.settings.screen_width)
        new_star.rect.y=randint(-50,self.settings.screen_height-50)
        self.stars.add(new_star)

    def _initial_star(self):
        """限制星星数量"""
        while len(self.stars.sprites())<=10:
            self._creat_star()

    def _ship_hit(self):
        """相应飞船与外星人碰撞"""
        if self.stats.ships_left>0:
            #将飞船生命值减一
            self.stats.ships_left-=1
            self.sb.prep_ships()
            # print(self.stats.ships_left)
            #清空外星人和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            #重置游戏
            self._creat_fleet()
            self.ship.center_ship()
            #暂停
            sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=self.settings.screen_height:
                self._ship_hit()
                break

    
    def _update_screen(self):
            """更新屏幕上图像并切换到新屏幕"""
         #每次循环时重绘屏幕
            self.screen.fill(self.settings.bg_color)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.stars.draw(self.screen)
            self.ship.blitme()
            self.aliens.draw(self.screen)
            self.sb.show_score()
            #如果游戏处于非活跃状态，就绘制Play按钮
            if not self.game_active:
                self.play_button.draw_button()
            #让最近绘制的屏幕可见
            pygame.display.flip()
         


if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai=AlienInvasion()
    ai.run_game()