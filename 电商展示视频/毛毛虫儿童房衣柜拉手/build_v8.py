#!/usr/bin/env python3
import subprocess, os
os.chdir("/home/hatch/workspace/video/caterpillar_handle")

# New image order (different from previous versions) + benefit copy.
# Top sticker = benefit phrase, bottom text = expanded benefit sentence (echo).
# (name, image, move, bars, badge, sweep_width, frames)
SEGS = [
    ("v8s1", "corr_7535.jpg", ("zoom", "1+0.0004*on"),
     [("wbar_title.png", "H-130")], "xbdg_room.png", 660, 75),
    ("v8s2", "corr_7534.jpg", ("pan", "lr"),
     [("xbar_ceramic.png", "H-130")], "xbdg_ceramic.png", 674, 75),
    ("v8s3", "corr_7517.jpg", ("zoom", "1.03-0.0004*on"),
     [("xbar_matte.png", "H-130")], "xbdg_matte.png", 674, 75),
    ("v8s4", "corr_7535.jpg", ("zoom", "1.10+0.0004*on"),
     [("xbar_round.png", "H-130")], "xbdg_round.png", 674, 75),
    ("v8s5", "corr_7530.jpg", ("pan", "rl"),
     [("xbar_multi.png", "H-130")], "xbdg_multi.png", 674, 75),
    ("v8s6", "corr_7534.jpg", ("zoom", "1.10+0.0004*on"),
     [("xbar_install.png", "H-130")], "xbdg_install.png", 620, 75),
    ("v8s7", "corr_7530.jpg", ("zoom", "1.10+0.0004*on"),
     [("wbar_name_small.png", "H-260"), ("wbar_slogan.png", "H-130")], None, 640, 75),
]

def build_seg(name, img, move, bars, badge, sweep_w, frames):
    inputs = ["-loop", "1", "-i", img]
    for bar, _ in bars:
        inputs += ["-loop", "1", "-i", bar]
    idx = 1 + len(bars)
    badge_idx = None
    if badge:
        inputs += ["-loop", "1", "-i", badge]
        badge_idx = idx; idx += 1
    if move[0] == "zoom":
        base = (f"[0:v]scale=1440:2560:force_original_aspect_ratio=increase,crop=1440:2560,"
                f"zoompan=z={move[1]}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=720x1280:fps=30[base]")
    else:
        xexpr = "180+360*n/74" if move[1] == "lr" else "540-360*n/74"
        base = (f"[0:v]scale=1440:2160,crop=720:1280:x='{xexpr}':y=440[base]")
    fc = [base]
    cur = "base"
    for bi, (bar, y) in enumerate(bars):
        fc.append(f"[{1+bi}:v]format=yuva420p,fade=t=in:st=0:d=0.4:alpha=1[bar{bi}]")
        fc.append(f"[{cur}][bar{bi}]overlay=(W-w)/2:{y}[tmp{bi}]")
        cur = f"tmp{bi}"
    if badge_idx is not None:
        fc.append(f"[{badge_idx}:v]format=yuva420p[st]")
        fc.append(f"[{cur}][st]overlay=30:'if(lt(t,0.4),-110+350*t,30)'[tmpb]")
        cur = "tmpb"
    dur = frames / 30.0
    if sweep_w:
        fc.append(f"[{cur}]drawbox=x='(720-{sweep_w})/2':y=1262:w='{sweep_w}*t/{dur}':h=6:color=0xF27CA7@0.9:t=fill[v]")
    else:
        fc.append(f"[{cur}]null[v]")
    cmd = ["ffmpeg", "-y", "-v", "error"] + inputs + [
        "-filter_complex", ";".join(fc),
        "-map", "[v]", "-frames:v", str(frames),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", f"{name}.mp4"]
    print("building", name, flush=True)
    subprocess.run(cmd, check=True)
    print("built", name, flush=True)

for s in SEGS:
    build_seg(*s)

trans = ["fade", "slideleft", "fade", "slideup", "smoothleft", "fade"]
offs = [2.1, 4.2, 6.3, 8.4, 10.5, 12.6]
parts = []
cur = "0:v"
for i, (tr, off) in enumerate(zip(trans, offs)):
    nxt = f"x{i+1}" if i < len(trans) - 1 else "vout"
    parts.append(f"[{cur}][{i+1}:v]xfade=transition={tr}:duration=0.4:offset={off}[{nxt}]")
    cur = nxt
parts.append("[7:a][8:a]amix=inputs=2:duration=longest:normalize=0[aout]")
inputs = []
for s in SEGS:
    inputs += ["-i", f"{s[0]}.mp4"]
inputs += ["-i", "narration_v8.mp3", "-i", "music15.wav"]
cmd = ["ffmpeg", "-y", "-v", "error"] + inputs + [
    "-filter_complex", ";".join(parts),
    "-map", "[vout]", "-map", "[aout]",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
    "-t", "15.1", "-movflags", "+faststart",
    "毛毛虫儿童房衣柜拉手_15秒展示_v8.mp4"]
print("building final...", flush=True)
subprocess.run(cmd, check=True)
print("final built", flush=True)
subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "csv=p=0", "毛毛虫儿童房衣柜拉手_15秒展示_v8.mp4"], check=False)
for t in [1.2, 3.8, 6.2, 8.8, 11.2, 13.8]:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i",
                    "毛毛虫儿童房衣柜拉手_15秒展示_v8.mp4", "-frames:v", "1", "-q:v", "3",
                    f"v8check_{t}.jpg"], check=True)
print("BUILD_DONE")
