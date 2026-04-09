import pygame
import threading
import time
from bot import ChatBot
from bidi.algorithm import get_display
import arabic_reshaper

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("💙 חבר")

font = pygame.font.Font("Arial.ttf", 22)

bot = ChatBot()

input_text = ""
chat_history = []

bot_thinking = False
scroll_offset = 0

BG = (18, 18, 18)
USER_COLOR = (0, 200, 100)
BOT_COLOR = (50, 150, 255)
TEXT_COLOR = (255, 255, 255)


def fix_hebrew(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def wrap_text(text, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        text_surface = font.render(fix_hebrew(test_line), True, TEXT_COLOR)

        if text_surface.get_width() > max_width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line

    lines.append(current_line)
    return lines

def draw():
    global scroll_offset

    screen.fill(BG)

    y = 20 + scroll_offset

    for sender, message in chat_history:
        lines = wrap_text(message, 500)

        for line in lines:
            fixed = fix_hebrew(line)
            text_surface = font.render(fixed, True, TEXT_COLOR)

            if sender == "user":
                x = WIDTH - text_surface.get_width() - 20
                pygame.draw.rect(screen, USER_COLOR, (x - 10, y - 5, text_surface.get_width() + 20, 30), border_radius=10)
            else:
                x = 20
                pygame.draw.rect(screen, BOT_COLOR, (x - 10, y - 5, text_surface.get_width() + 20, 30), border_radius=10)

            screen.blit(text_surface, (x, y))
            y += 35

        y += 10

    scroll_offset = min(scroll_offset, 0)

    if bot_thinking:
        thinking = fix_hebrew("חבר חושב...")
        text_surface = font.render(thinking, True, (150, 150, 150))
        screen.blit(text_surface, (20, HEIGHT - 80))

    input_surface = font.render(fix_hebrew("> " + input_text), True, USER_COLOR)
    screen.blit(input_surface, (20, HEIGHT - 40))

    pygame.display.flip()

def get_bot_response(user_text):
    global bot_thinking, scroll_offset

    bot_thinking = True
    time.sleep(1.2)

    response = bot.get_response(user_text)

    chat_history.append(("bot", response))

    bot_thinking = False
    scroll_offset -= 60

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