"""Detecta planos y extrae el movimiento de cámara de cada uno.

Uso: python3 motion.py video.mp4 salida.json
Por cuadro: similaridad (dx, dy, rotación, escala) entre cuadros vecinos con
flujo óptico sobre puntos rastreables, más luminancia media y diferencia de
histograma para encontrar cortes, destellos y fundidos.
"""
import json, math, sys
import cv2
import numpy as np

src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
W0 = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H0 = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
W, H = 480, int(480 * H0 / W0)

frames = []
prev_g = prev_h = None
while True:
    ok, fr = cap.read()
    if not ok:
        break
    sm = cv2.resize(fr, (W, H), interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
    h = cv2.calcHist([hsv], [0, 1, 2], None, [16, 8, 8], [0, 180, 0, 256, 0, 256])
    cv2.normalize(h, h)
    rec = {"luma": float(g.mean()), "sat": float(hsv[..., 1].mean())}
    if prev_g is not None:
        rec["hdiff"] = float(cv2.compareHist(prev_h, h, cv2.HISTCMP_BHATTACHARYYA))
        rec["pdiff"] = float(np.abs(g.astype(np.int16) - prev_g).mean())
        pts = cv2.goodFeaturesToTrack(prev_g, 400, 0.01, 8)
        m = None
        if pts is not None and len(pts) >= 12:
            nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev_g, g, pts, None, winSize=(21, 21), maxLevel=3)
            a, b = pts[st == 1], nxt[st == 1]
            if len(a) >= 12:
                m, inl = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=2.0)
                if m is not None:
                    rec["inliers"] = float(inl.mean())
                    res = np.linalg.norm((a @ m[:, :2].T + m[:, 2]) - b, axis=1)
                    rec["resid"] = float(np.median(res))  # movimiento propio de la acción
        if m is not None:
            s = math.hypot(m[0, 0], m[1, 0])
            rec.update(dx=float(m[0, 2]) / W, dy=float(m[1, 2]) / H,
                       rot=math.degrees(math.atan2(m[1, 0], m[0, 0])), scale=s)
    frames.append(rec)
    prev_g, prev_h = g, h

# Cortes: salto de histograma que no es un destello (el destello vuelve).
n = len(frames)
cuts = [0]
for i in range(1, n):
    f = frames[i]
    hard = f["hdiff"] > 0.38 and f["pdiff"] > 18
    if hard and i - cuts[-1] >= 3:
        cuts.append(i)
shots = []
for k, a in enumerate(cuts):
    b = (cuts[k + 1] if k + 1 < len(cuts) else n) - 1
    seg = frames[a + 1:b + 1]
    dx = [f.get("dx", 0) for f in seg]
    dy = [f.get("dy", 0) for f in seg]
    rot = [f.get("rot", 0) for f in seg]
    sc = [f.get("scale", 1) for f in seg]
    lum = [frames[i]["luma"] for i in range(a, b + 1)]
    cum = lambda v: np.cumsum(v).round(4).tolist() if v else []
    shots.append({
        "shot": k + 1, "f_in": a, "f_out": b,
        "t_in": round(a / fps, 3), "t_out": round((b + 1) / fps, 3),
        "dur": round((b - a + 1) / fps, 3),
        "pan_x": round(float(sum(dx)), 4), "tilt_y": round(float(sum(dy)), 4),
        "roll_deg": round(float(sum(rot)), 2),
        "zoom": round(float(np.prod(sc)) if sc else 1.0, 4),
        "shake": round(float(np.std(np.diff(dx)) + np.std(np.diff(dy))) if len(dx) > 2 else 0, 5),
        "action": round(float(np.median([f.get("resid", 0) for f in seg])) if seg else 0, 3),
        "luma_in": round(lum[0], 1), "luma_out": round(lum[-1], 1),
        "luma_min": round(min(lum), 1), "luma_max": round(max(lum), 1),
        "curve_x": cum(dx), "curve_y": cum(dy),
        "curve_z": np.cumprod(sc).round(4).tolist() if sc else [],
        "curve_r": cum(rot),
    })
json.dump({"fps": fps, "w": W0, "h": H0, "n": n, "shots": shots,
           "frames": [{k: round(v, 4) for k, v in f.items()} for f in frames]},
          open(out, "w"))
for s in shots:
    print(f"S{s['shot']:02d} {s['t_in']:6.2f}-{s['t_out']:6.2f} ({s['dur']:4.2f}s) "
          f"pan {s['pan_x']:+.3f} tilt {s['tilt_y']:+.3f} zoom x{s['zoom']:.3f} "
          f"roll {s['roll_deg']:+.1f} shake {s['shake']:.4f} act {s['action']:.2f} "
          f"luma {s['luma_in']:.0f}->{s['luma_out']:.0f} [{s['luma_min']:.0f},{s['luma_max']:.0f}]")
