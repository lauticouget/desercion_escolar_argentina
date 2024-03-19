# Construcción del dataset

## De la base de hogares

### Variables identificatorias
 La siguiente lista de variables sirven para identificar a cada hogar de la base de datos (por la unión de _CODUSU_ y _NRO_HOGAR_) y al unir encuestas de distintos períodos. A su vez, se incluye aquí información geográfica.

    CODUSU: Código de identificación de la vivienda.
    NRO_HOGAR: código de identificación del hogar.
    REALIZADA: indica si la encuesta se realizó en ese hogar.
    ANO4: año de realización de la encuesta.
    TRIMESTRE: trimestre de realización de la encuesta.
    REGION: región geográfica.
    MAS_500: indica si el aglomerado tiene más de 500.000 habitantes o no.
    AGLOMERADO: código de identificación del aglomerado.
    PONDERA: ponderador estadístico.

### Variables utilizadas en la construcción del dataset

    IV1: tipo de vivienda.
    IV2: cantidad de ambientes de la vivienda.
    IV3: materiales del piso de la vivienda.
    IV4: materiales de la cubierta exterior del techo.
    IV5: indica si el techo tiene cielorraso/revestimiento interior.
    IV6: indica si la vivienda tiene agua. 
    IV7: indica si el agua es de la red pública o no.
    IV8: indica si tiene baño o letrina.
    IV9: indica si el baño/letrina se encuentra dentro o fuera de la vivienda.
    IV10: indica si el baño tiene inodoro con botón y arrastre de agua o no.
    IV11: indica si el desagüe del baño es a la red pública o no.
    IV12_1: indica si la vivienda está ubicada cerca de un basural.
    IV12_2: indica si la vivienda está ubicada en una zona inundable.
    IV12_3: indica si la vivienda está ubicada en una villa de emergencia.
    II1: indica la cantidad de ambientes para uso exclusivo del hogar.
    II2: indica cuántos de esos ambientes se usan para dormir.
    II3: indica si alguno de esos ambientes se usan exclusivamente como lugar de trabajo.
    II4_1: indica si el hogar tiene cuarto de cocina.
    II4_2: indica si el hogar tiene lavadero.
    II4_3: indica si el hogar tiene garage.
    II7: indica el régimen de tenencia del hogar.
    II8: indica el combustible utilizado para cocinar.
    II9: indica tenencia y uso de baño.
    
    Las siguientes variables indican si en los últimos tres meses, las personas del hogar han vivido:
    V1: de lo que ganan en el trabajo.
    V2: de alguna jubilación o pensión.
    V21: del aguinaldo de alguna jubilación o pensión del mes anterior.
    V22: del retroactivo de alguna jubilación o pensión del mes anterior.
    V3: de la indemnización por despido.
    V5: de un subsidio o ayuda social del gobierno, iglesias, etc.
    V6: con mercaderías, ropa, alimentos del gobierno, iglesias, escuelas, etc. 
    V7: con mercaderías, ropa, alimentos de familiares, vecinos u otras personas que no viven en el hogar.
    V8: de algún alquiler de su propiedad.
    V11: de intereses o rentas por plazos fijos/inversiones.
    V12: de cuotas de alimentos o ayuda en dinero de personas que no viven en el hogar.
    V13: de gastar ahorros. 
    V14: de pedir préstamos a familiares/amigos.
    
    Resumen del hogar
    IX_TOT: cantidad total de miembros del hogar.
    IX_MEN10: cantidad de miembros menores de 10 años.
    IX_MAYEQ10: cantidad de miembros mayores de 10 años.
    DECCFR: decil de ingresos familiar del total de la EPH.

## De la base de individuos
### Variables identificatorias

La siguiente lista de variables sirven para identificar a cada persona de la base de datos (por la unión de _CODUSU_, _NRO_HOGAR_, y __COMPONENTE_), unir individuos con hogares y encuestas de distintos períodos. A su vez, se incluye aquí información geográfica.

    CODUSU: Código de identificación de la vivienda.
    NRO_HOGAR: código de identificación del hogar.
    COMPONENTE: código identificador de la persona.
    H15: indica si la encuesta se realizó en ese hogar.
    ANO4: año de realización de la encuesta.
    TRIMESTRE: trimestre de realización de la encuesta.
    REGION: región geográfica.
    MAS_500: indica si el aglomerado tiene más de 500.000 habitantes o no.
    AGLOMERADO: código de identificación del aglomerado.
    PONDERA: ponderador estadístico.

### Variables usadas en la construcción del dataset
    CH03: relación de parentesco.
    CH04: sexo.
    CH06: años cumplidos.
    CH07: estado civil.
    CH08: tipo de cobertura médica.
    CH09: condición de analfabetismo.
    CH10: asistencia a establecimientos educativos.
    CH11: indica si el último establecimiento al que asiste o asistió es público o privado.
    CH15: indica dónde nació.
    CH16: indica dónde vivía hace cinco años.
    NIVEL_ED: indica el nivel educativo.
    ESTADO: indica la condición de actividad. 
    PP02E: indica motivos por los cuales la persona no buscó trabajo en los últimos 30 días.
    PP02H: indica si la persona buscó trabajo en los últimos 12 meses.
    PP07H: indica si la persona recibe descuentos jubilatorios por su trabajo.
    PP07I: indica si la persona aporta por si misma a algún sistema jubilatorio.
    PP04B1: indica si la persona presta servicio doméstico como ocupación principal.
    T_VI: total de ingresos no laborables
    V2_M: total de ingresos por jubilación o pensión.

## Variables creadas para el dataset

    CH06_jefx: edad del jefe de hogar.
    ESTADO_jefx: estado laboral del jefe de hogar.
    NIVEL_ED_jefx: nivel educativo del jefe de hogar.
    PP02E_jefx: indica motivos por los cuales el jefe de hogar no buscó trabajo en los últimos 30 días.
    PP07H_jefx: indica si el jefe de hogar buscó trabajo en los últimos 12 meses.
    ESTADO_conyuge: estado laboral del cónyuge.
    CONYUGE_TRABAJA: estado laboral del cónyuge.
    JEFA_MUJER: indica si la jefa de hogar es mujer.
    HOGAR_MONOP: indica si el hogar es monoparental.
    ratio_ocupados: indica el ratio de miembros ocupados sobre miembros totales del hogar.
    
    Las siguientes variables indican necesidades básicas insatisfechas del hogar
    NBI_COBERTURA_PREVISIONAL
    NBI_DIFLABORAL
    NBI_HACINAMIENTO
    NBI_SANITARIA
    NBI_TENENCIA
    NBI_TRABAJO_PRECARIO
    NBI_VIVIENDA
    NBI_ZONA_VULNERABLE
    DESERTO: variable objetivo.