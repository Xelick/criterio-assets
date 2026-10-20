# criterio-assets

Las imágenes y vídeos que sirve `alojadordemisimagenes12123134.netlify.app`.

**Los archivos sueltos de la raíz no se editan a mano.** Son una *salida*: los
escribe `publicar_assets.py` copiando lo que generan los build. Para cambiar una
pieza se edita su generador en `002_IA_COURSE/CURSO_AI_OPERATOR/conceptos/` y se
vuelve a publicar. La excepción es [`clientes/`](#clientes), que sí se escribe a
mano.

```bash
cd "G:/My Drive/002_IA_COURSE/CURSO_AI_OPERATOR/conceptos"
uv run publicar_assets.py --listar    # qué cambiaría
uv run publicar_assets.py             # sincroniza y hace push
```

Netlify despliega solo en cada push a `main`.

## Qué hay en la raíz

Todo plano, ordenado por prefijo. Cada serie sale de una carpeta de export:

| Prefijo | Qué es | Sale de | Cuántos |
|---|---|---|---|
| `C01`–`C30` `-NN.jpg` | Carruseles de conceptos | `conceptos/export_operator` | 150 |
| `CN08`–`CN11` `-NN.jpg` | Conceptos, estilo nuevo | `conceptos/export_operator_c2` | 24 |
| `H01`–`H30` `-gancho/-cN/-cierre.jpg` | Historias de conceptos | `conceptos/export_historias` | 150 |
| `P01`–`P10` `-NN.jpg` | Carruseles de preguntas | `conceptos/export_operator_preg` | 50 |
| `Q01`–`Q10` `-gancho/-cN/-cierre.jpg` | Historias de preguntas | `conceptos/export_historias_preg` | 50 |
| `dia01`–`dia30`, `extra*.jpg` | Campaña de 30 días | `campana/export_ig` | 36 |
| `BOT-*`, `SES-*.jpg` | Piezas con mascota | `conceptos/export_operator_bot` | 15 |
| `V*-NN.jpg` | Carruseles sin humo | `conceptos/export_operator_verdad` | 7 |
| `KM*-NN.jpg` | Kit de marca paso a paso | `conceptos/export_operator_kit` | 10 |
| `promo-*` (mp4 + portada) | Videos promocionales de Criterio | a mano | — |
| `noticia-*` (mp4 + portada) | Reels de noticias (Opus 5.5) | a mano | — |
| `cocokiki-*` (mp4 + portada) | Reels de la cuenta Coco & Kiki | a mano | — |

`publicar_assets.py` borra de la raíz los `.jpg` que ya no genera, pero **nunca**
toca `.mp4`, `promo-*` ni `noticia-*`. Una portada `cocokiki-*-portada.jpg` no
está protegida por nombre: si se sube a mano, conviene renombrarla `promo-…` o
añadir `cocokiki-` a la lista de protegidos del script.

## Por qué está plano

Las colas de publicación piden `<sitio>/C01-01.jpg`, sin carpetas. Si algún día
se anidan, hay que cambiar `HOST` y las colas a la vez. Por eso las series de
arriba **no** se mueven a carpetas, aunque sean muchas.

## clientes/

Material de clientes que se escribe a mano. `publicar_assets.py` solo mira los
archivos sueltos de la raíz, así que las subcarpetas no las toca.

| Carpeta | Qué es |
|---|---|
| [`clientes/el-eden-de-las-carnes/`](clientes/el-eden-de-las-carnes/) | 10 agentes de Claude Code para la carnicería, adaptados de agency-agents |

**Ojo:** el repo es público y se sirve en la web. A `clientes/` no va nada
privado del cliente (IDs de hojas, webhooks, claves, datos de sus clientes,
cifras).

## Por qué vive en F: y no en Google Drive

Drive sincroniza los archivos internos de `.git` a media operación y corrompe el
repo. Mismo motivo que los proyectos de Unity y los reels.
