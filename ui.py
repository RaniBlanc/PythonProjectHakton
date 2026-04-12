import pygame
import threading
import time
from bot import ChatBot
from bidi.algorithm import get_display
import arabic_reshaper

pygame.init()

WIDTH, HEIGHT = 1000, 800
HEADER_HEIGHT = 70
INPUT_HEIGHT = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Safe Space")

font = pygame.font.Font("Arial.ttf", 20)
big_font = pygame.font.Font("Arial.ttf", 28)

bot = ChatBot()

input_text = ""
chat_history = []

bot_thinking = False
scroll_offset = 0

BG = (20, 20, 35)
HEADER = (30, 30, 60)
USER_COLOR = (0, 180, 120)
BOT_COLOR = (80, 140, 255)
TEXT_COLOR = (255, 255, 255)

def is_hebrew(text):
    return any('\u0590' <= c <= '\u05FF' for c in text)

def fix_text(text):
    if is_hebrew(text):
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text

def wrap_text(text, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        text_surface = font.render(fix_text(test_line), True, TEXT_COLOR)

        if text_surface.get_width() > max_width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line

    lines.append(current_line)
    return lines

def draw_header():
    pygame.draw.rect(screen, HEADER, (0, 0, WIDTH, HEADER_HEIGHT))

    title = big_font.render(fix_text("חבר שעוזר"), True, TEXT_COLOR)
    subtitle = font.render(fix_text("תמיד כאן בשבילך"), True, (180, 180, 180))

    screen.blit(title, (WIDTH//2 - title.get_width()//2, 5))
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 40))

def draw_chat():
    global scroll_offset

    chat_top = HEADER_HEIGHT + 10
    chat_bottom = HEIGHT - INPUT_HEIGHT - 10

    y = chat_top + scroll_offset

    for sender, message in chat_history:
        lines = wrap_text(message, 500)

        for line in lines:
            fixed = fix_text(line)
            text_surface = font.render(fixed, True, TEXT_COLOR)

            padding = 12
            box_width = text_surface.get_width() + padding*2
            box_height = 30

            if sender == "user":
                x = WIDTH - box_width - 20
                color = USER_COLOR
            else:
                x = 20
                color = BOT_COLOR


            if chat_top < y < chat_bottom:
                pygame.draw.rect(screen, color, (x, y, box_width, box_height), border_radius=15)
                screen.blit(text_surface, (x + padding, y + 5))

            y += 40

        y += 10

    scroll_offset = min(scroll_offset, 0)

def draw_input():
    pygame.draw.rect(screen, (25,25,45), (0, HEIGHT-INPUT_HEIGHT, WIDTH, INPUT_HEIGHT))

    input_surface = font.render(fix_text("> " + input_text), True, USER_COLOR)
    screen.blit(input_surface, (20, HEIGHT - 35))

def draw_thinking():
    if bot_thinking:
        text_surface = font.render(fix_text("חושב..."), True, (150,150,150))
        screen.blit(text_surface, (20, HEIGHT - 80))

def draw():
    screen.fill(BG)
    draw_header()
    draw_chat()
    draw_thinking()
    draw_input()
    pygame.display.flip()

def type_text_effect(text):
    displayed = ""
    for char in text:
        displayed += char
        chat_history[-1] = ("bot", displayed)
        time.sleep(0.015)

def get_bot_response(user_text):
    global bot_thinking, scroll_offset

    bot_thinking = True
    time.sleep(1)

    response = bot.get_response(user_text)

    chat_history.append(("bot", ""))
    bot_thinking = False

    type_text_effect(response)

    scroll_offset -= 40

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            scroll_offset += event.y * 20

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_text.strip():
                    chat_history.append(("user", input_text))
                    threading.Thread(target=get_bot_response, args=(input_text,)).start()
                    input_text = ""

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

            else:
                input_text += event.unicode

    draw()

pygame.quit()