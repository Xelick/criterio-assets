# Video A v4: one-take en bloques, John contra seis monstruos (30 s)

Modelo: **Seedance 2.5**, `omni_reference`, 30 s, 21:9. Primero un borrador a 480p.
El video guía es `previz_onetake_v4_bloques_21x9.mp4`. Es la misma cámara del v3, pero con los
personajes como bloques rígidos de caja y esfera, sin espada, efectos ni utilería, siguiendo los
ejemplos de Higgsfield (ver `../GUIA_PREVIZ_BLOQUES.md`):

- La caja blanca es John y las cajas negras son los monstruos.
- El panel verde marca el frente de cada figura y el rojo la espalda.
- Los bloques solo se trasladan y giran. Toda la coreografía está escrita en el prompt.

Único cambio de cámara respecto al v3: el empuje de los 3.4–4.3 s termina en un plano medio y no
en el primer plano de la mano, porque con un bloque ese primer plano no mostraba nada.

Las imágenes van en este orden:

| Imagen | Qué es | ID |
|---|---|---|
| 1 | John | `cb042bab` |
| 2 | Línea de seis monstruos | job `8e49fb99` |
| 3 | Espada | job `f2d00d5d` |
| 4 | Locación | job `d8839ed2` |
| 5 | Cartas y esfera | job `4d630ce7` |

El prompt no nombra películas ni personas reales, para que no lo bloquee el filtro de propiedad
intelectual.

Borrador 1 (job `9f821264`): el movimiento ya salió fluido. Faltaba que los monstruos reaccionaran a
los cortes y soltaran algo; el primero no soltó nada. Por eso se agregó la sección HIT REACTIONS
AND ENERGY: en cada golpe sale luz y brasas en los colores de la paleta, en lugar de sangre. También
se detallaron los cortes del primer monstruo. Para el jefe final, cada corte le deja una marca de
luz que no se apaga y se acumula aunque él no pierda la postura; el último golpe es un corte
cargado que enciende todas las marcas a la vez y lo destruye desde dentro. En ese golpe (26 s) hay
un impact frame, como en el anime: unos 6 cuadros en blanco y negro puro, con 2 cuadros en
negativo, y luego vuelve al color cuando el jefe explota. El prompt no dice "anime" para que no
cambie el estilo del resto del video, que sigue siendo fotorrealista.

```text
Create a 30-second photoreal live-action fight film at night, ONE continuous take with no cuts.
John — crimson coat, round gold sunglasses — walks into a stone shrine courtyard by the sea, stops
and draws his katana; leaving the scabbard it becomes a giant black flame sword, and two walls of
floating paper talisman cards rise from the stone along the path to a vermilion torii and the sea.
Six shadow doubles of him form out of iridescent flakes and, writhing like insects in
metamorphosis, burst into SIX MONSTERS. They attack ONE AT A TIME, hand to hand, and he takes them
apart up close, pushing forward to the torii. Grounded stunt choreography, real weight, no blood.
NON-IP.

ACTIVE REFERENCES
video 1 = Previz — master reference for the camera path, lens, framing, timing, positions and
facing for all 30 seconds; follow its camera strictly. Its figures are a legend, not a look: the
WHITE box with a sphere on top = John; the BLACK boxes with a sphere on top = the six monsters
(they appear one by one at 4.8–6.6s, grow taller at 7.4s when they metamorphose, and each vanishes
the instant it is destroyed; the one standing on top of the arch is Monster 6). Every figure
carries the same facing code — a GREEN panel on the chest = that person's front, a RED panel = their
back — so read who faces whom at every second from the green and red. Green and red are this code
only: nothing in the film is green, and the red panel is not a costume colour. The figures are
rigid and only slide and turn because the previz carries positions, facing and camera, NOT
choreography — every body movement is written below; never reproduce their sliding, rigid,
turning-in-place motion. There is NO sword in the previz: the sword exists only in this text and
image 3. Legend for the set: grey floor = the wet stone courtyard; grey arch = the vermilion torii;
grey box with a pointed roof = the shrine hall; grey posts with a box on top = stone lanterns; the
two walls of light-grey tiles that rise from the ground at 4.6s = the floating talisman cards; the
dark flat plane beyond the arch = the sea. The greys and the flat grey sky are not visual targets.
Wherever this text and video 1 disagree about camera, positions or facing, video 1 wins; about how
bodies move, this text wins.
image 1 = John — face, long wavy dark hair, thin mustache, sparse chin beard, ROUND GOLD-FRAME
SUNGLASSES always on, dark red suit, white shirt, small royal blue bow tie, long crimson overcoat
worn open. Identity 100% consistent at every distance.
image 2 = the SIX MONSTERS, one species, left to right = Monster 1 to 6: 1 lean sprinter with long
thin limbs; 2 hunched with very long arms; 3 a spider-like crawler; 4 a brute with a swollen upper
body; 5 gaunt with moth-like wings half spread; 6 the biggest, extra thin arms, crown of tendrils.
All: cracked black obsidian-and-chitin skin, ridged spine, torn coat membrane, black hair-tendrils,
faceless elongated head with two round lenses burning white-hot cyan and magenta. Each keeps its
own design for the whole take; a head and a half taller than John (Monster 6 taller still).
image 3 = the sword — red silk handle, gold four-lobed guard, golden beast-mouth pommel, black
flame blade with hooked spikes and glowing red runes.
image 4 = the location — the shrine courtyard by the sea at night in dense haze. Its camera angle
and emptiness are not inherited.
image 5 = the floating paper talisman cards with orange and blue eye sigils and the violet plasma
orb hanging high above the right card wall. Look only.

STYLE
Live-action feature-film realism: physical performers, real skin and cloth, practical sparks and
sea mist, fine natural film grain, no animated look, no CGI gloss, no slow motion.

LIGHTING
Night. Hard light and high contrast from practical sources only: strong backlight through dense
fog, huge volumetric beams slicing the haze — cyan-blue from one side, magenta-pink from the other;
the card walls glow orange and blue in the haze; the violet orb pulses softly. Mostly dark frames
with crushed blacks, lit by flashes and glints instead of fill light.

COLOR
Palette — shadows #1E2B27 #172B3F #3B2C46 #4F3554 #284B5A #2E4C45; highlights #186E98 #3E9EB7
#5BA2B8 #7BB8AF #6B4569 #A86A8C #C4879F. The monsters are almost pure black shapes with thin
iridescent rim glints and sparks in their skin cracks; John's crimson coat and the sword's red
runes are the warmest accents in the frame. No green anywhere.

CAMERA
Strictly video 1 for all 30 seconds — one continuous take, no cuts, John always in frame:
0–4.3s a hard push-in from a frontal wide to a close medium shot on John as his hand reaches the
hilt, with a slight Dutch tilt; 4.3s a whip with the draw, then a low angle tilting up as the cards
rise; 7.3–15.3s one long, level orbit around him while he fights, in readable medium-wide framing;
15.3–16.2s a burst of sharp punch-in zooms on the combination; 16.2–17s a still hold; 17–18s a slow
push; 18–21.6s a slow push behind him toward the torii; 21.6–26s a chase behind him, tilting up to
the monster; 26–30s a slow pull-back as he walks away. Ultra-wide to wide lenses, low angles. The
horizon stays level — only slight Dutch angles, never a roll. Natural 180-degree shutter: fast
cuts, kicks and the coat carry directional motion blur.

PHYSICS
Feet plant and carry weight on wet stone, with small splashes; knees and hips absorb every step and
landing; the crimson coat swings with cloth delay and settles a beat after he stops. The flame sword
is MUCH larger than a katana and has real mass: every cut starts in the hips, the blade drags
momentum through the follow-through and he recovers it into the next move. Monsters grip the
stone with their claws, skid when they stop and push off when they lunge.

HIT REACTIONS AND ENERGY
EVERY cut or blow that lands on a monster — Monster 1 included, from the very first cut — gets a
visible body reaction AND a release of light. The body jolts, recoils, staggers or folds around the
hit, claws flaring, head snapping back, feet scrabbling for balance. Where the blade passes, the
monster's inner energy spills out instead of blood: a slash of cyan, magenta and violet light
opens along the line of the cut and flares through the cracks of its black chitin, throwing a
spray of glowing embers and flecks of light in the palette (#3E9EB7 #5BA2B8 #7BB8AF #A86A8C
#C4879F with white-hot cores) that drift and fade within a few frames. Elbows, knees and kicks send
a pulse of light rippling through its cracks. Blocks on the blade throw crimson-gold sparks; the
flame sword leaves a brief crimson-gold trail. The bigger the hit, the bigger the burst. Each
monster's destruction is the biggest burst of its fight: light floods out of every crack and it
shatters into black and iridescent flakes and cyan-magenta light that fade within half a second —
no body left, no blood.
THE FINAL BOSS (Monster 6) is different: it is too strong to stagger, so it keeps its stance and
only flinches, but every cut still hurts it — each one leaves a glowing scar of cyan-magenta light
burned into its chitin that does NOT fade. The scars accumulate hit after hit, cracks spreading
from them and leaking light, so by 25s its body is laced with glowing scars and it is visibly
weakening. John's last strike is CHARGED: during his sidestep and full spin the flame sword
gathers power — the flame swells and burns brighter, crimson-gold light coiling up the blade —
and the final diagonal cut releases it all; at that instant every scar on the boss ignites at once,
the accumulated damage detonating together, and it bursts apart from the inside.
IMPACT FRAME (once in the film, at 26.0s): at the exact instant the charged cut lands, the picture
flips for about a quarter of a second (6 frames) into a stark impact frame — the live-action image
reduced to pure black and pure white, no greys and no colour: John and the boss as hard graphic
silhouettes, the blade's path and the eruption of light as pure white, with harsh radial streaks
bursting from the point of impact; in the middle of it, 2 frames flash as an inverted negative
(black and white swapped). Then it snaps straight back to full colour as the boss explodes into
light and flakes. Photoreal before and after; the impact frame is the only stylised moment.

CAST AND BLOCKING (0–30s)
Exactly one John and six monsters, never a seventh, no duplicates, no bystanders. None of the
monsters exists before 4.8s. All six stay IN FRONT of John, between him and the torii — nobody
behind his back; he advances, they give ground. They fight ONE AT A TIME, in order; the others prowl
a full gap ahead, facing him, never overlapping in frame. John is never hit; calm and economical.
The monsters are frenzied, twitchy and predatory.

THE SWORD AND THE GRIP
One single-edged Japanese sword. It is a katana in a black lacquered scabbard at John's LEFT hip,
edge up, handle forward, until 4.45s; as it leaves the scabbard at 4.6s it becomes the flame sword
of image 3, more than twice the katana's length, with a burst of crimson-gold sparks; at 27.6s the
flame dies and it shrinks back to the katana; at 28.0s he sheathes it. The draw: his right hand
crosses his body and closes on the handle, his left hand holds the scabbard mouth, his thumb
pushes the guard, and the blade slides out along the scabbard. His hands always wrap ONLY the long
red silk-wrapped handle, between the gold guard and the golden beast-mouth pommel; the blade
extends from the guard AWAY from him. His hand never touches the blade, never holds the sword above
the guard, never upside down. Exactly ONE sword exists at any moment — before the draw there is no
flame blade anywhere, not on his back, not over his shoulder.

FIGHT CHOREOGRAPHY (the spine of the film)
John fights like a trained swordsman in continuous flowing motion: footwork that carries his
weight into every cut, hips and shoulders turning before the blade, wind-up, impact,
follow-through and recovery chained straight into the next move. Exchanges are fast and connected,
never pose-to-pose: a block flows into a counter, a slip flows into a cut, each step lands where
the next attack begins. The monsters skitter, lunge, recoil and scramble, bodies twisting and
reacting to every hit. Two signature combos:
COMBO 1, AERIAL INTO GROUND CHAIN — John springs off the enemy's raised limb, meets it in the air
with a cutting slash while the camera follows him upward, lands in a low crouch and, with zero
pause, unleashes a rapid chain of low sweeping cuts that alternate direction, stepping forward with
each one, the blade leaving white-hot arcs, driving the enemy back.
COMBO 2, SPIN-KICK, DASH, RISING SLASH — a spinning back kick slams the enemy away; John instantly
dashes after it so fast the frame streaks with motion; a flurry of strikes too fast to follow, then
one final rising slash that throws the enemy high into the air.
No energy blasts, no projectiles — claws against blade, elbows, knees, kicks, sweeps, free-hand
checks. No stiff limbs, no sliding feet, no snapping between poses, no frozen holds.

ACTION TIMING
0–4.4s — John walks out past the shrine hall and the stone lanterns, coat swaying, and stops on the
open stone at 3.1s; his right hand closes on the hilt at 2.6s; his thumb pushes the guard (click
3.6s). End state 4.4s: standing square to the path, hand on the hilt, weight settled.
4.4–7.6s — the draw: the katana leaves the scabbard and becomes the flame sword (4.6s) with a burst
of sparks; the two card walls rise from the stone and lock into rows; 4.8–6.6s six void
silhouettes of John form from swirls of flakes, five on the path ahead, one crouched on top of the
torii; 6.6–7.4s each convulses, its outline cracks like a chrysalis, limbs stretch with new joints,
muscles swell, and it bursts into its monster form from image 2. End state 7.6s: John in guard,
sword raised, stepping forward; the six monsters facing him down the path.
7.6–12.2s — Monster 1 (the sprinter) rushes in alone: 8.7s high claw blocked on the blade, sparks;
9.3s low claw slipped; 9.5–10.6s John answers with the ground chain of COMBO 1 — four low sweeping
cuts, stepping forward with each — and EVERY cut lands: each one opens a glowing slash of
cyan-magenta light across its body and throws embers, and it staggers back a step with each hit;
11.7s it overcommits a lunge, John drops low and sweeps its leg, it slams onto its back at his feet
(12.0s), downward thrust, light erupts from the cut and it shatters at 12.2s in a burst of light and
flakes. End state: John rising from the thrust, the next monster already coming.
12.2–17s — the chain, John stepping forward each time, every hit answered with light: Monster 2
rushes, rising elbow into its gut sends a pulse of light through its cracks, it folds, flat cut, it
shatters at 13.0s. Monster 3 scuttles in, one clean diagonal cut, it shatters at 14.0s. Monster 4 (the brute): elbow 15.4s, knee to the ribs 15.6s, pommel to the jaw
15.8s, backhand cut 16.0s, it shatters. End state 17s: John in guard, breathing, sword low.
17–21s — Monster 5 presses with feints (17.8s, 18.6s), John slips each; 19.5s it commits — COMBO 2:
a spinning back kick at 19.6s slams it down the path, John dashes after it in a blur and his rising
slash throws it into the air, where it shatters at 20.1s. 20.5s Monster 6 leaps down from the torii
and LANDS CLEANLY ON ITS FEET in a crouch at 21.0s, upright a beat later. End state 21s: John and
Monster 6 facing each other down the path.
21–26s — the last duel with the final boss, the longest exchange: John closes at a run; 22.7s high
claw blocked, sparks; 23.0s low claw slipped; 23.3s its kick checked by John's forearm; 23.7s John's
cut lands across its chest — it holds its ground but a glowing scar stays burned into it and it
jumps back; 24.0s elbow — it barely flinches; 24.4s its wide sweep — COMBO 1: John springs up off its
raised arm, cuts across it in mid-air, lands in a crouch and chains three low sweeping cuts
(24.7–25.0s), each one adding a new glowing scar, light now leaking from cracks all over its body,
driving it back toward the torii; 25.1s desperate overhead lunge; 25.4s John sidesteps into a full
spin while the flame sword charges, the flame swelling and blazing brighter; 26.0s the CHARGED final
diagonal cut — IMPACT FRAME: 6 frames of stark black-and-white with a 2-frame negative flash — then
back to colour as every scar on the boss ignites at once and it explodes from the inside into the
biggest storm of light, flakes and cyan-magenta sparks of the film.
26–30s — John walks on through the drifting flakes toward the torii; 27.6s the flame dies and the
sword becomes the katana; 28.0s he sheathes it (click); he passes under the torii toward the dark
sea. End state 30s: his back to the camera under the torii, walking, coat moving in the wind.

AUDIO
Sea wind, deep rumble, cloth snaps, footfalls on wet stone, cracking chitin, claws on steel, heavy
impacts, an electric crackle and hiss of escaping energy on every cut that lands, crystalline
shimmer of flakes; no music, no dialogue. Accents: 3.6s click · 4.6s steel
ring into a flame roar · 6.6–7.4s chitin cracking · 8.7/10.2s clangs · 12.0s slam ·
12.2/13.0/14.0/16.0/20.1s shatters · 19.6s kick · 21.0s landing · 22.5–26s rapid trade ·
25.4–26.0s rising hum of the sword charging · 26.0s a split second of total silence on the
impact frame, then a thunderclap of an impact and the biggest shatter · 28.0s sheath click · 28.5–30s wind only.

HOLD FOR THE FULL TIMELINE
video 1 camera path, positions and facing 1:1, one continuous take, no cuts, John always in frame;
bodies move with fluid, weighty, connected choreography — never like the rigid previz boxes; no
green anywhere; six monsters from image 2, each its own variant, always in front of him, one at a
time; every hit on a monster gets a body reaction and a burst of palette-coloured light and embers,
from the first cut of Monster 1 on; the final boss keeps its stance but keeps the glowing scars of
every cut until the charged final cut ignites them all; at 26.0s one black-and-white impact frame
with a negative flash, then back to colour; six destructions at 12.2 / 13.0 / 14.0 /
16.0 / 20.1 / 26.0s; katana until 4.45s and from 27.6s, the much larger flame sword in between, always gripped by the handle; John never hit; image
1 identity with round gold sunglasses in every frame; no text, no watermarks.
```
