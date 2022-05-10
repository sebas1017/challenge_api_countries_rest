URL=127.0.0.1:8000

FILE=./../instance/tangelo_challenge.sqlite

RESULT=$(curl --write-out "%{http_code}\n" --silent --output /dev/null "$URL")

A=$( printf $RESULT )


if [ "$A" -eq 200 ]; then
  echo "TEST 100%"
  echo "VERIFICANDO SI EL PROYECTO CREO LA BASE DE DATOS..."
  if [ -f "$FILE" ]; then
    echo "$FILE exists."
    echo "EL PROYECTO CREO LA BASE DE DATOS CORRECTAMENTE..."
  else
    echo "EL PROYECTO NO CREO LA BASE DE DATOS CORRECTAMENTE..."
fi
else
  echo "API externa fallo , ejecutar nuevamente"
fi


