#! /usr/bin/env python

import sys
import json
salidas=[] #lista de diccionarios
for asn in sys.argv[2:]: #asn(son los nodos a los que se le van a validar sus vecinos)

    prefijos=set() #variable que representa las redes
    vecinos=set() #variable de los nodos vecinos
    archivo= open(sys.argv[1],"r")  #abre un archivo pasando los argumento como banderas
    for linea in archivo.readlines(): #inicia lectura linea a linea del archivo
        #print linea
        partes= linea.strip().split("|") #separa la linea con el separador |
        ases= partes[6].split(" ") #ases toma la columna 6 donde estan los nodos ['4608', '1221', '4637', '2497']
       # print partes[5]
       # print ases
        #print ases[-1]
        if  asn not in ases:  
    		continue
        prefijos.add(partes[5])	#se carga los prefijos que no sean iguales
        posiciones=	[i for i,x in enumerate(ases) if x==asn]# permite validar las posiciones en una lista que tiene el mismo valor
        #print posiciones
        posmax= len(ases)-1 #maxima posicion de la lista ases
        #print posmax
        for pos in posiciones: #permite recorrer la lista para validar si el asn tiene vecinos
            if pos+1 <= posmax and ases[pos+1]!=asn: # pregunta una posicion hacia adelante
                vecinos.add(ases[pos+1])
            if pos-1 >=0 and ases[pos-1]!=asn: #pregunta una posicion hacia atras
                vecinos.add(ases[pos-1])
        #print vecinos
        #print prefijos
    archivo.close()
    
    salidas.append({ # crea una lista de diccionarios para importar a json
            'Origin-AS':asn,
            'neighbours':list(vecinos),
            'prefixes':list(prefijos)      
            
            })

with open("module_out.json", "w") as f: #genera el archivo de salida .json
    json.dump(salidas,f)

