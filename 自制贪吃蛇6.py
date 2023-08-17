import pygame
import random
import os
import time

# 初始化pygame
pygame.init()

# 设置游戏窗口大小和标题
window_width = 640
window_height = 480
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# 设置游戏速度和蛇的初始位置
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

# 获取当前脚本所在的文件夹路径
current_dir = os.path.dirname(__file__)
font_path = os.path.join(current_dir, 'ZCOOLQingKeHuangYou-Regular.ttf')  # 使用中文字体文件名

# 加载中文字体
font_style = pygame.font.Font(font_path, 50)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    # 将消息显示在窗口中央
    text_rect = mesg.get_rect(center=(window_width / 2, window_height / 2))
    window.blit(mesg, text_rect)

def game_loop():
    game_over = False
    game_close = False
    game_win = False

    x1 = window_width / 2
    y1 = window_height / 2

    x1_change = 0
    y1_change = 0

    score = 0
    start_time = time.time()

    snake_length = 1
    snake_list = []

    # 随机生成食物的位置
    foodx = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            window.fill(black)
            message("你输了！按 Q-退出或 C-重新开始", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        window.fill(black)
        pygame.draw.rect(window, green, [foodx, foody, snake_block, snake_block])

        # 添加蛇的位置到列表中
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        # 当蛇的长度超过当前的分数时，移除蛇的最早位置，实现蛇的增长效果
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list:
            pygame.draw.rect(window, white, [segment[0], segment[1], snake_block, snake_block])

        # 更新并绘制计分板和计时器
        elapsed_time = int(time.time() - start_time)
        font = pygame.font.Font(font_path, 36)  # 使用中文字体
        time_text = font.render(f"时间: {elapsed_time}秒", True, white)
        score_text = font.render(f"得分: {score}", True, white)
        window.blit(time_text, (10, 10))
        window.blit(score_text, (10, 40))

        # 添加游戏胜利条件
        if score > 5 and not game_win:
            game_win = True
            window.fill(black)
            message("恭喜你获胜！", green)
            pygame.display.update()
            pygame.time.wait(3000)
            game_over = True

        pygame.display.update()

        # 检查是否碰到自己
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
            score += 1
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
