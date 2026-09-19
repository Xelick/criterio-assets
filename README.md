# criterio-assets

Las imágenes y vídeos que sirve `alojadordemisimagenes12123134.netlify.app`.

**No se edita nada a mano aquí.** Este repo es una *salida*: lo escribe
`publicar_assets.py` copiando lo que generan los build. Para cambiar una pieza
se edita su generador en `002_IA_COURSE/CURSO_AI_OPERATOR/conceptos/` y se
vuelve a publicar.

```bash
cd "G:/My Drive/002_IA_COURSE/CURSO_AI_OPERATOR/conceptos"
uv run publicar_assets.py --listar    # qué cambiaría
uv run publicar_assets.py             # sincroniza y hace push
```

Netlify despliega solo en cada push a `main`.

## Por qué está plano

Las colas de publicación piden `<sitio>/C01-01.jpg`, sin carpetas. Si algún día
se anidan, hay que cambiar `HOST` y las colas a la vez.

## Por qué vive en F: y no en Google Drive

Drive sincroniza los archivos internos de `.git` a media operación y corrompe el
repo. Mismo motivo que los proyectos de Unity y los reels.
