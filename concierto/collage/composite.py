"""Composite the collage layers over the final concert video and mux the song.

back_*.png  : chat bubbles that rise from behind the dancers; hidden wherever the frame
              shows the blue cloaks (blue key, only below y=440 so the sky never keys).
front_*.png : everything else, straight alpha.
Prints, every 6th frame, how much of the singer's box (red-coat track + head) the
graphics cover, so overlaps can be caught without looking at frames.
"""
import json, os, subprocess
import numpy as np
from PIL import Image, ImageFilter

W, H = 1920, 1080
probe = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                   'stream=r_frame_rate,nb_frames', '-of', 'json', 'v.mp4'],
                                  capture_output=True, text=True).stdout)['streams'][0]
print('master', probe)
rate = probe['r_frame_rate']


def layer(path):
    if not os.path.exists(path):
        return None
    a = np.asarray(Image.open(path).convert('RGBA'), dtype=np.float32)
    return a if a[..., 3].max() > 0 else None


dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', 'v.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                        '-r', rate, '-i', '-', '-i', 'v.mp4', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264',
                        '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                        '-c:a', 'copy', 'out.mp4'], stdin=subprocess.PIPE)
ramp = np.clip((np.arange(H, dtype=np.float32) - 440) / 40, 0, 1)[:, None]
report, f = [], 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    bg = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
    out, cover = bg.copy(), np.zeros((H, W), np.float32)
    back = layer(f'fr/back_{f:04d}.png')
    if back is not None:
        R, G, B = bg[..., 0], bg[..., 1], bg[..., 2]
        mx, mn = bg.max(-1), bg.min(-1)
        key = np.clip((B - np.maximum(R, G) - 15) / 25, 0, 1) * np.clip(((mx - mn) / (mx + 1) - 0.3) / 0.1, 0, 1) * ramp
        key = np.asarray(Image.fromarray((key * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5)),
                         dtype=np.float32) / 255
        a = back[..., 3] / 255 * (1 - key)
        out = out * (1 - a[..., None]) + back[..., :3] * a[..., None]
        cover = a
    front = layer(f'fr/front_{f:04d}.png')
    if front is not None:
        a = front[..., 3] / 255
        out = out * (1 - a[..., None]) + front[..., :3] * a[..., None]
        cover = 1 - (1 - cover) * (1 - a)
    if f % 6 == 0:
        s = bg[::4, ::4]
        red = (s[..., 0] > 50) & (s[..., 0] > 2.4 * s[..., 1]) & (s[..., 0] > 1.7 * s[..., 2])
        if red.sum() >= 15:
            ys, xs = np.nonzero(red)
            x0, x1 = np.percentile(xs, 3) * 4, np.percentile(xs, 97) * 4
            y0, y1 = np.percentile(ys, 3) * 4, np.percentile(ys, 97) * 4
            pad = 0.15 * (x1 - x0) + 10
            X0, X1 = int(max(0, x0 - pad)), int(min(W, x1 + pad))
            Y0, Y1 = int(max(0, y0 - max(60, 0.5 * (y1 - y0)))), int(min(H, y1))
            c = float((cover[Y0:Y1, X0:X1] > 0.6).mean())
            report.append(f'{f / 24:6.2f} singer=({X0},{Y0})-({X1},{Y1}) covered={c:.3f}' + ('  <<<' if c > 0.04 else ''))
    enc.stdin.write(out.clip(0, 255).astype(np.uint8).tobytes())
    f += 1
enc.stdin.close()
enc.wait()
print('frames', f)
print('\n'.join(report))
