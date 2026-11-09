# Subir los Reels de Valorant a YouTube Shorts

Herramienta para tu PC. Baja tus 20 Reels de Valorant de Instagram y los sube a YouTube
(DuplexDragon) con los títulos y descripciones de `shorts.json`, en orden de mejor a peor
Reel (empieza con Omen y Sage, 40 mil vistas).

## Instalar (una sola vez, Windows)

1. Instala Python 3 desde python.org (marca "Add Python to PATH").
2. Abre esta carpeta, escribe `cmd` en la barra de direcciones y pulsa Enter.
3. Ejecuta:

```
pip install playwright yt-dlp
```

Necesitas tener Google Chrome instalado.

## Usar

Prueba primero con un video en privado y revisando antes de publicar:

```
python subir_shorts.py --cuantos 1 --privado --ver
```

La primera vez se abre Chrome: inicia sesión con la cuenta del canal y pulsa Enter en la
ventana negra. La sesión queda guardada en `perfil/`.

Si salió bien, borra ese video de prueba en YouTube Studio, borra `progreso.json` y sube
uno por día:

```
python subir_shorts.py
```

Cada vez que la corras sube el siguiente pendiente. Subir 1 al día (a las 6-8 p. m.) es
mejor que subir los 20 juntos: YouTube reparte mejor los Shorts y tus suscriptores no
reciben 20 avisos de golpe.

## Si algo falla

- **No baja un video**: guárdalo tú (en Instagram: tu Reel → ⋯ → Descargar, o tu archivo
  original) en la carpeta `videos/` con el nombre del código, por ejemplo
  `videos/DZtdVGUiyg1.mp4`. Los códigos están en `shorts.json`. También puedes usar tu
  sesión de Instagram: `python subir_shorts.py --cookies-de chrome`.
- **Falla la subida**: YouTube cambia su página a veces. Avísale a Claude con el mensaje
  de error para ajustar el script.
- `progreso.json` guarda lo que ya se subió; no repite videos.

Los títulos y descripciones se pueden cambiar en `shorts.json` antes de subir.
