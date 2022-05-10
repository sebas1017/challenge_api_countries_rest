# API-REST COUNTRIES
![alt text](https://github.com/sebas1017/tangelo_challenge_api/blob/main/images_demo/docker.jpeg?raw=true)

![alt text](https://github.com/sebas1017/tangelo_challenge_api/blob/main/images_demo/python_http_server.png?raw=true)


![alt text](https://github.com/sebas1017/tangelo_challenge_api/blob/main/images_demo/heroku.png?raw=true)

actualmente puede ver desplegada la api en https://api-countries-http.herokuapp.com/
Servidor HTTP simple sin uso de frameworks(flask ,django, etc)

Este servidor responde a solicitudes tipo GET de acuerdo a las especificaciones solo tenemos un endpoint el cual a su vez consume una API REST externa para
la extraccion  y clasifcacion de datos asociados a paises , de acuerdo a esto para poder ejecutar el proyecto debemos hacer lo siguiente
# INSTALACION [HEROKU-SERVIDOR][CON DOCKER]
debe tener una cuenta creada en heroku y descargar el cliente de heroku luego:
    heroku login
    heroku container:login
    heroku create api-countries-http  #o el nombre que desee
    heroku container:push web -a  api-countries-http
    heroku container:release web -a  api-countries-http  #esto despliega

# INSTALACION [LINUX][CON DOCKER][LOCALMENTE]
1: tener instalado docker

clonar el proyecto y en la carpeta al nivel del Dockerfile ejecutar el siguiente comando
> docker build -t api_countries_http .

el punto indica que creara una imagen de docker apartir del Dockerfile que se encuentra
en la ruta actual donde ejecuta el comando , una vez realizado esto la imagen estara creada
y podra crear un contenedor de la api con el siguiente comando

> docker run -p 8000:8000 api_countries_http

este comando ejecutara un container de la api , expuesto en el puerto 8000 de la maquina propia
y por lo tanto ya podra dirigirse a la ruta http://localhost:8000 y al invocar este url en la raiz debe esperar a que cargue la api y podra ver los resultados del procesamiento de datos y si entra al contenedor podra ver que en los archivos , se creo automaticamente data.json y la base de datos sqlite en la ruta instance/tangelo_challenge.sqlite
# INSTALACION [LINUX][SIN DOCKER][LOCALMENTE]
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



para ejecutar los tests he implementado un script en bash que hace peticiones basicas a la api
mientras esta en funcionamiento , para ejecutarlo ir a la ruta instance/test_api.sh

este script debe ser ejecutado mientras la api esta en localhost corriendo, bien sea 
atraves de docker o de forma local con las instrucciones anteriormente nombradas
tambien se debe tener en cuenta que se captura la excepcion en caso de que la API
externa no responda el JSON adecuado ya que he notado que al hacer peticiones desde la misma maquina existen ocasiones en las que el json retornado es diferente , para lo cual
solo debe recargar la API y para lo cual desde el codigo he controlado con un lapso de tiempo
entre peticion y excepciones , saludos!!
# FUNCIONAMIENTO
![alt text](https://github.com/sebas1017/tangelo_challenge_api/blob/main/images_demo/APIREST.png?raw=true)
![alt text](https://github.com/sebas1017/tangelo_challenge_api/blob/main/images_demo/DATABASE.png?raw=true)


# DISEÑO DE LA SOLUCION 
![alt text](https://github.com/sebas1017/tangelo_challenge_api/blob/main/images_demo/PROCESS_DIAGRAM_API.png)


La solucion planteada la defini desde un servidor HTTP simple en python3 creando este , tenemos un endpoint que se encuentra en la raiz de la direccion local , puerto 8000(se puede cambiar en caso de que tengan el puerto ocupado)
al realizar una solicitud de tipo GET al endpoint este a su vez ejecuta el llamado a la APIREST externa  https://rapidapi.com/apilayernet/api/rest-countries-v1  desde la cual esta misma cuenta con un endpoint el cual es :
>https://restcountries.com/v3.1/all  y luego se hace el llamado a los datos por region en el siguiente endpoint   https://restcountries.com/v3.1/region/{region}

este nos entrega toda la informacion de las regiones existentes(continentes) en este caso se procesa la informacion y solo se dejan las distintas regiones(conjunto)
luego de la solicitud GET desde el servidor HTTP hacia la API REST externa esta misma entrega una respuesta hacia el servidor HTTP nuevamente una vez el servidor procesa la informacion  genera un archivo en la ruta local del proyecto llamado data.json el cual contiene el resultado de los datos solicitados,posteriormente en esta parte del proceso a su vez se guardan las estadisticas de tiempo de procesamiento en milisegundos , esto en la base de datos SQLITE que es creada en la carpeta instance al ejecutar por primera vez el proyecto


luego de esto al punto inicial desde el que hicimos el llamado a nuestro servidor HTTP es decir desde nuestro navegador es devuelto en formato JSON los resultados del procesamiento de datos
se utilizo pandas para la manipulacion de las estadisticas generando un dataframe
Tambien adjunto en el presente repositorio el archivo del diagrama del diseño de la solucion generado desde draw.io
