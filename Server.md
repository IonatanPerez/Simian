### Insctrucciones y documentacion del server en google cloud ###

Para ejecutar el codigo en forma continua usamos una maquina virtual en google cloud

Necesitamos las siguiente herramientas:

## Maquina Virtual ##

Creamos una maquina virtual en google cloud services. La maquina actual se llama "instance-2" tiene un disco de 100G con un Ubuntu y esta bajo la cuenta ionatan@gmail.com. Una vez creada la maquina instalamos conda y los paquertes necesarios en un enviroment llamado Simian.
El ip externo de dicha maquina es 35.232.197.21

## Conexion ssh ##

Usamos el software putty para conectarnos. Para eso primero con la herramienta que tiene creamos un par clave publica/clave privada. La clave publica la subimos en la seccion metadata de Google Cloud Services para que la VM acepte la conexion. El nombre de usuario asociado es ionatan.

## Ejecutar codigo ##

Para ejecutar codigo primero de debe establecer la conexion ssh. Una vez logueados en la VM hay que actualiza el git que esta en la carpeta ~/Proyectos/Simian 

Una vez actualizado el git corremos tmux para tener una consola nueva que quede corriendo al desconectar la conexion ssh. Dentro de la consola tmux ejecutamos el archivo py que haga lo deseado y con el programa corriendo nos desconectamos de la consolo apretando "Ctrl+b" y luego "d".

Para volver a acceder a la consola donde esta corriendo el codigo debemos ejecutar "tmux ls" para conocer la lista de consolas activas y luego tmux attach -t # donde # es el numero de consola a la que queremos conectarnos. 

## Recuperar archivos ##

Podemos usar WinSCP que permite copiar en forma facil archivos de servidores mediante ssh
