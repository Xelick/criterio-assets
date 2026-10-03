# Guía: previz en bloques para Seedance

Reglas sacadas del blog de Higgsfield "GPT Astra 6 + Blender + Higgsfield Builds The Craziest
Cinematic Scenes" (@adilinthewildtempo, 12 sep 2026), más lo que aprendimos con los borradores
de John.

## Qué lleva el previz

- **Solo formas básicas grises.** Cada personaje es una figura de caja y esfera. El escenario
  también es de bloques grises. El previz fija la cámara, el tiempo y dónde está cada personaje,
  nada más.
- **Sin props.** Nada de espada, chispas, auras, anillos, olas ni orbes. Todo eso va escrito en el
  prompt y en las imágenes de referencia. Cuando el previz tenía props y maniquíes articulados,
  Seedance copiaba sus movimientos tiesos y los errores del agarre de la espada.
- **Los bloques solo se trasladan y giran.** No se animan brazos ni piernas, y no se inclina el
  cuerpo. En el ejemplo del concierto, los 66 bailarines son cajas quietas y el baile está escrito
  entero en el prompt: "the boxes only mark positions and facing; the actual choreography lives in
  the generation prompt so the dancers move fluidly instead of copying the stiff blocking".
- **Código de orientación.** Un panel verde marca el frente y uno rojo la espalda. Así se lee quién
  mira a quién en cada segundo.
- **Color por papel.** Cada personaje tiene su color (en el ejemplo del casino, negro = el hombre,
  blanco = la mujer). Aquí John es blanco y los monstruos son negros.
- **Primeros planos legibles.** Un primer plano de un detalle, como la mano en la empuñadura, no
  muestra nada si el personaje es un bloque. En el previz se abre a plano medio y el prompt dice
  qué se ve.

## Cómo se escribe el prompt

1. **ACTIVE REFERENCES.** El video es la referencia maestra de cámara, tiempos, posiciones y
   orientación. "Its figures are a legend, not a look": se explica cada color y se aclara que el
   verde y el rojo son solo el código de orientación, no colores del vestuario. Se dice que las
   figuras están quietas porque el previz no lleva coreografía. Para cámara y posiciones manda el
   video; para el movimiento manda el texto.
2. **STYLE, LIGHTING, COLOR.** Cada uno en su bloque.
3. **CAMERA.** "Strictly video 1", con los movimientos por tramos de tiempo.
4. **PHYSICS.** Pies que cargan peso, la tela con retraso, el peso de la espada, la reacción a cada
   golpe.
5. **CAST AND BLOCKING.** Cuántos personajes hay exactamente y dónde está cada uno.
6. **Coreografía.** Es la columna del video.
7. **ACTION TIMING.** Va por etapas, y cada etapa termina con su "End state": dónde quedan los
   cuerpos en el último segundo.
8. **AUDIO.**
9. **HOLD FOR THE FULL TIMELINE.** Al final se repiten las reglas clave.

Notas:
- No nombrar películas, personas reales ni términos de videojuego, porque el filtro de propiedad
  intelectual bloqueó un borrador por eso. Basta con poner "NON-IP".
- Cada imagen de referencia se define con su papel: "appearance only", "location only", "look
  only".
