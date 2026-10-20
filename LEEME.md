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
