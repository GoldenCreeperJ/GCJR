import pygame
import sys
import random


class Snake_Starting:
    def __init__(self, owner):
        # 开始页面
        self.owner = owner
        self.owner.write_name()
        self.font_list = [[self.owner.font45.render(str(self.owner.score) + '分', True, 'white')],
                          [self.owner.font45.render('开始', True, 'white')]]
        if self.owner.score == self.owner.width * self.owner.length:
            self.font_list[0] = [self.owner.font45.render('满分', True, 'white')]
        for i in range(2):
            j = self.font_list[i][0].get_rect()
            self.font_list[i].append(j)
        self.draw()

    def draw(self):
        # 绘制
        for i in range(2):
            self.font_list[i][1].center = [int(self.owner.screen_rect[0] * 0.5),
                                           int(self.owner.screen_rect[1] * (0.3 + 0.2 * i))]
            self.owner.screen.blit(self.font_list[i][0], self.font_list[i][1])

    def resize_function(self):
        # 适应大小
        if self.owner.depth > min(self.owner.screen_rect) // 2:
            self.owner.depth = min(self.owner.screen_rect) // 2
            self.owner.max_rect = tuple(
                map(lambda x: x // self.owner.depth if x // self.owner.depth > 2 else 2, self.owner.screen_rect))
        if self.owner.screen_rect[0] // self.owner.depth < self.owner.length:
            self.owner.length = self.owner.max_rect[0]
        if self.owner.screen_rect[1] // self.owner.depth < self.owner.width:
            self.owner.width = self.owner.max_rect[1]
        self.owner.board_rect = (self.owner.length, self.owner.width)
        self.owner.grid_rect = tuple(map(lambda x: x * self.owner.depth, self.owner.board_rect))
        self.draw()


class Snake_Gaming:
    # 游戏页面
    def __init__(self, owner):
        self.owner = owner
        self.owner.write_name()
        self.owner.score = 0
        self.start_pos = tuple(
            map(lambda x, y: (x - y * self.owner.depth) // 2, self.owner.screen_rect, self.owner.board_rect))
        self.head_place = tuple(map(lambda x: x // 2, self.owner.board_rect))
        self.tail_place = self.head_place
        self.body_list = [self.head_place]
        self.vector = (1, 0)
        self.in_pause = False
        self.grow = False
        self.real_speed = self.owner.start_speed if self.owner.speed_change else self.owner.end_speed
        self.__update_apple()

    def __update_apple(self):
        # 生成苹果
        self.apple_place = (random.randint(0, self.owner.length - 1), random.randint(0, self.owner.width - 1))
        while self.apple_place in self.body_list:
            self.apple_place = (random.randint(0, self.owner.length - 1), random.randint(0, self.owner.width - 1))
        self.apple_pos = tuple(map(lambda x, y: x + y * self.owner.depth, self.start_pos, self.apple_place))

    def __update_snake(self):
        # 生成蛇
        self.head_place = tuple(map(lambda x, y: x + y, self.head_place, self.vector))
        self.body_list.append(self.head_place)
        if self.grow:
            self.grow = False
        else:
            self.tail_place = self.body_list.pop(0)
            self.tail_pos = tuple(map(lambda x, y: x + y * self.owner.depth, self.start_pos, self.tail_place))
        self.head_pos = tuple(map(lambda x, y: x + y * self.owner.depth, self.start_pos, self.head_place))

    def __eat_test(self):
        # 检测是否吃苹果
        if self.head_place == self.apple_place:
            self.grow = True
            self.__update_apple()
            self.owner.score += 1
            if self.owner.speed_change:
                self.real_speed = (self.owner.speed_rate * self.owner.start_speed) // (
                            self.owner.score + self.owner.speed_rate)

    def death_test(self):
        # 检测是否死亡
        return (self.head_place in self.body_list[:-1] and len(self.body_list) != 1) or (
            not 0 <= self.head_place[0] <= self.owner.length - 1) or (
            not 0 <= self.head_place[1] <= self.owner.width - 1)

    def moving_function(self, event):
        # 移动
        if event.key in (pygame.K_w, pygame.K_UP) and self.vector != (0, 1):
            self.vector = (0, -1)
        elif event.key in (pygame.K_s, pygame.K_DOWN) and self.vector != (0, -1):
            self.vector = (0, 1)
        elif event.key in (pygame.K_d, pygame.K_RIGHT) and self.vector != (-1, 0):
            self.vector = (1, 0)
        elif event.key in (pygame.K_a, pygame.K_LEFT) and self.vector != (1, 0):
            self.vector = (-1, 0)

    def replace_function(self):
        # 适应大小
        self.start_pos = tuple(
            map(lambda x, y: (x - y * self.owner.depth) // 2, self.owner.screen_rect, self.owner.board_rect))
        self.apple_pos = tuple(map(lambda x, y: x + y * self.owner.depth, self.start_pos, self.apple_place))
        pygame.draw.rect(self.owner.screen, 'white', self.start_pos + self.owner.grid_rect, width=1)
        pygame.draw.rect(self.owner.screen, 'red', self.apple_pos + (self.owner.depth, self.owner.depth))
        for i in self.body_list:
            self.body_pos = tuple(map(lambda x, y: x + y * self.owner.depth, self.start_pos, i))
            pygame.draw.rect(self.owner.screen, 'green', self.body_pos + (self.owner.depth, self.owner.depth))

    def draw(self):
        # 绘制
        self.__eat_test()
        self.__update_snake()
        pygame.draw.rect(self.owner.screen, 'white', self.start_pos + self.owner.grid_rect, width=1)
        pygame.draw.rect(self.owner.screen, 'red', self.apple_pos + (self.owner.depth, self.owner.depth))
        pygame.draw.rect(self.owner.screen, 'black', self.tail_pos + (self.owner.depth, self.owner.depth))
        pygame.draw.rect(self.owner.screen, 'green', self.head_pos + (self.owner.depth, self.owner.depth))
        pygame.time.wait(self.real_speed)


class Snake_Setting:
    # 设置页面
    def __init__(self, owner):
        self.owner = owner
        self.in_modify = -1
        self.font_list = [[self.owner.font45.render('深度', True, 'white')],
                          [self.owner.font45.render(str(self.owner.depth), True, 'white')],
                          [self.owner.font45.render('长度', True, 'white')],
                          [self.owner.font45.render(str(self.owner.length), True, 'white')],
                          [self.owner.font45.render('宽度', True, 'white')],
                          [self.owner.font45.render(str(self.owner.width), True, 'white')],
                          [self.owner.font45.render('变速', True, 'white')],
                          [self.owner.font45.render(str(self.owner.speed_change), True, 'white')],
                          [self.owner.font45.render('最快', True, 'white')],
                          [self.owner.font45.render(str(self.owner.end_speed), True, 'white')],
                          [self.owner.font45.render('加速', True, 'white')],
                          [self.owner.font45.render(str(self.owner.speed_rate), True, 'white')],
                          [self.owner.font45.render('初始', True, 'white')],
                          [self.owner.font45.render(str(self.owner.start_speed), True, 'white')], ]
        for i in range(14):
            j = self.font_list[i][0].get_rect()
            j.topleft = [20 + 100 * (i % 2), 25 + 50 * (i // 2)]
            self.font_list[i].append(j)
        self.draw()

    def draw(self):
        # 绘制
        self.owner.write_name()
        for i in self.font_list:
            self.owner.screen.blit(i[0], i[1])

    def return_function(self):
        # 返回键功能
        if self.in_modify == 1:
            if self.owner.letter and 0 < int(self.owner.letter) <= min(self.owner.screen_rect) // 2:
                self.owner.depth = int(self.owner.letter)
            else:
                if self.owner.letter and int(self.owner.letter) > min(self.owner.screen_rect) // 2:
                    self.owner.depth = min(self.owner.screen_rect) // 2
                self.font_list[1][0] = self.owner.font45.render(str(self.owner.depth), True, 'white')
            self.owner.max_rect = tuple(
                map(lambda x: x // self.owner.depth if x // self.owner.depth > 2 else 2, self.owner.screen_rect))
            if self.owner.max_rect[0] < self.owner.length:
                self.owner.length = self.owner.max_rect[0]
                self.font_list[3][0] = self.owner.font45.render(str(self.owner.length), True, 'white')
            if self.owner.max_rect[1] < self.owner.width:
                self.owner.width = self.owner.max_rect[1]
                self.font_list[5][0] = self.owner.font45.render(str(self.owner.width), True, 'white')

        elif self.in_modify == 3:
            if self.owner.letter and (1 < int(self.owner.letter) <= (self.owner.screen_rect[0] // self.owner.depth)
                                      or self.owner.width > 1 and 0 < int(self.owner.letter) <= (
                                              self.owner.screen_rect[0] // self.owner.depth)):
                self.owner.length = int(self.owner.letter)
            else:
                if self.owner.letter and int(self.owner.letter) > (self.owner.screen_rect[0] // self.owner.depth):
                    self.owner.length = self.owner.max_rect[0]
                self.font_list[3][0] = self.owner.font45.render(str(self.owner.length), True, 'white')

        elif self.in_modify == 5:
            if self.owner.letter and (1 < int(self.owner.letter) <= (self.owner.screen_rect[1] // self.owner.depth)
                                      or self.owner.length > 1 and 0 < int(self.owner.letter) <= (
                                              self.owner.screen_rect[1] // self.owner.depth)):
                self.owner.width = int(self.owner.letter)
            else:
                if self.owner.letter and int(self.owner.letter) > (self.owner.screen_rect[1] // self.owner.depth):
                    self.owner.width = self.owner.max_rect[1]
                self.font_list[5][0] = self.owner.font45.render(str(self.owner.width), True, 'white')

        elif self.in_modify == 9:
            pass
        elif self.in_modify == 11:
            pass
        elif self.in_modify == 13:
            pass

        self.draw()
        self.in_modify = -1
        self.owner.board_rect = (self.owner.length, self.owner.width)
        self.owner.grid_rect = tuple(map(lambda x: x * self.owner.depth, self.owner.board_rect))

    def resize_function(self):
        # 适应页面大小
        if self.owner.depth > min(self.owner.screen_rect) // 2:
            self.owner.depth = min(self.owner.screen_rect) // 2
            self.owner.max_rect = tuple(
                map(lambda x: x // self.owner.depth if x // self.owner.depth > 2 else 2, self.owner.screen_rect))
        self.owner.length = self.owner.max_rect[0]
        self.owner.width = self.owner.max_rect[1]
        self.font_list[1][0] = self.owner.font45.render(str(self.owner.depth), True, 'white')
        self.font_list[3][0] = self.owner.font45.render(str(self.owner.length), True, 'white')
        self.font_list[5][0] = self.owner.font45.render(str(self.owner.width), True, 'white')
        self.owner.board_rect = (self.owner.length, self.owner.width)
        self.owner.grid_rect = tuple(map(lambda x: x * self.owner.depth, self.owner.board_rect))
        self.draw()


class Snake_Main:
    def __init__(self, screen=pygame.display.set_mode((800, 600), flags=pygame.RESIZABLE)):
        # 初始化
        pygame.init()
        pygame.display.set_caption('贪吃蛇')
        self.screen = screen
        self.font15 = pygame.font.SysFont(pygame.font.get_fonts()[27], 15)
        self.font45 = pygame.font.SysFont(pygame.font.get_fonts()[27], 45)
        self.font75 = pygame.font.SysFont(pygame.font.get_fonts()[27], 75)
        self.text_name = self.font15.render('made by J', True, 'white')
        self.name_rect = self.text_name.get_rect()
        self.clock = pygame.time.Clock()

        self.state_list = ('starting', 'gaming', 'setting')
        self.state = self.state_list[0]
        self.depth, self.length, self.width, self.score = 20, 40, 30, 0
        self.start_speed, self.end_speed, self.speed_rate, self.speed_change = 100, 30, 10, True
        self.max_rect = (self.length, self.width)
        self.board_rect = (self.length, self.width)  # 不合并，浅拷贝
        self.grid_rect = tuple(map(lambda x: x * self.depth, self.board_rect))

    def write_name(self):
        # 更新页面大小
        self.screen.fill('black')
        self.screen_rect = self.screen.get_rect()[2:]
        self.name_rect.bottomright = self.screen_rect
        self.screen.blit(self.text_name, self.name_rect)

    def loop(self):
        # 主循环
        starting_page = Snake_Starting(self)
        running = True
        while running:

            self.clock.tick(self.end_speed)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.write_name()
                    self.max_rect = tuple(
                        map(lambda x: x // self.depth if x // self.depth > 2 else 2, self.screen_rect))
                    if self.state == self.state_list[0]:
                        starting_page.resize_function()
                    elif self.state == self.state_list[1]:
                        gaming_page.replace_function()
                    elif self.state == self.state_list[2]:
                        setting_page.resize_function()

                if self.state == self.state_list[0]:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if pygame.Rect.collidepoint(starting_page.font_list[1][1], event.pos):
                            self.state = self.state_list[1]
                            gaming_page = Snake_Gaming(self)
                            del starting_page
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = self.state_list[2]
                            setting_page = Snake_Setting(self)
                            del starting_page

                elif self.state == self.state_list[1]:
                    if event.type == pygame.KEYDOWN:
                        if not gaming_page.in_pause:
                            gaming_page.moving_function(event)
                        if event.key == pygame.K_ESCAPE:
                            self.state = self.state_list[2]
                            setting_page = Snake_Setting(self)
                            del gaming_page
                        elif event.key == pygame.K_SPACE:
                            gaming_page.in_pause = not gaming_page.in_pause
                        break

                elif self.state == self.state_list[2]:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if setting_page.in_modify != -1:
                            setting_page.return_function()
                        for i in range(1, len(setting_page.font_list), 2):
                            if pygame.Rect.collidepoint(setting_page.font_list[i][1], event.pos):
                                setting_page.in_modify = i
                                self.letter = ''
                                break
                        if setting_page.in_modify == 7:
                            self.speed_change = not self.speed_change
                            setting_page.in_modify = -1

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            setting_page.return_function()
                        elif event.key == pygame.K_BACKSPACE:
                            self.letter = self.letter[:-1]
                            setting_page.font_list[setting_page.in_modify][0] = self.font45.render(self.letter, True,
                                                                                                   'white')
                            setting_page.draw()
                        elif setting_page.in_modify and '0' <= event.unicode <= '9':
                            self.letter += event.unicode
                            setting_page.font_list[setting_page.in_modify][0] = self.font45.render(self.letter, True,
                                                                                                   'white')
                            setting_page.draw()
                        elif event.key == pygame.K_ESCAPE:
                            setting_page.return_function()
                            self.state = self.state_list[0]
                            starting_page = Snake_Starting(self)
                            del setting_page
            if self.state == self.state_list[1] and not gaming_page.in_pause:
                gaming_page.draw()
                if gaming_page.death_test():
                    self.state = self.state_list[0]
                    starting_page = Snake_Starting(self)
                    starting_page.resize_function()
                    del gaming_page
            pygame.display.flip()


if __name__ == '__main__':
    snake = Snake_Main()
    snake.loop()
    pygame.quit()
    sys.exit()