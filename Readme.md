# Documentacion LN

Este archivo contiene la documentacion de la estructura de datos usada para recolectar info de la pagina de LN

Queremos recolectar la info disponible de cada autor de LN aprovechando que tienen una pagina donde estan todas sus notas indexadas. 

## Notas tecnicas del funcionamiento del sitio LN

- LN usa un sistema de URLS donde basicamente se ignora los textos y solo considera el arbol de la URL en caso de que haya y los ids que estan al final. Esto lo hace para varios de sus contenidos, para los autores, para las notas, y para las imagenes.

- Por ejemplo al tener una URL de un autor de la forma https://www.lanacion.com.ar/autor/test-id buscara las notas del autor [id] sin importar el texto test o el que haya en su lugar.

- Haciendo una revision rapida, al 26/10/19 tienen hasta el id 13170, buscando con mas cuidado aparecen id en el medio sin informacion pero al menos hasta el autor 13170 parece haber id creados. 

### Estructura del codigo y de la logica de busqueda.
- Se crea un diccionario general donde por el id se accede a la info del autor correspondiente.
- Se hace un barrido por id buscando las notas que estan indexadas a cada autor usando una navedador
- Como en la pagina que se carga originalmente no figuran todas las notas (se cargan de a batch de a 30) hay que clikear en el boton inferior hasta que cargue todas las notas. Para evitar errores entre click y click se espera y ademas al no encontrar mas notas se hace un chequeo (si se encuentra multiplos de 30 notas se sospecha que se corto la carga antes del final)
- Con la pagina cargada se levanta la info general del autor.
- Una vez cargada la pagina con todos los links, se comienza procesar cada uno de ellos y se los agrega a la lista de noticias del autor. 
- Cada un numero fijo de autores se vuelca a disco la info para evitar manipular cantidades muy altas de datos en memoria. Tambien se vuelca a disco en caso de error o interrupcion. 

### La estructura de datos para cada autor va a ser la siguiente:
- Nombre (STR) -- Nombre completo del autor extraido de la pagina
- Id (Int) -- Id interno de LN para el autor
- URL (STR) -- URL de la pagina que se esta analizando
- Medio (STR) -- Medio para el cual escribe el autor que se indica en la pagina 
- Bio (Long STR) -- Bio extraida de la pagina, puede ser un texto largo o puede no haberlo
- FotoUrl (STR) -- Url de la foto
- FotoId (INT) -- Id de la foto para eventualmente identificar imagenes descargadas. LN usa un servidor de fotos con un formato que es el siguiente https://bucket[1,2,3].glanacion.com/anexos/fotos/[id[-2:]]/[id]h[altoenpixeles].jpg
- Notas (LST(dict)) -- Listado de notas donde cada nota es un dict.
- NotasEncontradas (INT) -- Cantidad de notas encontradas
- ScrollingCorrecto (BOOL) -- Indica si se presume que termino de scrollear bien al buscar mas noticias.
- Last (DATE) -- Indica la fecha de la ultima nota recolectada para poder reanudar desde alli. 

### La estructura de datos para cada nota va a ser la siguiente:

- Id (INT) -- Id de la nota
- IdAutor (INT) -- Id del autor de la nota
- Link (STR) -- Link a la nota
- Seccion (STR) -- Parte de url que corresponde a la seccion. Es importante para que se puede buscar la nota por el id construyendo bien el path
- Tema (STR) -- Tema 
- TemaId (INT) -- Id del tema, sirve para hacer despues busquedas por tema con urls del estilo https://www.lanacion.com.ar/tema/test-tid[ID]
- ImagenUrl (STR) -- link a la imagen que ilustra la entrada de la nota
- ImagenId (INT) -- id de la imagen, sirve para buscarla en los servidores con un url generica
- Fecha (STR) -- La fecha leida como un string.

# Pendientes
- Ver que no retome uno atras (revisar como quedo id 59 y 60) Resuelto.
- Ver que sepa que esta buscadio cuando vuelve a buscar el mismo id. Resuelto.
- Hacer que si l primer id de nota ya esta en la lista ni busque los 30 primeros. Resuelto
- Por alguna razon el navegador se cuelga en el autor Id 196. Revisar que pasa. Lo salteo
- Hacer que cuando crea la entrada de cada nota en el autor, el id ademas de usarlo como key lo guarde dentro.
- Cuando se corta por algo y graba parcial, despues cuando retoma ve que ya esta cargada la info y no sigue :(  Resuelto