# Ficha del negocio — El Edén de las Carnes

Fuente única de datos para los agentes de esta carpeta. Si algo cambia (precios,
número, combos), se cambia aquí primero y luego en el agente que lo cite.

> Este repo es **público** (se sirve en GitHub Pages y Netlify). Aquí solo va lo
> que el cliente ya muestra en sus catálogos. Nada de IDs de hojas, URLs de
> webhooks, claves ni datos de clientes finales.

## Quiénes son

- **Negocio:** carnicería de barrio en Bogotá — res, cerdo, pollo, vísceras,
  pescado y embutidos.
- **Dirección:** Transversal 80G # 2-12, Bogotá.
- **WhatsApp de pedidos:** 310 553 0634 (`wa.me/573105530634`).
- **Clientes:** hogares del sector (minorista) y restaurantes, asaderos y
  tiendas (mayorista). Gente poco tecnológica: todo pasa por WhatsApp.

## Cómo venden hoy

| Canal | Dónde | Cómo funciona |
|---|---|---|
| Minorista | https://edencatalogo.netlify.app/ | 56 productos con precio, opción de gramaje exacto, 3 combos, regalo por compras de $100.000 o más |
| Mayorista | https://mayoristascarneseleden.netlify.app/ | 77 cortes a precio por kilo. Se pide **por unidad**; el total se calcula al pesar en la entrega |

El cliente arma el pedido en el catálogo y se abre WhatsApp con el mensaje ya
escrito: productos, día de entrega, franja horaria, nombre, teléfono, dirección
y método de pago.

- **Franjas de entrega:** 7–9 a.m., 9–11 a.m., 11 a.m.–1 p.m.
- **Pagos:** efectivo, Nequi, Daviplata, transferencia, tarjeta.
- **Combos vigentes (minorista):** De la Casa $130.000 · Familiar $180.000 ·
  Completísimo $250.000. Traen su propio obsequio y **no suman** para el regalo
  de $100.000.
- **Precios:** viven en dos hojas de Google Sheets (minorista y mayorista); los
  catálogos los leen en vivo. Cambiar un precio = editar la hoja, no el sitio.
- **Registro de pedidos:** cada pedido del minorista confirmado queda en la hoja
  «Pedidos Edén» (fecha, cliente, productos, total, franja, pago).

## Precios de referencia (sep 2026)

Lomo fino $56.000 · Tilapia $28.000 · Chorizo santandereano x5 $18.000 ·
Chorizo santarrosano x10 $22.000. Mayorista: pernil sin hueso +50 kg $13.000/kg,
costilla ahumada paquete x5 kg $95.000. Para cualquier otro precio, la hoja
manda: nunca inventar uno.

## Lo que todavía falta

- Afiches reales de los 3 combos nuevos.
- Fotos reales de ~30 cortes del mayorista que hoy usan foto genérica.
- Definir qué cortes del mayorista se venden en paquete (ej. pezuña x6).
- Dominio propio para los catálogos.

## Reglas de la casa para cualquier agente

1. **Español de Colombia, trato de usted**, cálido y directo. Nada de jerga
   corporativa ni anglicismos.
2. **Nunca inventar** precios, existencias, horarios ni promociones. Si no está
   en esta ficha o en la hoja, se pregunta a John o a la carnicería.
3. **Mensajes para WhatsApp sin emojis «astral»** (👋📅🎁…) dentro de enlaces
   `wa.me` — en iPhone llegan rotos. En texto normal, con moderación.
4. **Fotos honestas:** un corte sin foto real va sin foto o con la de su
   categoría, nunca con una foto de stock que parezca del local.
5. La carne es perecedera: cualquier recomendación tiene que respetar la cadena
   de frío y la rotación (lo primero que entra es lo primero que sale).
