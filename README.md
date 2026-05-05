# Sistema de Juego de Bingo — Práctica 2

Sistema completo de bingo orientado a objetos que extiende el generador de cartones de la Práctica 1, incorporando jugadores, bombo de extracción y un director de partida. El diseño materializa cuatro tipos distintos de relación entre clases (herencia, composición, agregación y asociación).

## Cómo ejecutar

```bash
python main.py
```

**Requisitos:** Python 3.11 o superior. No necesita librerías externas (solo biblioteca estándar).

## Estructura del proyecto

```
proyecto_bingo/
├── carton.py          # Clase base Carton (adaptada de la Práctica 1)
├── carton_doble.py     # Clase CartonDoble (hereda de Carton)
├── bombo.py           # Clase Bombo (extracción de números)
├── jugador.py         # Clase Jugador (posee cartones)
├── juego.py           # Clase Juego (director de la partida)
├── main.py            # Script de demostración
└── README.md          # Este archivo
```

## Descripción del diseño

El sistema se compone de cinco clases con responsabilidades bien delimitadas:

- **`Carton`** modela una grilla de 5×5 generada a partir de una palabra de 5 letras no repetidas y un número máximo múltiplo de 5 entre 50 y 90. Encapsula la generación de la grilla, el marcado de números y la verificación de bingo.
- **`CartonDoble`** extiende `Carton` con una segunda grilla independiente, permitiendo a su poseedor ganar si completa cualquiera de las dos.
- **`Bombo`** mantiene los números disponibles, extrae sin repetición y registra el historial de la partida.
- **`Jugador`** representa a un participante que posee uno o más cartones (incluidos cartones dobles) y lleva el conteo de marcados.
- **`Juego`** orquesta la partida: registra jugadores, ejecuta turnos, detecta al ganador y produce el reporte final.

## Relaciones entre clases

### Cartón ↔ CartónDoble — HERENCIA
`CartonDoble` **es un tipo de** `Carton`. Hereda todos sus atributos y métodos (grilla, marcado, verificación de bingo) y extiende su comportamiento agregando una segunda grilla. Sobrescribe `verificar_bingo()` y `marcar_numero()` para considerar ambas grillas (polimorfismo) e introduce `grilla_mas_cercana()` como método propio. La reutilización se logra mediante `super()`, evitando duplicar la lógica de la clase base. Esta relación se eligió porque un cartón doble cumple el contrato completo de un cartón: cualquier código que espere un `Carton` puede recibir un `CartonDoble` sin modificación.

### Juego ↔ Bombo — COMPOSICIÓN ◆
El `Bombo` **es parte del** `Juego` y no puede existir sin él. Se crea internamente dentro del constructor del `Juego` como atributo privado (`self.__bombo`), de modo que el código externo nunca tiene una referencia directa al bombo ni puede instanciarlo de forma independiente para esta partida. Si el `Juego` se destruye, el `Bombo` desaparece con él. Esta relación fuerte refleja que el bombo es un elemento constitutivo del juego, sin sentido fuera de una partida concreta.

### Jugador ↔ Cartón(es) — AGREGACIÓN ◇
El `Jugador` **tiene** cartones, pero los cartones se crean **fuera** del jugador y se le asignan mediante `agregar_carton()`. Un cartón existe con independencia de quién lo posea: fue generado previamente y puede ser devuelto con `retirar_carton()` para reasignarse a otro jugador. Si el jugador abandona la partida, sus cartones siguen existiendo. Esta relación más laxa permite la reasignación dinámica de cartones y refleja la realidad del bingo, donde los cartones se reparten pero no pertenecen ontológicamente al jugador.

### Juego ↔ Jugador(es) — ASOCIACIÓN
El `Juego` **conoce** a los jugadores pero no los crea ni los destruye. Los jugadores se construyen externamente y se registran voluntariamente mediante `registrar_jugador()`; pueden retirarse en cualquier momento con `retirar_jugador()` y seguir existiendo después. Son entidades completamente independientes que colaboran durante la partida. Esta relación es la más débil de las cuatro: una pura referencia que habilita la comunicación (notificación de números extraídos) sin implicar dependencia de ciclo de vida.

## Salida esperada

Al ejecutar `python main.py` se mostrará en consola:
1. Los cartones repartidos a cada uno de los tres jugadores (uno con `CartonDoble`).
2. El desarrollo turno a turno: número extraído y qué jugadores lo marcaron.
3. El anuncio del ganador en cuanto alguien complete bingo.
4. Un reporte final con turnos jugados, números extraídos, ganador y estadísticas por jugador.# ProgIVG102-Act02-Bingo
