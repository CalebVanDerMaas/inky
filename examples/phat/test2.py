import os
from PIL import Image, ImageDraw
from inky.auto import auto

# Set up the display
inky_display = auto(ask_user=True, verbose=True)
inky_display.set_border(inky_display.WHITE)

# Create a new palette image
image = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
image.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

# Fill the image with white
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, inky_display.WIDTH, inky_display.HEIGHT), fill=0)  # 0 is white in this palette

# Load the font sprites
PATH = os.path.dirname(__file__)
micro_font_sprites = Image.open(os.path.join(PATH, "resources/microFontTemplate.png")).convert("1")

# Define the micro font character positions
microFontDict = {'a': (0, 0, 4, 4), 'b': (4, 0, 8, 4), 'c': (8, 0, 12, 4), 'd': (12, 0, 16, 4,), 'e':(16, 0, 20, 4), 'f': (20, 0, 24, 4), 'g': (24, 0, 28, 4), 'h': (28, 0, 32, 4), 'i': (32, 0, 36, 4), 'j': (36, 0, 40, 4), 'k': (40, 0, 44, 4), 'l': (44, 0, 48, 4), 'm': (48, 0, 52, 4), 'n':(52, 0, 56, 4), 'o':(56, 0, 60, 4), 'p': (60, 0, 64, 4), 'q': (64, 0, 68, 4), 'r': (68, 0, 72, 4), 's': (72, 0, 76, 4), 't': (76, 0, 80, 4), 'u': (80, 0, 84, 4), 'v': (84, 0, 88, 4), 'w': (88, 0, 92, 4), 'x':(92, 0, 96, 4), 'y': (96, 0, 100, 4), 'z':(100, 0, 104, 4), '.':(104, 4, 108, 8), ' ':(104, 0, 108, 4)}

def draw_text(input_string, start_pos):
    current_pos = start_pos
    for char in input_string.lower():
        if char in microFontDict:
            crop_region = microFontDict[char]
            char_image = micro_font_sprites.crop(crop_region)
            # Use the character image as a mask to paste black (1) onto the main image
            image.paste(1, current_pos, char_image)
        current_pos = (current_pos[0] + 4, current_pos[1])

outputString = "Test: The quick brown fox jumps over the lazy dog."
# Calculate the middle of the screen, adjusting for text length
start_x = (inky_display.WIDTH - len(outputString) * 4) // 2
start_y = inky_display.HEIGHT // 2
draw_text(outputString, (start_x, start_y))

# Draw debug information
draw.rectangle([0, 0, inky_display.WIDTH - 1, inky_display.HEIGHT - 1], outline=1)
draw.text((2, inky_display.HEIGHT - 10), f"Text start: {start_x},{start_y}", fill=1)

# Save the result image for debugging
image.save("debug_output.png", "PNG")

try:
    # Display the image
    inky_display.set_image(image)
    inky_display.show()
    print("Image sent to display successfully.")
except Exception as e:
    print(f"Error displaying image: {e}")

print(f"Text started at position: ({start_x}, {start_y})")
print("Debug image saved as 'debug_output.png'")