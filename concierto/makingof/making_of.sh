#!/usr/bin/env bash
# Making of del Concierto de Criterio: mezcla el video final (A) con el previz de Blender (B).
# Uso: making_of.sh final.mp4 previz.mp4 salida.mp4   (necesita MartianMono.ttf en la carpeta actual)
set -euo pipefail
FINAL=$1; PREVIZ=$2; OUT=$3
F=MartianMono.ttf
BEAT=0.4651   # 129 BPM

# Qué se ve en cada momento (T en segundos):
#  0-3     solo Blender
#  3-8.4   cortina: Blender a la izquierda, el final entra desde la derecha
#  8.4-12.4  final
#  12.4-16.8 transparencia: los dos encima al 50 %
#  16.8-23.6 pantalla partida: Blender | final
#  23.6-28 final
#  28-31   parpadeo al ritmo: un beat Blender, un beat final
#  31-36   fundido de Blender a final
#  36-40   final
EXPR="if(lt(T,3),B,\
if(lt(T,8.4),if(lt(X,W*(1-(T-3)/5.4)),B,A),\
if(lt(T,12.4),A,\
if(lt(T,16.8),(A+B)/2,\
if(lt(T,23.6),if(lt(X,W/2),B,A),\
if(lt(T,28),A,\
if(lt(T,31),if(mod(floor((T-28)/$BEAT),2),A,B),\
if(lt(T,36),A*(T-31)/5+B*(1-(T-31)/5),A))))))))"

pill() { # texto x y inicio fin
  echo "drawtext=fontfile=$F:text='$1':fontsize=30:fontcolor=0xffda00:box=1:boxcolor=0x111118@0.92:boxborderw=18:x=$2:y=$3:enable='between(t,$4,$5)'"
}

FILTER="[1:v]scale=1920:1080,setsar=1,format=yuv420p[b];\
[0:v]setsar=1,format=yuv420p[a];\
color=c=0xffda00:s=6x1080:r=24:d=40[line];\
[a][b]blend=all_expr='$EXPR'[mix];\
[line]split[l1][l2];\
[mix][l1]overlay=x='1920*(1-(t-3)/5.4)-3':y=0:enable='between(t,3,8.4)'[m1];\
[m1][l2]overlay=x=957:y=0:enable='between(t,16.8,23.6)',\
$(pill 'BLENDER · PREVIZ' 60 60 0 8.4),\
$(pill 'VIDEO FINAL · IA' 'w-tw-60' 60 3 12.4),\
$(pill 'PREVIZ + FINAL' 60 60 12.4 16.8),\
$(pill 'BLENDER' 60 60 16.8 23.6),\
$(pill 'VIDEO FINAL' 'w-tw-60' 60 16.8 23.6),\
$(pill 'DE BLENDER A VIDEO FINAL' 60 60 31 36),\
$(pill 'MAKING OF · @criterio_ai' '(w-tw)/2' 'h-th-80' 36 40)[v]"

ffmpeg -y -v error -i "$FINAL" -i "$PREVIZ" -filter_complex "$FILTER" -map '[v]' -map 0:a \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
