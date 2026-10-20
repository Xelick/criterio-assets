# El Edén de las Carnes — equipo de agentes

Diez agentes de Claude Code para la carnicería **El Edén de las Carnes**
(Bogotá), adaptados al español y al negocio a partir de
[msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
(licencia MIT, ver `LICENSE-agency-agents`).

La ficha del negocio — catálogos, WhatsApp, franjas, pagos, combos y reglas de
la casa — está en [`CONTEXTO.md`](CONTEXTO.md). Todos los agentes la leen
primero.

## Los agentes

| Agente | Para qué | Viene de |
|---|---|---|
| [`eden-atencion-whatsapp`](agentes/eden-atencion-whatsapp.md) | Responder pedidos, dudas y reclamos por WhatsApp | Customer Service, Hospitality Guest Services |
| [`eden-ventas-mayoristas`](agentes/eden-ventas-mayoristas.md) | Conseguir restaurantes, asaderos y tiendas | Sales Outreach, Offer & Lead Gen |
| [`eden-fidelizacion`](agentes/eden-fidelizacion.md) | Que los clientes vuelvan: recordatorios, fechas, frecuentes | Customer Success Manager, Email Strategist |
| [`eden-precios-y-margenes`](agentes/eden-precios-y-margenes.md) | Margen por corte, alzas de costo, combos, minorista vs mayorista | Pricing Analyst |
| [`eden-compras-e-inventario`](agentes/eden-compras-e-inventario.md) | Cuánto pedir, rotación, merma, cadena de frío, proveedores | Supply Chain Strategist |
| [`eden-operaciones-y-domicilios`](agentes/eden-operaciones-y-domicilios.md) | Alistamiento por franja, rutas, checklists, procesos | Operations Manager, Workflow Architect |
| [`eden-contabilidad-y-caja`](agentes/eden-contabilidad-y-caja.md) | Cuadre por medio de pago, cartera mayorista, cierre del mes | Bookkeeper & Controller, Finance Tracker |
| [`eden-reporte-semanal`](agentes/eden-reporte-semanal.md) | Resumen semanal de la hoja «Pedidos Edén» para el dueño | Analytics Reporter, Executive Summary |
| [`eden-redes-sociales`](agentes/eden-redes-sociales.md) | Calendario, guiones de reel, textos, estados de WhatsApp | Instagram Curator, TikTok Strategist, Content Creator |
| [`eden-pauta-meta`](agentes/eden-pauta-meta.md) | Anuncios locales en Facebook/Instagram que llevan a WhatsApp | Paid Social Strategist, Paid Media Creative |

Ninguno envía mensajes, publica, edita las hojas de precios ni mueve dinero:
todos **preparan** y alguien de la carnicería (o John) ejecuta. Lo que necesita
aprobación sale marcado `[PROPUESTA — APROBAR]`; lo que no está confirmado,
`[CONFIRMAR]`.

### Qué se dejó por fuera y por qué

Del repo original (más de 300 agentes) se descartaron los de ingeniería,
videojuegos y mercados chinos, y los pensados para empresas grandes (CFO, FP&A,
deal strategist, MEDDPICC, SEO técnico, compra programática). A una carnicería
de barrio le sobran.

## Dónde vive

Esta es la branch **`cliente/el-eden-de-las-carnes`** del repo
`Xelick/criterio-assets`. Es una branch independiente (sin historia común con
`main`): solo trae lo del Edén, no los ~500 assets de Criterio. Cada cliente
tiene su propia branch `cliente/<nombre>`.

Para bajarla sola, sin el resto del repo:

```bash
git clone --single-branch -b cliente/el-eden-de-las-carnes https://github.com/Xelick/criterio-assets.git eden-agentes
```

## Cómo instalarlos

Para usarlos en cualquier proyecto de Claude Code:

```bash
cp eden-agentes/agentes/*.md ~/.claude/agents/
```

O solo en la carpeta de trabajo del Edén (recomendado, así no aparecen en otros
proyectos):

```bash
mkdir -p "<carpeta del Edén>/.claude/agents"
cp eden-agentes/agentes/*.md "<carpeta del Edén>/.claude/agents/"
cp eden-agentes/CONTEXTO.md "<carpeta del Edén>/"
```

Luego, en Claude Code: *«Usa eden-reporte-semanal con la hoja de pedidos de
esta semana»* o *«eden-atencion-whatsapp: un cliente dice que la molida llegó
incompleta»*.

## Ojo: este repo es público

`criterio-assets` es público: cualquiera puede ver esta branch en GitHub (no se
sirve en la web, eso es solo `main`). Aquí van **solo** los
agentes y la ficha con datos que el cliente ya muestra en sus catálogos. Nunca
subir: IDs de hojas, URL del webhook de pedidos, claves, datos de clientes
finales, costos de compra ni cifras de caja.
