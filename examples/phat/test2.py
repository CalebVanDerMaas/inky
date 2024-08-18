import os
from PIL import Image
from inky.auto import auto

# Set up the display
inky_display = auto(ask_user=True, verbose=True)
inky_display.set_border(inky_display.BLACK)

# Load the background template and font sprites
PATH = os.path.dirname(__file__)
background = Image.open(os.path.join(PATH, "resources/blankInky.png")).convert("RGB")
micro_font_sprites = Image.open(os.path.join(PATH, "resources/microFontTemplate.png"))

# Define the micro font character positions
microFontDict = {'a': (0, 0, 4, 4), 'b': (4, 0, 8, 4), 'c': (8, 0, 12, 4), 'd': (12, 0, 16, 4,), 'e':(16, 0, 20, 4), 'f': (20, 0, 24, 4), 'g': (24, 0, 28, 4), 'h': (28, 0, 32, 4), 'i': (32, 0, 36, 4), 'j': (36, 0, 40, 4), 'k': (40, 0, 44, 4), 'l': (44, 0, 48, 4), 'm': (48, 0, 52, 4), 'n':(52, 0, 56, 4), 'o':(56, 0, 60, 4), 'p': (60, 0, 64, 4), 'q': (64, 0, 68, 4), 'r': (68, 0, 72, 4), 's': (72, 0, 76, 4), 't': (76, 0, 80, 4), 'u': (80, 0, 84, 4), 'v': (84, 0, 88, 4), 'w': (88, 0, 92, 4), 'x':(92, 0, 96, 4), 'y': (96, 0, 100, 4), 'z':(100, 0, 104, 4), '.':(104, 4, 108, 8), ' ':(104, 0, 108, 4)}

def build_image(input_string, start_pos):
    for char in input_string.lower():
        if char in microFontDict:
            crop_region = microFontDict[char]
            char_image = micro_font_sprites.crop(crop_region)
            background.paste(char_image, start_pos, char_image)
        start_pos = (start_pos[0] + 4, start_pos[1])
    return background

outputString = "This is a test. The quick brown fox jumps over the lazy dog."
result_image = build_image(outputString, (0,0))

# Convert the image to the display's palette
inky_image = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
inky_image.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
inky_image.paste(result_image)

# Display the image
inky_display.set_image(inky_image)
inky_display.show()