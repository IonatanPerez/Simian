localfolder = "./raw/autores/" # Carpeta donde se almacena la info que se va generando. Esta carpeta esta en el gitignore
scrappingFile = localfolder + "scrappingLog.json" # Archivo donde se guarda info del scrapping
nroAutoresLimiteNulos = 100 # Asumimos que cuando hay 10 ids consecutivos sin info es que se acabo la lista de autores. 
batchLN = 30 # Este es el numero de notas que carga por vez LN al cargar mas notas
numeroDeIntentosDeBusquedaPorAutor = 5 # Cantidad de veces que se trata de buscar las notas para un mismo autor
timewait = 1 # tiempo en segundos que espera antes de buscar mas notas para darle tiempo a la pagina que cargue
processingFolder = "./raw/data/autores/"
startOnId = 0