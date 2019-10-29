# Porque usar jupyer #

Jupyter es un entorno comodo para programar cuando se quiere intercalar resultados con codigos o cuando se quiere dejar registro de testeos de analisis de datos. Para la elaboracion del codigo final suele ser mas comodo usar un editor de texto que venga con plugins adecuados como es el visual studio code. 

Por eso sugerimos trabajar con jupyer en la fase de testeo y desarrollo y con visual code studio para escribir el py con las funciones ya depuradas.

# Como agregar el enviroment al jupyter #

Jupyter corre por fuera del enviroment activado y tiene una lista de kernels (versiones de python) instalados. Para poder ejecutar el codigo en jupyter en un enviroment dado hay que agregar el kernel correspondiente al enviroment en dicha lista. Esto se debe hacer por unica vez con este codigo 

$ python -m ipykernel install --user --name Simian --display-name "Python (Simian)"

# Como usar jupyter #

Jupyer lab deberia estar instalado si siguieron las instrucciones del archivo Paquetes.md porque es parte estandar del anaconda. Para ejecutarlo hay que poner (en la consola)

$ jupyter lab 

desde la carpeta donde se encuentre el proyecto y esperar a que se abra una ventana en el navegador predeterminado porque funciona como servidor web local. Se trabaja en el navegador desde donde se pueden abrir los archivos en el menu lateral y editarlos en la ventana central. 

