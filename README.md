# API-REST COUNTRIES


Servidor HTTP simple sin uso de frameworks(flask ,django, etc)

Este servidor responde a solicitudes tipo GET de acuerdo a las especificaciones solo tenemos un endpoint el cual a su vez consume una API REST externa para
la extraccion  y clasifcacion de datos asociados a paises , de acuerdo a esto para poder ejecutar el proyecto debemos hacer lo siguiente



# INSTALACION [LINUX]
requisitos:
1: tener instalado python 3
2: tener instalada la libreria para creacion de entornos virtuales en python3 en caso de no tenerla ejecutar sudo apt-get install python3-venv
clonar el proyecto en su repositorio local y desplazarse hasta ese directorio , posteriormente crear un entorno virtual para instalar las dependencias 

> python3 -m venv venv

luego debera activar el entorno virtual anteriormente creado

> . venv/bin/activate  o bien usando el comando   source venv/bin/activate


una vez activado el entorno virtual debera instalar las dependencias por lo que en la raiz del proyecto ejecutar el siguiente comando

> pip install -r requirements.txt o bien  el comando   pip3 install -r requirements.txt


una vez instaladas las dependencias correr el script main.py  

> python main.py   o bien el comando python3.py

una vez ejecutado podra ir al url  http://127.0.0.1:8000/      y obtendra la respuesta en formato JSON de acuerdo a las especificaciones


al hacer la solicitud de tipo GET en este endpoint , en su directorio local se generara un archivo data.json que tendra la informacion vista desde el navegador
pero en un archivo JSON

si desea tambien puede realizar la solicitud GET desde la linea de comandos 
> curl http://127.0.0.1:8000/

# FUNCIONAMIENTO
![alt text](https://github.com/sebas1017/tangelo_challenge_api/blob/main/images_demo/APIREST.png?raw=true)
![alt text](https://github.com/sebas1017/tangelo_challenge_api/blob/main/images_demo/DATABASE.png?raw=true)


# DISEÑO DE LA SOLUCION 
![alt text](https://github.com/sebas1017/tangelo_challenge_api/tree/main/images_demo/PROCESS_DIAGRAM_API.png?raw=true)


La solucion planteada la defini desde un servidor HTTP simple en python3 creando este , tenemos un endpoint que se encuentra en la raiz de la direccion local , puerto 8000(se puede cambiar en caso de que tengan el puerto ocupado)
al realizar una solicitud de tipo GET al endpoint este a su vez ejecuta el llamado a la APIREST externa  https://rapidapi.com/apilayernet/api/rest-countries-v1  desde la cual esta misma cuenta con un endpoint el cual es :
>https://restcountries-v1.p.rapidapi.com/all  y luego se hace el llamado a los datos por region en el siguiente endpoint   https://restcountries.eu/rest/v2/region/{region}

este nos entrega toda la informacion de las regiones existentes(continentes) en este caso se procesa la informacion y solo se dejan las distintas regiones(conjunto)
luego de la solicitud GET desde el servidor HTTP hacia la API REST externa esta misma entrega una respuesta hacia el servidor HTTP nuevamente una vez el servidor procesa la informacion  genera un archivo en la ruta local del proyecto llamado data.json el cual contiene el resultado de los datos solicitados,posteriormente en esta parte del proceso a su vez se guardan las estadisticas de tiempo de procesamiento en milisegundos , esto en la base de datos SQLITE que es creada en la carpeta instance al ejecutar por primera vez el proyecto


luego de esto al punto inicial desde el que hicimos el llamado a nuestro servidor HTTP es decir desde nuestro navegador es devuelto en formato JSON los resultados del procesamiento de datos
se utilizo pandas para la manipulacion de las estadisticas generando un dataframe
Tambien adjunto en el presente repositorio el archivo del diagrama del diseño de la solucion generado desde draw.io
