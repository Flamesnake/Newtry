class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        """初始化游戏静态设置"""
        #屏幕设置
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(0,0,0)
        
        #子弹设置
        
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(160,160,160)
        self.bullet_allowed=10
        #外星人设置
        
        self.fleet_drop_speed=100
           
        # 飞船设置
        
        self.ship_limit=3
        #以什么速度加快游戏节奏
        self.speedup_scale=1.1
        #外星人分数的提高速度
        self.score_scale=1.5


        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置（在不初始化类的情况下初始化动态数据）"""
        self.ship_speed=3
        self.bullet_speed=30.0
        self.alien_speed=1.0
         #方向1向右，-1向左
        self.fleet_direction=1
        self.alien_points=50
    
    def increase_speed(self):
        """随着游戏进行加速"""
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        self.alien_points=int(self.score_scale*self.alien_points)