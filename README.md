# [NOMBRE DEL ALUMNO]

**Matrícula:** 125052638  
**Nombre del alumno**: Hernández Huerta Ari Leonardo
**Grupo:** IDIA222  
**Materia:** Manejo Masivo de Datos  
**Profesor:** José Javier Moya Moya  
**Fecha:** 09/11/2026  

---

# Práctica: Hadoop Streaming, Docker, PostgreSQL y API REST

## Información general

La práctica consiste en construir una solución de procesamiento de datos utilizando contenedores Docker, Hadoop Streaming, PostgreSQL y una API REST en Python para responder una pregunta de negocio asignada según la matrícula.

### Matrícula

125052638

### Pregunta de negocio asignada

> ¿Cuál es el ingreso total por hora del día (0-23) y categoría de producto?

### Tamaño aproximado del dataset

El dataset generado contiene aproximadamente 148,000 registros de ventas distribuidos a lo largo de todo el año 2025, incluyendo información de fecha, hora, categoría, producto, cantidad vendida, precio unitario y método de pago.

---

# Herramientas utilizadas

- Docker Desktop
- Visual Studio Code (recomendado)
- Git
- Python 3
- Hadoop 3.3.6
- OpenJDK 17
- PostgreSQL
- Flask
- Conexión a Internet estable

---

# Arquitectura de la solución

```text
ventas_125052638.csv
            |
            v
      Hadoop Streaming
    mapper.py + reducer.py
            |
            v
        part-00000
            |
            v
   cargar_resultados.py
            |
            v
        PostgreSQL
            |
            v
         API Flask
            |
            v
  http://localhost:5000/resultados
```

---

# Procedimiento de reproducción

## 1. Clonar el repositorio

```bash
git clone <https://github.com/AriLeo-droid/Examen-Parcial2>
```

Ingresar al proyecto:

```bash
cd <Examen-Parcial2>
```

---

## 2. Generar el dataset

Ejecutar de forma nativa:

```bash
python generar_dataset.py
```

Introducir la matrícula:

```text
125052638
```

Esto generará:

```text
ventas_125052638.csv
```

---

## 3. Construcción limpia de contenedores

Detener cualquier instancia previa:

```bash
docker compose down
```

Construir y levantar:

```bash
docker compose up --build -d
```

Verificar:

```bash
docker ps
```

---

# Verificación del entorno Hadoop

Entrar al contenedor:

```bash
docker exec -it hadoop bash
```

Verificar Hadoop:

```bash
hadoop version
```

Verificar Java:

```bash
java -version
```

Verificar sistema operativo:

```bash
cat /etc/os-release
```

Verificar variables:

```bash
echo $JAVA_HOME
```

```bash
echo $HADOOP_HOME
```

```bash
echo $PATH
```

---

# Configuración SSH

## Acceso local en Hadoop

Cambiar al usuario Hadoop:

```bash
su - hadoop
```

Verificar usuario:

```bash
whoami
```

Verificar llaves:

```bash
ls -la ~/.ssh
```

Verificar servicio SSH:

```bash
ps aux | grep sshd
```

Realizar prueba:

```bash
ssh localhost
```

Aceptar la huella digital cuando se solicite:

```text
yes
```

La conexión debe realizarse sin solicitar contraseña.

---

## Acceso API → Hadoop

Entrar al contenedor API:

```bash
docker exec -it api_crud bash
```

Verificar llaves:

```bash
ls -la ~/.ssh
```

Si no existen:

```bash
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
```

Copiar la clave pública:

```bash
cat ~/.ssh/id_rsa.pub
```

Entrar nuevamente a Hadoop:

```bash
docker exec -it hadoop bash
```

```bash
su - hadoop
```

Agregar la clave al archivo:

```bash
echo "PEGAR_AQUI_CLAVE_PUBLICA" >> ~/.ssh/authorized_keys
```

Ajustar permisos:

```bash
chmod 700 ~/.ssh
```

```bash
chmod 600 ~/.ssh/authorized_keys
```

Volver al contenedor API:

```bash
docker exec -it api_crud bash
```

Probar la conexión:

```bash
ssh hadoop@hadoop
```

La conexión debe realizarse sin solicitar contraseña.

---

# Implementación MapReduce

## Verificación de scripts

Ir al directorio:

```bash
cd /workspace/mapreduce
```

Verificar:

```bash
ls
```

Deben mostrarse:

```text
mapper.py
reducer.py
secuencial.py
```

---

## Prueba local Mapper + Reducer

```bash
head -200 /data/input/ventas_125052638.csv | python3 mapper.py | sort | python3 reducer.py
```

Esta prueba valida el correcto funcionamiento de los scripts antes de ejecutar Hadoop Streaming.

---

# Comparativa de rendimiento (C2)

## Procesamiento secuencial

Ejecutar:

```bash
time python3 secuencial.py /data/input/ventas_125052638.csv
```

### Resultado obtenido

```text
real 1m26.295s
```

---

## Hadoop Streaming

Eliminar resultados previos:

```bash
rm -rf /data/output/resultado
```

Ejecutar:

```bash
time hadoop jar \
$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-input /data/input/ventas_1*5052638.csv \
-output /data/output*resultado \
-mapper "python3 mappe*.py" \
-reducer "python3 reducer.p*" \
-file mapper.py \
-file reduce*.py
```

### Resultado obtenido

`*`text
real 1m21.531s
```

---

## *onclusión de rendimiento

En este *scenario, Hadoop Streaming obtuvo *n tiempo ligeramente menor (1m21.5*1s) que la solución secuencial*(1m26.295s). Esto se debe*a que el procesamiento se*realizó mediante las fases Map y R*duce, distribuyendo el trabajo de *gregación. Sin embargo, la diferen*ia fue pequeña porque el volumen d* datos aún es relativamente modera*o y se ejecutó sobre una sola máqu*na. A medida que aumentan el tamañ* del dataset y la cantidad de nodo* disponibles, Hadoop suele mostrar*ventajas más significativas frente*a una solución secuencial.

---

#*Verificación de resultados Hadoop
*Comprobar archivos generados:

```*ash
ls /data/output/resultado
```
*Se deben observar:

```text
_SUCCE*S
part-00000
```

Visualizar resul*ados:

```bash
head /data/output/r*sultado/part-00000
```

---

# Car*a de resultados a PostgreSQL

Entr*r al contenedor API:

```bash
dock*r exec -it api_crud bash
```

Ejec*tar:

```bash
python3 /workspace/s*ripts/cargar_resultados.py /data/o*tput/resultado/part-00000
```

---*
# Validación mediante API REST

A*rir el navegador:

```text
http://127.0.0.1:5000/resultados
```

La A*I debe devolver los resultados alm*cenados en PostgreSQL en formato J*ON.

---

# Preguntas teóricas

##*1. Explica la diferencia entre los*modos standalone, pseudo-distribui*o y totalmente distribuido de Hado*p. ¿En cuál de ellos se usa HDFS?
***Standalone:** Hadoop se ejecuta *omo una aplicación local sin demon*os ni servicios distribuidos. Se u*iliza principalmente para pruebas * desarrollo.

**Pseudo-distribuido*** Todos los servicios Hadoop se e*ecutan en una sola máquina, pero c*da demonio funciona como un proces* independiente. Permite probar el *omportamiento distribuido sin nece*idad de varios equipos.

**Totalme*te distribuido:** Hadoop se instal* en múltiples nodos físicos o virt*ales conectados por red. Cada serv*cio puede ejecutarse en máquinas d*stintas.

**HDFS** se utiliza en l*s modos **pseudo-distribuido** y **totalmente distribuido**.

---

##*2. ¿Por qué el dataset se monta co*o volumen y no se copia dentro de *a imagen con COPY? Menciona al men*s dos razones.

Montar el dataset *omo volumen permite cambiar o rege*erar el archivo sin reconstruir la*imagen Docker. Además, evita incor*orar archivos grandes al repositor*o y a las imágenes, reduciendo el *amaño de estas. También facilita c*mpartir el mismo dataset entre dis*intos contenedores y conservar la *eparación entre código y datos.

-*-

## 3. ¿Qué ocurre con los datos*de la base de datos al ejecutar do*ker compose down? ¿Y con docker compose down -v?

Al ejecutar **docker compose down**, los contenedores son eliminados, pero los volúmenes persistentes permanecen, por lo que los datos de PostgreSQL se conservan. En cambio, **docker compose down -v** elimina también los volúmenes asociados, provocando la pérdida de los datos almacenados en ellos.

---

## 4. ¿Por qué MapReduce no siempre es más rápido que un script secuencial con un archivo de 400 MB? ¿A partir de qué condiciones conviene?

MapReduce introduce costes adicionales asociados a la creación de procesos, comunicación entre etapas, ordenación de claves y coordinación del framework. Para archivos relativamente pequeños, esa sobrecarga puede superar el beneficio de la paralelización. MapReduce resulta más conveniente cuando se trabaja con volúmenes de datos muy grandes o cuando el procesamiento se distribuye entre múltiples nodos.

---

## 5. Diferencia entre CMD y ENTRYPOINT, y entre COPY y ADD.

**CMD** define el comando por defecto que se ejecutará al iniciar un contenedor y puede ser sustituido fácilmente al lanzarlo. **ENTRYPOINT** establece el ejecutable principal del contenedor y se utiliza cuando se desea que siempre se ejecute el mismo programa.

**COPY** copia archivos y carpetas desde el host al contenedor de manera directa. **ADD** realiza la misma función, pero además puede extraer archivos comprimidos y soportar fuentes remotas, por lo que tiene un comportamiento más amplio.

---

# Bibliografía

- Apache Hadoop Documentation: https://hadoop.apache.org/docs/
- Hadoop Streaming Documentation: https://hadoop.apache.org/docs/current/hadoop-streaming/HadoopStreaming.html
- Docker Documentation: https://docs.docker.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Flask Documentation: https://flask.palletsprojects.com/
- OpenJDK Documentation: https://openjdk.org/
- Git Documentation: https://git-scm.com/doc

---

**Fin del documento.**