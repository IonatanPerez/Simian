import IPython.core.oinspect as insp

print ("Recuerde que para que esta clase funcione debe incluir self.chequeosdeimplementacion() en caso de sobreescrbir el __init__")

isabstract = "Implementar"

class Abstract:
   
    def __init__ (self,*args):
        print ("Me iniciaste")
        print (*args)
        self.chequeosdeimplementacion()
        self.runoninit(*args)
        
    def chequeosdeimplementacion(self):
        metodos = [method for method in dir(self) if callable(getattr(self, method))]
        metodos = [metodo for metodo in metodos if not metodo[0:2]=="__"]
        propiedades = [method for method in dir(self) if not callable(getattr(self, method))]
        propiedades = [propiedad for propiedad in propiedades if not propiedad[0:2]=="__"]
        if metodos:
            for metodo in metodos:
                linea = insp.getsource(getattr(self, metodo)).split("\n")[1].lstrip()
                if linea == "return isabstract":
                    print ("Warning: En " +type(self).__name__+" no se implemento el metodo " + metodo)
        if propiedades:
            for propiedad in propiedades:
                if getattr(self, propiedad) == isabstract: print ("Warning: En " +type(self).__name__+" no se implemento la propiedad " + propiedad)
                    
    def runoninit(self,*args):
        print (*args)