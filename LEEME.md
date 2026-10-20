# Equipo de agentes — Criterio AI

Doce agentes de Claude Code para la agencia, en `agentes/`. Se instalan copiando
esa carpeta a `.claude/agents/` del espacio de trabajo.

Adaptados de [agency-agents](https://github.com/msitarzewski/agency-agents) (MIT).
No es una traduccion: el repo original trae `name` legible con color/emoji/vibe,
y Claude Code necesita `name` como identificador invocable. El contenido esta
reescrito contra el plan vigente de la agencia.

**Nada se edita a mano.** Se edita `construir_agentes.py` y se vuelve a correr:

```bash
uv run --no-project python construir_agentes.py
```

## Los doce

| Agente | Para que |
|---|---|
| `crit-jefe-de-gabinete` | Hace cumplir el plan y la semana 60/30/10 |
| `crit-oferta` | La oferta empaquetada: que incluye y que no |
| `crit-cuentas` | De cliente entregado a mensualidad y referidos |
| `crit-propuestas` | Propuestas y cotizaciones que cierran |
| `crit-descubrimiento` | Las conversaciones con dueños de negocio |
| `crit-linkedin` | Publicaciones en ingles que abren conversacion |
| `crit-reels` | Los reels de proceso, el unico canal automatizado |
| `crit-precios-usd` | Precios en dolares para clientes de afuera |
| `crit-verificador` | Que lo que sale afuera sea cierto |
| `crit-marca` | Que todo se vea de la misma familia |
| `crit-plata` | Lo que entra, lo que falta cobrar, como va el mes |
| `crit-automatizaciones` | Si una automatizacion merece existir |

## Reglas comunes

Ninguno manda mensajes, publica, cobra ni pone precio por su cuenta: preparan el
borrador y la persona decide. Lo interno va en espanol de Colombia; lo que va a
un cliente de afuera, en ingles.

## Donde se instalan

Claude Code busca los agentes en `.claude/agents/` de la **raiz del espacio de
trabajo**, no en subcarpetas. El generador escribe en los dos sitios:

- `00_AGENCIA/.claude/agents/` — la casa canonica, junto al resto de la agencia
- `<raiz del espacio>/.claude/agents/` — donde se encuentran de verdad

Si solo vivieran en la subcarpeta, no cargarian salvo que la sesion se abra
exactamente ahi. Y estos son agentes de toda la agencia, no de una carpeta.

**Los agentes de proyecto se registran al abrir la sesion.** Despues de generar,
hay que reabrir Claude Code para que aparezcan.

## Como ejecutan

Cada agente deja su trabajo en disco, no en el chat:

    00_AGENCIA/_equipo/salidas/<agente-sin-crit>/AAAA-MM-DD-tema.md

Todos traen un procedimiento numerado y una **tarea por defecto**: si se invocan
sin encargo, saben que hacer. Y todo entregable lleva «lo que necesito de John»
y «lo que no pude verificar».
