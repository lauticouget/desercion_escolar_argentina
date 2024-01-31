# Desercion Escolar en Argentina 
En Argentina, la educación es un derecho consagrado por la Constitución Nacional y regulado por la Ley Nº 26.206 de Educación Nacional. La escolaridad obligatoria abarca 14 años consecutivos, desde sala de 4 y preescolar en el Nivel Inicial, pasando por el Nivel Primario (con duración de 6 o 7 años según la jurisdicción), hasta el Nivel Secundario (con duración de 6 o 5 años, según la duración del nivel primario de la jurisdicción).

El país cuenta con una cobertura casi universal del Nivel Primario, con tasas de asistencia que se sitúan alrededor del 99%. En el Nivel Secundario la cobertura de la población de entre 12 y 19 años es casi universal en el Ciclo Básico y llega al 91% en el Ciclo Orientado. Sin embargo, aproximadamente el 20% de los jóvenes y adultos de entre 18 y 24 años no ha completado sus estudios obligatorios.

Aunque la tasa de abandono escolar en primaria es notablemente baja, representando un 0,41% del total a nivel nacional, la situación se torna preocupante al ingresar al nivel secundario. Aquí, el abandono asciende al 7,66%, afectando al 16,8% de los estudiantes en su último año de la escolaridad obligatoria.
Frente a este panorama, nuestro proyecto se propone desarrollar un Sistema de Alerta Temprana (SAT) para identificar señales de riesgo de abandono escolar en Argentina, utilizando la Encuesta Permanente de Hogares (EPH) como principal fuente de datos.

Este proyecto no solo tiene la intención de ser una herramienta de detección temprana, sino también un recurso valioso para los formadores de políticas educativas y los profesionales de la educación.

### Objetivos
- Desarrollar un modelo de predicción de deserción escolar para ser utilizado por el SAT.
- Desarrollar un tablero de análisis de datos educativos de la EPH.
- Integrar el SAT en el tablero de análisis.

### Antecedente
Tomás Michel Torino realizó estudio similar en su Tesis de Maestría de la UTDT. En este trabajo se construyó una base de datos utilizando las EPH de los últimos dos trimestres de 2021 y los primeros dos de 2022 para realizar el entrenamiento y validación de modelos que permite predecir si una persona de hasta 18 años de edad ha desertado o no de alguno de los niveles obligatorios del sistema educativo.

La base de datos construida contiene una variable (objetivo) llamada DESERTO con valores binarios (1 si la persona declara haber terminado sus estudios obligatorios y 0 si no lo hicieron y además declaran no continuar cursando).

#### Propuestas de mejora sobre el antecedente
La muestra de la EPH sigue una estructura de tipo 2-2-2:
- Un hogar es entrevistado durante dos trimestres consecutivos.
- Ese hogar se retira de la muestra por dos trimestres.
- El mismo hogar vuelve a entrevistarse dos trimestres consecutivos.

De esta forma, la EPH permite hacer seguimientos longitudinales de los integrantes de un mismo hogar en un período de un año y medio.
El trabajo de Michel Torino no hace uso de esa estructura, en cuanto asigna los valores de la variable objetivo según lo que declaran las personas un único trimestre (borrando duplicados entre distintos períodos de observación). Una posible mejora es construir las bases de datos a partir de las trayectorias: tomar personas que un dado trimestre declararon estar cursando en algún nivel obligatorio, y al volver a a ser encuestadas habían desertado.

A su vez, el estudio de Michel Torino toma la población en edad escolar teórica. Dada  la cobertura del Nivel Primario y Ciclo Básico del Nivel Secundario, podría ser conveniente tomar la población de 15 años o más. Esto permitiría incluir la porción de menor cobertura del Nivel Secundario y la Educación Permanente de Jóvenes y Adultos (EPJA). 

Los valores nulos fueron reemplazados por la media de cada atributo. En el caso particular de los ingresos y deciles de ingresos, podría ser provechoso investigar otras formas de imputación.

# Sobre este repositorio
Organización del proyecto
------------

    ├── README.md
    ├── artifacts          <- Repositorio de artefactos, como logs, transformadores, etc.
    ├── data
    │   ├── raw            <- La data de origen, inmutable.
    │   ├── preprocessed   <- Data intermedia con algunas transformaciones.
    │   └── stage          <- La data lista para ser utilizada en un modelo.
    │
    ├── models             <- Modelos listos.
    │
    ├── notebooks          <- Jupyter notebooks. (desde Humai recomiendan agregarle la fecha al inicio del nombre.)
    
    
Para ejecutar:
------------

Python version: 3.11.5
<br>
Poetry package orchestrator must be installed (version used at installation: 1.6.1)


## Cómo trabajar las ramas ? (GitFlow)
- Rama principal: main
- Rama de desarrollo (la cual sale y va hacia main): develop
- El resto de las ramas salen desde develop y vuelven a develop: 
  - Hacemos una rama por cada tarea de Trello, y nombramos la rama igual a la tarea pero en sneak_case. Ejemplo: Si la tarea de Trello se llama Mi Primer Tarea entonces la rama se llama la_primer_tarea_de_pepito

## Cómo trabajar los commits ?
Todos los commits comienzan el mensaje indicando el nombre de la rama. Esto permite tener facil rastreo del historial de cambios en las ramas tronco (develop y main).
Ejemplo no ideal: La rama la_primer_tarea_de_pepito podría tener 3 commits con los mensajes primera parte de mi tarea, segunda parte de mi tarea y tercera parte de mi tarea. De esta manera quedarían ordenados así en el historial de commits para las ramas tronco (luego de mergear el commit, obvio):
- ```tercera parte de mi tarea```
- ```segunda parte de mi tarea```
- ```primera parte de mi tarea```

El problema con no haber indicado el nombre de rama en el commit es que no sabemos en qué rama se hizo el cambio, por lo tanto perdemos el orden y la posibilidad de usar esa rama si es útil hacer nuevos cambios desde allí.
Ahora, si agregamos el nobre de rama en el mensaje del commit entonces quedaría así:

- ```la_primer_tarea_de_pepito: tercera parte de mi tarea```
- ```la_primer_tarea_de_pepito: segunda parte de mi tarea```
- ```la_primer_tarea_de_pepito: primera parte de mi tarea```

Si Pepe necesita el codigo de Mengano mientras desarrolla su tarea, se lo trae haciendo git pull. Habiendo ambos respetado esta regla de mensaje en los commits lo que sucede cuando se mergea el codigo de Pepe a develop es lo siguiente:


- ```la_primer_tarea_de_pepito: tercera parte de mi tarea```
- ```la_primer_tarea_de_pepito: segunda parte de mi tarea```
- ```la_primer_tarea_de_mengano: codigo super util``` *<-- Acá es muy claro que pepe se trajo este commit de la rama de mengano. Si mengano no nombraba su rama correctamente entonces nadie sabe de donde salió ese commit.*
- ```la_primer_tarea_de_pepito: primera parte de mi tarea```
