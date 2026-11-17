# Titan Data Analyst

Proyecto de análisis de datos operacionales sintéticos. Lee un CSV de turnos y genera métricas agregadas por turno, comparaciones con plan y un reporte JSON trazable.

## Pregunta analítica

¿Cómo varían producción, cumplimiento, detenciones y tiempo de ciclo entre turnos Día y Noche? El conjunto es didáctico; las diferencias observadas no explican causas ni representan una faena real.

## Ejecutar

Requiere Python 3.10 o superior y no instala dependencias.

```powershell
python analyze.py data/shifts.csv --output report.json
```

## Métricas

- Toneladas totales y planificadas.
- Cumplimiento ponderado = toneladas reales / plan.
- Disponibilidad ponderada = minutos operativos / minutos programados.
- Media de tiempo de ciclo de los registros válidos.
- Conteo de filas válidas y rechazadas.

Las filas inválidas se contabilizan y se omiten; los valores faltantes no se imputan. El reporte incluye las fórmulas y el nombre del archivo analizado.

## Diccionario de datos

`date`, `shift`, `planned_tonnes`, `actual_tonnes`, `scheduled_minutes`, `downtime_minutes`, `cycle_time_min`, `material`. Toneladas en t; tiempos en minutos. El dataset se etiqueta como sintético.

## Licencia

MIT para código y datos de ejemplo.
