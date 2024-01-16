# Desercion Escolar en Argentina 
(usar vista previa en los comandos de VSCode para visualizar mejor el documento)

Este proyecto pretende servir como herramienta predicciones acerca de la deserción de escuela secundaria en los aglomerados de la Argentina.

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

## Cookie cutter template
https://github.com/deployr-ai/workstation

Archivo README del template del proyecto: ./template_README.md
