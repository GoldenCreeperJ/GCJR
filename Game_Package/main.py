from Snake import *
from Sweepmine import *


# TODO: 玩家数据持久化存储和显示
# TODO：适配局域网多人联机
class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('主菜单')
        self.screen = pygame.display.set_mode((800, 600), flags=pygame.RESIZABLE)
        self.font15 = pygame.font.SysFont(pygame.font.get_fonts()[27], 15)
        self.font45 = pygame.font.SysFont(pygame.font.get_fonts()[27], 45)
        self.text_name = self.font15.render('made by J', True, 'white')
        self.name_rect = self.text_name.get_rect()
        self.clock = pygame.time.Clock()

        self.write_name()
        self.font_list = [[self.font45.render('贪吃蛇', True, 'white')],
                          [self.font45.render('扫雷', True, 'white')]]
        for i in range(2):
            j = self.font_list[i][0].get_rect()
            self.font_list[i].append(j)
        self.draw()

    def draw(self):
        # 绘制
        for i in range(2):
            self.font_list[i][1].center = [int(self.screen_rect[0] * 0.5), int(self.screen_rect[1] * (0.3 + 0.2 * i))]
            self.screen.blit(self.font_list[i][0], self.font_list[i][1])

    def write_name(self):
        self.screen.fill('black')
        self.screen_rect = self.screen.get_rect()[2:]
        self.name_rect.bottomright = self.screen_rect
        self.screen.blit(self.text_name, self.name_rect)

    def loop(self):
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.VIDEORESIZE:
                    self.write_name()
                    self.draw()

                if event.type == pygame.MOUSEBUTTONUP:
                    if pygame.Rect.collidepoint(self.font_list[0][1], event.pos):
                        snake = SnakeMain()
                        snake.loop()
                    elif pygame.Rect.collidepoint(self.font_list[1][1], event.pos):
                        sweepmine = SweepmineMain()
                        sweepmine.loop()
                    self.write_name()
                    self.draw()
            pygame.display.flip()


if __name__ == '__main__':
    main = Main()
    main.loop()
