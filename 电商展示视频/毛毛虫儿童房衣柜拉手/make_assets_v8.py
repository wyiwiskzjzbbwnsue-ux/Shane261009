#!/usr/bin/env python3
"""Generate v8 caption bars and benefit stickers for the caterpillar handle video.

Bars: black translucent rounded rectangles, white text.
Stickers: product pastel palette, dark gray text, capsule shape, width fits text.
Run in the directory where build_v8.py expects its PNG assets.
"""
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"


def bar(text, fontsize, fname):
    f = ImageFont.truetype(FONT, fontsize)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bbox = tmp.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    W, H = tw + 80, th + 50
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=26, fill=(0, 0, 0, 150))
    d.text(((W - tw) / 2 - bbox[0], (H - th) / 2 - bbox[1]), text, font=f, fill=(255, 255, 255, 255))
    img.save(fname)
    print(fname, "width:", W)


def badge(text, color, fname):
    f = ImageFont.truetype(FONT, 40)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bbox = tmp.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    W, H = tw + 80, 96
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=44, fill=color + (255,))
    d.text(((W - tw) / 2 - bbox[0], (H - th) / 2 - bbox[1]), text, font=f, fill=(58, 58, 58, 255))
    img.save(fname)
    print(fname, "width:", W)


# Bottom benefit sentences (54px) -> xbar_*.png used by build_v8.py
bar("陶瓷材质，孩子摸着舒服", 54, "xbar_ceramic.png")
bar("哑光质感，看着温馨舒服", 54, "xbar_matte.png")
bar("圆润造型，不怕宝宝磕碰", 54, "xbar_round.png")
bar("多色可选，怎么搭都好看", 54, "xbar_multi.png")
bar("安装方便，不用请师傅", 54, "xbar_install.png")
# Title / ending bars reused from v7 (regenerated here for completeness)
bar("毛毛虫儿童房衣柜拉手", 58, "wbar_title.png")
bar("给孩子的房间添点可爱", 56, "wbar_slogan.png")
bar("毛毛虫儿童房衣柜拉手", 44, "wbar_name_small.png")

# Top benefit stickers (40px, product pastels, dark text)
badge("孩子房换新装", (240, 175, 192), "xbdg_room.png")
badge("温润不冰手", (169, 198, 228), "xbdg_ceramic.png")
badge("柔光不刺眼", (156, 211, 190), "xbdg_matte.png")
badge("圆润不怕磕碰", (242, 212, 136), "xbdg_round.png")
badge("怎么搭都好看", (201, 190, 230), "xbdg_multi.png")
badge("自己就能装好", (242, 196, 168), "xbdg_install.png")
