import os

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess
    import sys
    print("正在安装 Pillow 库...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont


def create_icon():
    icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
    os.makedirs(icons_dir, exist_ok=True)

    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        margin = max(1, size // 10)
        rect = [margin, margin, size - margin, size - margin]
        radius = size // 5
        draw.rounded_rectangle(rect, radius=radius, fill=(30, 100, 200, 255))

        inner_margin = size // 4
        inner_rect = [inner_margin, inner_margin + size // 8, size - inner_margin, size - inner_margin]
        draw.rounded_rectangle(inner_rect, radius=size // 10, fill=(255, 255, 255, 255))

        line_y_top = inner_margin + size // 4
        line_y_mid = inner_margin + size // 3
        line_y_bot = inner_margin + size // 2.2
        line_left = inner_margin + size // 10
        line_right = size - inner_margin - size // 10
        line_thickness = max(1, size // 20)

        draw.line([(line_left, line_y_top), (line_right, line_y_top)], fill=(100, 100, 100, 255), width=line_thickness)
        draw.line([(line_left, line_y_mid), (line_right, line_y_mid)], fill=(100, 100, 100, 255), width=line_thickness)
        draw.line([(line_left, line_y_bot), (line_right - size // 6, line_y_bot)], fill=(255, 180, 50, 255), width=line_thickness + 1)

        images.append(img)

    ico_path = os.path.join(icons_dir, "app.ico")
    images[0].save(ico_path, format="ICO", sizes=[(s, s) for s in sizes])
    print(f"图标已生成: {ico_path}")
    print(f"包含尺寸: {sizes}")


if __name__ == "__main__":
    create_icon()
