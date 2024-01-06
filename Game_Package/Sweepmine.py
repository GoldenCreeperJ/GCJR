import pygame
import sys
import random


# 未完善
class SweepmineStarting:
    def __init__(self, owner):
        # 开始页面
        self.owner = owner
        self.owner.write_name()
        self.font_list = [[self.owner.font45.render(self.owner.flag, True, 'white')],
                          [self.owner.font45.render('开始', True, 'white')]]
        for i in range(len(self.font_list)):
            j = self.font_list[i][0].get_rect()
            self.font_list[i].append(j)
        self.draw()

    def draw(self):
        # 绘制
        for i in range(len(self.font_list)):
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
        if self.owner.mine_num > self.owner.length * self.owner.width:
            self.owner.mine_num = int(
                self.owner.length * self.owner.width * 0.2) if self.owner.length * self.owner.width * 0.2 else 1
        self.owner.board_rect = (self.owner.length, self.owner.width)
        self.owner.grid_rect = tuple(map(lambda x: x * self.owner.depth, self.owner.board_rect))
        self.draw()


class SweepmineGaming:
    def __init__(self, owner):
        self.owner = owner
        self.owner.write_name()
        self.open_num = 0
        self.board = [['' for _ in range(self.owner.length)] for _ in range(self.owner.width)]
        self.icon_board = [[[] for _ in range(self.owner.length)] for _ in range(self.owner.width)]
        self.start_pos = tuple(
            map(lambda x, y: (x - y * self.owner.depth) // 2, self.owner.screen_rect, self.owner.board_rect))
        self.total_draw()

    def update_mine(self, pos):
        self.mine_list = []
        for i in range(self.owner.mine_num):
            while True:
                mine_pos = (random.randint(0, self.owner.length - 1), random.randint(0, self.owner.width - 1))
                if mine_pos not in self.mine_list and mine_pos != pos:
                    self.mine_list.append(mine_pos)
                    break

    def mine_test(self, pos):
        return pos in self.mine_list

    def unfold_function(self, pos):
        unfold_list = [pos]
        while unfold_list:
            unfold_item, count = unfold_list.pop(), 0
            if 0 <= unfold_item[0] < self.owner.length and 0 <= unfold_item[1] < self.owner.width and isinstance(
                    self.board[unfold_item[1]][unfold_item[0]], str):
                self.open_num += 1
                for i in range(unfold_item[0] - 1, unfold_item[0] + 2):
                    for j in range(unfold_item[1] - 1, unfold_item[1] + 2):
                        if self.mine_test((i, j)):
                            count += 1
                self.board[unfold_item[1]][unfold_item[0]] = count
                pygame.draw.rect(self.owner.screen, (150, 150, 150), (
                    self.start_pos[0] + unfold_item[0] * self.owner.depth,
                    self.start_pos[1] + unfold_item[1] * self.owner.depth,
                    self.owner.depth - 1,
                    self.owner.depth - 1))
                if count:
                    self.extend_icon(unfold_item[0], unfold_item[1], str(count))
                else:
                    for i in (-1, 0, 1):
                        for j in (-1, 0, 1):
                            if 0 <= unfold_item[0] + i < self.owner.length and 0 <= unfold_item[
                                1] + j < self.owner.width and isinstance(
                                    self.board[unfold_item[1] + j][unfold_item[0] + i], str):
                                unfold_list.append((unfold_item[0] + i, unfold_item[1] + j))

    def extend_icon(self, x, y, string):
        self.tem_icon = self.owner.num_font.render(string, True, 'black')
        self.icon_rect = self.tem_icon.get_rect()
        self.icon_rect.topleft = list(map(lambda x, y: x + y * self.owner.depth, self.start_pos, (x, y)))
        if not self.icon_board[y][x]:
            self.icon_board[y][x].extend((self.tem_icon, self.icon_rect))
        else:
            self.icon_board[y][x][0] = self.owner.num_font.render(string, True, 'black')
        self.owner.screen.blit(self.tem_icon, self.icon_rect)

    def total_draw(self):
        for i in range(self.owner.length):
            for j in range(self.owner.width):
                self.single_draw(i, j)

    def single_draw(self, x, y):
        pos = self.board[y][x]
        if isinstance(pos, str):
            pygame.draw.rect(self.owner.screen, (200, 200, 200), (
                self.start_pos[0] + x * self.owner.depth, self.start_pos[1] + y * self.owner.depth,
                self.owner.depth - 1,
                self.owner.depth - 1))
        elif isinstance(pos, int):
            pygame.draw.rect(self.owner.screen, (150, 150, 150), (
                self.start_pos[0] + x * self.owner.depth, self.start_pos[1] + y * self.owner.depth,
                self.owner.depth - 1,
                self.owner.depth - 1))
        if pos:
            self.icon_board[y][x][1].topleft = list(
                map(lambda x, y: x + y * self.owner.depth, self.start_pos, (x, y)))
            self.owner.screen.blit(self.icon_board[y][x][0], self.icon_board[y][x][1])

    def resize_function(self):
        self.start_pos = tuple(
            map(lambda x, y: (x - y * self.owner.depth) // 2, self.owner.screen_rect, self.owner.board_rect))
        self.total_draw()


class SweepmineSetting:
    # 设置页面
    def __init__(self, owner):
        self.owner = owner
        self.in_modify = 0
        self.font_list = [[self.owner.font45.render('深度', True, 'white')],
                          [self.owner.font45.render(str(self.owner.depth), True, 'white')],
                          [self.owner.font45.render('长度', True, 'white')],
                          [self.owner.font45.render(str(self.owner.length), True, 'white')],
                          [self.owner.font45.render('宽度', True, 'white')],
                          [self.owner.font45.render(str(self.owner.width), True, 'white')],
                          [self.owner.font45.render('雷数', True, 'white')],
                          [self.owner.font45.render(str(self.owner.mine_num), True, 'white')]]
        for i in range(len(self.font_list)):
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
            self.owner.max_rect = list(
                map(lambda x: x // self.owner.depth if x // self.owner.depth > 2 else 2, self.owner.screen_rect))
            if self.owner.max_rect[0] < self.owner.length:
                self.owner.length = self.owner.max_rect[0]
                self.font_list[3][0] = self.owner.font45.render(str(self.owner.length), True, 'white')
            if self.owner.max_rect[1] < self.owner.width:
                self.owner.width = self.owner.max_rect[1]
                self.font_list[5][0] = self.owner.font45.render(str(self.owner.width), True, 'white')
            if self.owner.mine_num > int(self.owner.length * self.owner.width * 0.2):
                self.owner.mine_num = int(self.owner.length * self.owner.width * 0.2) if int(
                    self.owner.length * self.owner.width * 0.2) > 0 else 1
                self.font_list[7][0] = self.owner.font45.render(str(self.owner.mine_num), True, 'white')

        elif self.in_modify == 3:
            if self.owner.letter and (1 < int(self.owner.letter) <= (self.owner.screen_rect[0] // self.owner.depth)
                                      or self.owner.width > 1 and 0 < int(self.owner.letter) <= (
                                              self.owner.screen_rect[0] // self.owner.depth)):
                self.owner.length = int(self.owner.letter)
            else:
                if self.owner.letter and int(self.owner.letter) > (self.owner.screen_rect[0] // self.owner.depth):
                    self.owner.length = self.owner.max_rect[0]
                self.font_list[3][0] = self.owner.font45.render(str(self.owner.length), True, 'white')
            self.owner.mine_num = int(self.owner.length * self.owner.width * 0.2) if int(
                self.owner.length * self.owner.width * 0.2) else 1
            self.font_list[7][0] = self.owner.font45.render(str(self.owner.mine_num), True, 'white')

        elif self.in_modify == 5:
            if self.owner.letter and (1 < int(self.owner.letter) <= (self.owner.screen_rect[1] // self.owner.depth)
                                      or self.owner.length > 1 and 0 < int(self.owner.letter) <= (
                                              self.owner.screen_rect[1] // self.owner.depth)):
                self.owner.width = int(self.owner.letter)
            else:
                if self.owner.letter and int(self.owner.letter) > (self.owner.screen_rect[1] // self.owner.depth):
                    self.owner.width = self.owner.max_rect[1]
                self.font_list[5][0] = self.owner.font45.render(str(self.owner.width), True, 'white')
            self.owner.mine_num = int(self.owner.length * self.owner.width * 0.2) if int(
                self.owner.length * self.owner.width * 0.2) else 1
            self.font_list[7][0] = self.owner.font45.render(str(self.owner.mine_num), True, 'white')

        elif self.in_modify == 7:
            if self.owner.letter and 0 < int(self.owner.letter) < self.owner.length * self.owner.width:
                self.owner.mine_num = int(self.owner.letter)
            else:
                self.owner.mine_num = int(self.owner.length * self.owner.width * 0.2) if int(
                    self.owner.length * self.owner.width * 0.2) else 1
                self.font_list[7][0] = self.owner.font45.render(str(self.owner.mine_num), True, 'white')

        self.draw()
        self.in_modify = 0
        self.owner.board_rect = (self.owner.length, self.owner.width)
        self.owner.grid_rect = tuple(map(lambda x: x * self.owner.depth, self.owner.board_rect))
        self.owner.num_font = pygame.font.SysFont(pygame.font.get_fonts()[27], self.owner.depth)

    def resize_function(self):
        # 适应页面大小
        if self.owner.depth > min(self.owner.screen_rect) // 2:
            self.owner.depth = min(self.owner.screen_rect) // 2
            self.owner.max_rect = tuple(
                map(lambda x: x // self.owner.depth if x // self.owner.depth > 2 else 2, self.owner.screen_rect))
        self.owner.length = self.owner.max_rect[0]
        self.owner.width = self.owner.max_rect[1]
        self.owner.mine_num = int(self.owner.length * self.owner.width * 0.2) if int(
            self.owner.length * self.owner.width * 0.2) else 1
        self.font_list[1][0] = self.owner.font45.render(str(self.owner.depth), True, 'white')
        self.font_list[3][0] = self.owner.font45.render(str(self.owner.length), True, 'white')
        self.font_list[5][0] = self.owner.font45.render(str(self.owner.width), True, 'white')
        self.font_list[7][0] = self.owner.font45.render(str(self.owner.mine_num), True, 'white')
        self.owner.board_rect = (self.owner.length, self.owner.width)
        self.owner.grid_rect = tuple(map(lambda x: x * self.owner.depth, self.owner.board_rect))
        self.owner.num_font = pygame.font.SysFont(pygame.font.get_fonts()[27], self.owner.depth)
        self.draw()


class SweepmineMain:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('扫雷')
        self.screen = pygame.display.set_mode((800, 600), flags=pygame.RESIZABLE)
        self.font15 = pygame.font.SysFont(pygame.font.get_fonts()[27], 15)
        self.font45 = pygame.font.SysFont(pygame.font.get_fonts()[27], 45)
        self.text_name = self.font15.render('made by J', True, 'white')
        self.name_rect = self.text_name.get_rect()
        self.clock = pygame.time.Clock()

        self.state_list = ('starting', 'gaming', 'setting')
        self.flag_list = ('', '成功', '失败')
        self.state = self.state_list[0]
        self.flag = self.flag_list[0]
        self.depth, self.length, self.width, self.mine_num = 20, 40, 30, 200
        self.max_rect = (self.length, self.width)
        self.board_rect = (self.length, self.width)  # 不合并，浅拷贝
        self.num_font = pygame.font.SysFont(pygame.font.get_fonts()[27], self.depth)

    def write_name(self):
        self.screen.fill('black')
        self.screen_rect = self.screen.get_rect()[2:]
        self.name_rect.bottomright = self.screen_rect
        self.screen.blit(self.text_name, self.name_rect)

    def loop(self):
        starting_page = SweepmineStarting(self)
        running = True
        while running:

            self.clock.tick(30)
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
                        gaming_page.resize_function()
                    elif self.state == self.state_list[2]:
                        setting_page.resize_function()

                if self.state == self.state_list[0]:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if pygame.Rect.collidepoint(starting_page.font_list[1][1], event.pos):
                            self.state = self.state_list[1]
                            gaming_page = SweepmineGaming(self)
                            del starting_page
                            break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = self.state_list[2]
                            setting_page = SweepmineSetting(self)
                            del starting_page

                elif self.state == self.state_list[1]:
                    if self.mine_num + gaming_page.open_num == self.length * self.width:
                        self.state = self.state_list[0]
                        self.flag = self.flag_list[1]
                        starting_page = SweepmineStarting(self)
                        del gaming_page
                    if event.type == pygame.MOUSEBUTTONUP:
                        click_rect = tuple(map(lambda x, y: (x - y) // self.depth, event.pos, gaming_page.start_pos))
                        self.x, self.y = click_rect
                        if 0 <= self.x < self.length and 0 <= self.y < self.width:
                            click_block = gaming_page.board[click_rect[1]][click_rect[0]]
                            if not gaming_page.open_num:
                                gaming_page.update_mine((self.x, self.y))
                            if event.button == 1:
                                if isinstance(click_block, str) and click_block != '!':
                                    if gaming_page.mine_test((self.x, self.y)):
                                        self.state = self.state_list[0]
                                        self.flag = self.flag_list[2]
                                        starting_page = SweepmineStarting(self)
                                        del gaming_page
                                    else:
                                        gaming_page.unfold_function((self.x, self.y))
                            elif event.button == 3:
                                if isinstance(click_block, str):
                                    if click_block == '!':
                                        gaming_page.board[click_rect[1]][click_rect[0]] = '?'
                                        gaming_page.extend_icon(self.x, self.y, '?')
                                    elif click_block == '?':
                                        gaming_page.board[click_rect[1]][click_rect[0]] = ''
                                        gaming_page.extend_icon(self.x, self.y, '')
                                    else:
                                        gaming_page.board[click_rect[1]][click_rect[0]] = '!'
                                        gaming_page.extend_icon(self.x, self.y, '!')
                                    gaming_page.single_draw(self.x, self.y)
                                elif isinstance(click_block, int) and click_block:
                                    num_list1 = []
                                    num_list2 = []
                                    for i in range(self.x - 1, self.x + 2):
                                        for j in range(self.y - 1, self.y + 2):
                                            if 0 <= i < self.length and 0 <= j < self.width:
                                                if gaming_page.board[j][i] == '!':
                                                    num_list1.append((i, j))
                                                elif isinstance(gaming_page.board[j][i], str):
                                                    num_list2.append([i, j])
                                    if len(num_list1) == click_block:
                                        for x, y in num_list2:
                                            if gaming_page.mine_test((x, y)):
                                                self.state = self.state_list[0]
                                                self.flag = self.flag_list[2]
                                                starting_page = SweepmineStarting(self)
                                                del gaming_page
                                                break
                                            else:
                                                gaming_page.unfold_function((x, y))
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = self.state_list[2]
                            self.flag = self.flag_list[0]
                            setting_page = SweepmineSetting(self)
                            del gaming_page
                elif self.state == self.state_list[2]:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if setting_page.in_modify != 0:
                            setting_page.return_function()
                        for i in range(1, len(setting_page.font_list), 2):
                            if pygame.Rect.collidepoint(setting_page.font_list[i][1], event.pos):
                                setting_page.in_modify = i
                                self.letter = ''
                                break

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
                            starting_page = SweepmineStarting(self)
                            del setting_page
            pygame.display.flip()


if __name__ == '__main__':
    sweepmine = SweepmineMain()
    sweepmine.loop()
    pygame.quit()
    sys.exit()
