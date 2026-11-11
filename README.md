# [NOMBRE DEL ALUMNO]

**Matrícula:** 125052638  
**Alumno**: Hernández Huerta Ari Leonardo
**Grupo:** IDIA222  
**Materia:** Manejo Masivo de Datos  
**Profesor:** Jose Javier Moya Moya  
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
git clone <URL_DEL_REPOSITORIO>
```

Ingresar al proyecto:

```bash
cd <nombre_del_proyecto>
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
-input /data/input/ventas_125052638.csv \
-output /data/output/resultado \
-mapper "python3 mapper.py" \
-reducer "python3 reducer.py" \
-file mapper.py \
-file reducer.py
```

### Resultado obtenido

```text
real 1m21.531s
```

---

## Conclusión de rendimiento

En este escenario, Hadoop Streaming obtuvo un tiempo ligeramente menor (1m21.531s) que la solución secuencial (1m26.295s). Esto se debe a que el procesamiento se realizó mediante las fases Map y Reduce, distribuyendo el trabajo de agregación. Sin embargo, la diferencia fue pequeña porque el volumen de datos aún es relativamente moderado y se ejecutó sobre una sola máquina. A medida que aumentan el tamaño del dataset y la cantidad de nodos disponibles, Hadoop suele mostrar ventajas más significativas frente a una solución secuencial.

---

# Verificación de resultados Hadoop

Comprobar archivos generados:

```bash
ls /data/output/resultado
```

Se deben observar:

```text
_SUCCESS
part-00000
```

Visualizar resultados:

```bash
head /data/output/resultado/part-00000
```

---

# Carga de resultados a PostgreSQL

Entrar al contenedor API:

```bash
docker exec -it api_crud bash
```

Ejecutar:

```bash
python3 /workspace/scripts/cargar_resultados.py /data/output/resultado/part-00000
```

---

# Validación mediante API REST

Abrir el navegador:

```text
http://127.0.0.1:5000/resultados
```

La API debe devolver los resultados almacenados en PostgreSQL en formato JSON.

---

# Preguntas teóricas

## 1. Explica la diferencia entre los modos standalone, pseudo-distribuido y totalmente distribuido de Hadoop. ¿En cuál de ellos se usa HDFS?

**Standalone:** Hadoop se ejecuta como una aplicación local sin demonios ni servicios distribuidos. Se utiliza principalmente para pruebas y desarrollo.

**Pseudo-distribuido:** Todos los servicios Hadoop se ejecutan en una sola máquina, pero cada demonio funciona como un proceso independiente. Permite probar el comportamiento distribuido sin necesidad de varios equipos.

**Totalmente distribuido:** Hadoop se instala en múltiples nodos físicos o virtuales conectados por red. Cada servicio puede ejecutarse en máquinas distintas.

**HDFS** se utiliza en los modos **pseudo-distribuido** y **totalmente distribuido**.

---

## 2. ¿Por qué el dataset se monta como volumen y no se copia dentro de la imagen con COPY? Menciona al menos dos razones.

Montar el dataset como volumen permite cambiar o regenerar el archivo sin reconstruir la imagen Docker. Además, evita incorporar archivos grandes al repositorio y a las imágenes, reduciendo el tamaño de estas. También facilita compartir el mismo dataset entre distintos contenedores y conservar la separación entre código y datos.

---

## 3. ¿Qué ocurre con los datos de la base de datos al ejecutar docker compose down? ¿Y con docker compose down -v?

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