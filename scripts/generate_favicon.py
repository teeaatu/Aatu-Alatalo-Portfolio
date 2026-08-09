import os
from PIL import Image, ImageDraw

def create_favicon():
    size = 512
    # Create a transparent background image
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded rectangle (white background)
    # macOS/iOS standard icon rounding is roughly 22.5% of the size
    radius = int(size * 0.225)
    
    # Python PIL rounded rectangle logic
    draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=radius,
        fill="#ffffff"
    )

    # Draw black circle in the middle
    # To leave a nice margin, let's make the circle diameter about 64% of the box
    circle_d = int(size * 0.64)
    offset = (size - circle_d) // 2
    draw.ellipse(
        [(offset, offset), (offset + circle_d, offset + circle_d)],
        fill="#111111"
    )

    # Save PNGs for various needs
    img.save("assets/images/favicon-192x192.png", format="PNG", optimize=True)
    img.save("assets/images/favicon-512x512.png", format="PNG", optimize=True)
    
    # Save standard favicon.ico (multi-size)
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    img.save("favicon.ico", format="ICO", sizes=icon_sizes)

    print("Favicons generated successfully!")

if __name__ == '__main__':
    create_favicon()
