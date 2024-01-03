# README

Es necesario copiar y pegar el código en la página : https://www.codingame.com/ide/puzzle/onitama
Y compilará y el bot empezará a jugar.

## Descripción del Código

El código proporcionado parece ser una implementación en Python de un juego de tablero táctico para dos jugadores, donde cada jugador tiene un conjunto de cartas y debe realizar movimientos para intentar ganar el juego. A continuación, se proporciona una descripción general de las partes clave del código:

### Estructuras de Datos
- **Nodo:** Representa un estado del juego, incluyendo la disposición del tablero y la ubicación de las fichas de cada jugador.
- **Carta:** Representa una carta del juego, con un identificador único y una lista de movimientos asociados.
- **Movimiento:** Representa un movimiento realizado por un jugador, con la información sobre el cambio en la posición de una ficha y la carta utilizada.

### Funciones Principales
- **parseListToDictCartas:** Convierte una lista de cartas en un diccionario, donde la clave es el identificador del jugador y el valor es otro diccionario con las cartas y sus movimientos asociados.
- **intercambiarCarta:** Realiza un intercambio de cartas entre los jugadores.
- **bitboard_to_board:** Convierte una representación de tablero en formato bitboard a una matriz de caracteres.
- **board_to_bitboard:** Convierte una matriz de caracteres a una representación de tablero en formato bitboard.
- **evaluate:** Evalúa la posición actual del juego asignando puntuaciones en función de diversos criterios, como la posición de los maestros, la dominación de ciertas áreas y las fichas restantes.
- **get_possible_moves:** Obtiene los posibles movimientos que puede realizar un jugador en un estado dado.
- **alpha_beta_timeout:** Implementa el algoritmo Alpha-Beta Pruning con límite de tiempo para determinar el mejor movimiento posible en un estado del juego.
- **obtenerElMejorMovimiento:** Utiliza el algoritmo Alpha-Beta Pruning para encontrar el mejor movimiento posible para un jugador dado.

### Bucle del Juego
El código está diseñado para ejecutarse en un bucle infinito, donde se lee la entrada que representa el estado actual del juego, se realiza el cálculo del mejor movimiento y se imprime la salida correspondiente.

## Instrucciones para Ejecutar
Para ejecutar el código, se debe proporcionar una entrada que represente el estado actual del juego. La salida del programa indicará el mejor movimiento que el jugador debe realizar.

## Nota Importante
El código parece tener una sección marcada con "tengo un Bug", que podría indicar la presencia de un error o problema que necesita ser corregido.

Se recomienda revisar y depurar esa sección para asegurar el correcto funcionamiento del programa. Además, es posible que se deban realizar ajustes adicionales según los requisitos específicos del juego o del entorno de ejecución.

Espero que esta descripción sea útil para entender el propósito y el funcionamiento general del código. ¡Buena suerte con tu proyecto!
