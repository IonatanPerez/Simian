# Instrucciones para instalar los paquetes necesarios #

La idea es usar conda. Se puede descargar desde https://www.anaconda.com/ y tiene soporte para diferentes sistemas operativos. En esta guia lo vamos a usar desde la consola.

Una vez instalado creamos un enviroment para poder instalar o manipular paquetes sin necesidad de afectar al resto del sistema operativo. 

En https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html hay informacion acerca de como manipular los enviroments. 

Para crear el enviroment usamos de base los paquetes de anaconda.

$ conda create --name Simian anaconda 
$ activate Simian 

una vez dentro del enviroment y en la carpeta del proyecto podemos chequear que no haya algun paquete extra requerido usando:

$ conda env update -f enviroment.yml

enviroment.yml es un archivo donde estan guardados todos los paquetes que tiene el enviroment. La idea es que si por alguna razon se necesita instalar un paquete nuevo quede registro para que quienes repliquen en proyecto en otra compu actualicen su enviroment. Para actualizar el archivo se debe utilizar

$ conda env export > environment.yml