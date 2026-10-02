# Prompts por tramo: John contra Dark-John

Cada tramo se genera con **Genjutsu** (`hf_mult_motion_control`, 720p). La referencia
de movimiento es el tramo correspondiente de `previz_limpio.mp4`, cortado con ffmpeg
en los mismos segundos. Los tramos empiezan y terminan en un corte del original, así que
al pegarlos en orden los cortes caen en su cuadro exacto.

Referencias fijas en Higgsfield (cuenta actual):

| Qué | media / job id |
|---|---|
| John con lentes (hoja de personaje) | `cb042bab-020b-4f06-a55f-5e294f959d36` · elemento `John-Lentes` |
| Dark-John (hoja) | `0f946678-85c7-474e-953a-d36d1d227396` · elemento `Dark-John` |
| Katana que se vuelve espada flamígera | job `f2d00d5d-c21a-4cc7-9044-9711005b037d` |
| Previz completo (30 s) | `eb1d6fa0-cec4-4aeb-943d-97b9d7fe3ed7` |
| Previz del desenvaine (14.68–18.40 s) | `35b336f1-5227-4826-8452-5cffd8410fb8` |

## Bloque fijo (va al inicio de cada prompt)

> The reference video is a 3D previz blockout: follow its exact camera motion, cuts,
> framing, blocking and timing, and turn it into a photoreal live-action scene. Keep every
> cut on the same frame as the reference; do not add transitions, fades or extra shots.
> The red mannequin is the man from image 1 (long wavy dark hair, round gold-frame
> sunglasses, crimson overcoat, dark red suit, small blue bow tie). The black mannequin
> with magenta and cyan rings is his evil shadow doppelganger from image 2: a black void
> silhouette with an iridescent violet, teal, magenta and gold rim light and two round
> lenses burning bright cyan and magenta. Setting: a real Japanese shrine courtyard by the
> sea at dusk, red torii gate, ritual circle painted on stone, light mist.
> Cinematic 35mm film look, photoreal, no grey blockout shapes remain.

Después del bloque fijo va la descripción del tramo:

## Tramos

**A · 0.00–3.64 s · planos 1–3**
> Shot 1 (0.8 s), static wide: the torii gate and the sea, the man small in the ritual
> circle. Hard cut. Shot 2 (1.2 s), medium close-up of the man looking left; the camera
> pulls back and pans. Hard cut. Shot 3 (1.6 s), close-up of his hand closing on the red
> silk-wrapped handle and gold guard of the sheathed katana at his left hip; fast push-in
> and tilt down.

**B · 3.64–7.24 s · planos 4–6**
> Shot 4 (1.6 s), close-up of the katana handle from the other side, slight Dutch roll
> while pushing in. Hard cut. Shot 5 (0.7 s), extreme close-up of his eyes behind the
> round sunglasses, static. Hard cut. Shot 6 (1.2 s), close-up of his hand gripping the
> handle, static, tension.

**C · 7.24–10.56 s · planos 7–10**
> Shot 7 (0.8 s), static wide of the torii and dark waves. Hard cut. Shot 8 (0.7 s),
> close-up of a single floating paper talisman card with a glowing orange eye sigil.
> Hard cut. Shot 9 (0.8 s), top-down view of the man in the center of the red and white
> ritual circle. Hard cut. Shot 10 (1.0 s), extreme close-up of his face, slight roll.

**D · 10.56–14.68 s · planos 11–12**
> Shot 11 (1.8 s), high wide of the courtyard, the camera tilts down toward the circle.
> Hard cut. Shot 12 (2.4 s), the man standing full body in the circle, the camera slowly
> pulls back.

**E · 14.68–18.40 s · planos 13–19 · desenvaine, la espada crece y aparece Dark-John**
> Shot 13 (0.6 s), fast whip pan along the blade as he draws the katana; halfway through,
> as the blade leaves the scabbard it transforms into the much larger black flame sword
> from image 3, with glowing red runes and a burst of bright crimson and gold sparks.
> Hard cut. Shot 14 (0.7 s), a wall of real floating paper talisman cards with glowing
> orange and blue eye sigils and a glowing violet orb whose tentacle crackles with bright
> cyan electricity; slow push-in. Hard cut. Shot 15 (0.6 s), the camera spins 70° while
> the evil doppelganger from image 2 materializes and grows to full size in front of the
> cards. Shot 16 (3 frames), white-hot flash of the red and white ritual rings seen from
> above. Shot 17 (0.4 s), the spin continues 50°. Hard cut. Shot 18 (0.4 s), medium shot
> of the man with the giant flame sword raised. Hard cut. Shot 19 (0.8 s), medium close-up
> of his face, slow roll.

**F · 18.40–21.72 s · planos 20–24**
> Shot 20 (0.7 s), a radial burst of bright magenta and orange energy rays around the
> doppelganger. Hard cut. Shot 21 (0.5 s), a glowing white, red and gold mandala sigil
> floating above him, centered. Hard cut. Shot 22 (0.7 s), wide side view: the man and his
> doppelganger facing each other across the ritual circles. Hard cut. Shot 23 (0.9 s),
> close-up of his arm swinging the flame sword, sparks. Hard cut. Shot 24 (0.6 s),
> close-up of his feet planted on the stone.

**G · 21.72–24.60 s · planos 25–27**
> Shot 25 (1.0 s), over the man's shoulder toward the doppelganger charging at him; a sudden
> crash zoom at the end. Hard cut. Shot 26 (1.2 s), close-up of the man's face with his hand
> thrust forward; the camera tilts up. Hard cut. Shot 27 (0.7 s), static medium shot of the
> man with the flame sword across the foreground.

**H · 24.60–30.00 s · planos 28–29**
> Shot 28 (2.3 s), the glowing violet orb with its electric tentacle, the man's hand reaching
> in from the edge of frame; the camera pans left. Hard cut. Shot 29 (3.1 s), final strike:
> the man swings the flame sword at the doppelganger, the camera whips right and pushes in,
> a burst of crimson sparks and cyan electricity.

## Transiciones

- Todos los cambios de plano son **cortes secos**, igual que en el original. Ningún prompt
  pide fundidos.
- El plano 16 son 3 cuadros de destello: funciona como transición dentro del giro.
- En el plano 13, el barrido rápido ya conecta el desenvaine con el plano 14.
- Para montar: concatena A → H sin transiciones. Si un tramo sale con otra duración,
  recórtalo a su duración exacta antes de pegarlo.
