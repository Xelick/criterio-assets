# Previz: pelea de John contra Dark-John

Previsualización en Blender que replica los planos y el movimiento de cámara de un
clip de referencia de 30 s (29 planos, 25 fps). Sirve de guía de movimiento para
Higgsfield. Esta carpeta vive en una rama de trabajo; no se publica en Netlify.

- `previz_limpio.mp4`: el video que se le pasa a Higgsfield como referencia, sin textos.
- `previz_mononoke_john.mp4`: el mismo video con el número de plano y el tiempo sobreimpresos.
- `previz_mononoke_john.blend`: la escena; cada plano tiene su cámara animada cuadro a cuadro.
- `kf.json`: el movimiento extraído de cada plano: `[plano, cuadro_ini, cuadro_fin, 5 × [paneo, inclinación, zoom, giro]]`
  en 0 / 25 / 50 / 75 / 100 % del plano. Paneo e inclinación van en fracciones de cuadro,
  el zoom es un factor de escala y el giro va en grados.
- `motion.py`: detecta los cortes y extrae ese movimiento del clip original con flujo óptico.
- `previz.py`: arma la escena y renderiza. Para regenerarla:

```bash
python previz.py kf.json out    # necesita el paquete bpy 4.5
```

Momentos clave: en el plano 13 (14.7 s) John desenvaina y la katana crece hasta
volverse la espada flamígera. En el plano 15 (16.0 s) la cámara gira y aparece
Dark-John.
