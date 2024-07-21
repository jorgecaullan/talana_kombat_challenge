# Desafío Talana Kombat

Por Jorge Caullán

Este es un desafío propuesto por Talana para postular a trabajar como `Desarrollador Tech Lead`.

La verdad estaba bastante entretenido el desafío, le dediqué harto cariño y espero que con lo entregado, estar a la altura de lo que esperan 🙂.

## Ejecución

Para ejecutar el programa es fácil, solo debes usar:

`docker-compose up --build`

Al usar el comando, se correrán 3 componentes, uno para validar el linter, otro para validar los tests predefinidos, y el último para levantar una api en FastAPI.

Para acceder a la api, solo debes entrar desde un navegador a:

<http://localhost:8000/docs>

Donde deberás insertar la data del archivo JSON que prefieras.

## Ejecución unicamente de tests

Para la ejecución de los tests, solo es necesario usar:

`docker-compose up --build tests`

## Preguntas generales

### 1. Supongamos que en un repositorio GIT hiciste un commit y olvidaste un archivo. Explica cómo se soluciona si hiciste push, y cómo si aún no hiciste

(De ser posible, que quede solo un commit con los cambios.)

* En caso de ya haber hecho push, lo mejor seria hacer push de un segundo commit para evitar potenciales conflictos con otros desarrolladores.
* Sin embargo, también sé que existe la opción de hacer un `git commit --amend` (ya habiendo agregado el archivo con `git add {archivo}`) y luego un `git push --force`, pero esta opción solo la usaría si estoy trabajando en una rama propia y si no hay riesgo de que nadie mas pueda estar afectado ya que se modificará un commit ya subido.
* En caso de que aun no se haya hecho push, es fácil, solo se debe agregar el archivo con `git add {archivo}` y luego hacer un `git commit --amend` de la misma forma que antes pero sin el .

### 2. Si has trabajado con control de versiones ¿Cuáles han sido los flujos con los que has trabajado?

En mi trabajo anterior siempre se utilizó una version personalizada de Gitlab Flow. En la empresa siempre teníamos 4 ramas importantes, donde 3 de ellas estaban deployadas:

* **staging**: Deployada y usada unicamente como ambiente de pruebas, a la cual cualquier persona podia subir sus cambios en cualquier momento
* **develop**: No deployada, y usada para mantener código limpio antes de pasar a Beta. Se podia hacer push desde una rama unicamente después de que un Merge Request pasara por el Code Review y el QA. Todas las nuevas ramas debían salir desde `develop` (a excepción de los hotfix).
* **master**: Deployada y usada unicamente por nuestros clientes BetaTesters. Se consideraba un ambiente productivo al cual solo se podia hacer push desde la rama `develop` en releases, cuando se decidía sacar junto con las funcionalidades que estaban listas y probadas en develop.
* **production**: Deployada y usada por todo el resto de clientes finales. Era el ambiente más importante, al cual solo se podían hacer releases desde la rama de `master` en fechas y horarias previamente establecidas y habladas con los clientes.

Luego, además de esto, las otras ramas debían cumplir con el siguiente formato `prefijo/código`, donde:

* **prefijo**: podia ser `feature`, `enhancement`, `bugfix` o `hotfix`.
* **código**: el código de la plataforma de gestión donde se utilizara, en mi caso Jira.

Es decir, por ejemplo, para un feature del proyecto "talana" seria algo como: `feature/talana-123`

### 3. ¿Cuál ha sido la situación más compleja que has tenido con esto?

El principal problema **siempre** estaba en la rama staging, al ser una rama de pruebas, cuando alguien hacia push de una funcionalidad, la cual podia tener errores que afectaran de alguna forma funcionalidades de otros compañeros.

En algunas ocasiones, pasaba que alguien estaba haciendo un refactor de un archivo completo, y a la vez, otro compañero estaba cambiando detalles de la version antigua de mismo archivo, como resultado, cuando se hacia push a staging para probar los cambios, habían conflictos básicamente imposibles de resolver con una interfaz.

En estos casos, lo que debía hacerse es, definir una dependencia de funcionalidades. Por ejemplo, decir que la `funcionalidad1` debía depender de la `funcionalidad2` (o viceversa), por lo que `funcionalidad1` debía hacer pull de `funcionalidad2` cuando estuviera terminada, y entre ambos desarrolladores debían resolver los conflictos de cambios en la rama de `funcionalidad1`.

### 4. ¿Qué experiencia has tenido con los microservicios?

Tengo mucha experiencia trabajando con microservicios, básicamente en todos mis proyectos suelo usar microservicios, ya sea para escalar posibles cuellos de botella o para que nuevas funcionalidades sean independientes de otras.

En mi trabajo anterior, estuve trabajando en un proyecto llamado Dalca (una plataforma de gestión para radiólogos), el cual tenia al rededor de 40 microservicios, de los cuales, durante mis años de desarrollo ahí, yo me encargué de crear al menos unos 10 de ellos. Estos microservicios abarcaban diversas funcionalidades, desde la gestión de usuarios hasta la integración con hospitales externos.

### 5. ¿Cuál es tu servicio favorito de GCP o AWS? ¿Por qué?

En mi caso, tengo más preferencia y experiencia con GCP, donde el servicio que más me ha facilitado la vida es **Kubernetes**.

Al ser un fan de los microservicios, Kubernetes me aporta todo lo necesario para monitorear y trabajar con todos los microservicios en un único lugar, ya sea para escalarlos/des-escalarlos fácilmente o para ingresar al contenedor de algún servicio a revisar algo.

Además de Kubernetes, también me gusta mucho **Firebase/Authentication**, ya que el servicio tiene un costo extremadamente bajo, ayuda mucho con el escalamiento cuando se necesita tener muchos usuarios al mismo tiempo y es super fácil de implementar (al menos, es mas fácil que un servicio propio de usuarios).

Y por último, otro servicio de GCP que no se queda atrás es **Cloud Storage**, el cual también tiene un costo super bajo, ayuda un mundo con el escalamiento de información que debe leerse constantemente y se puede usar fácilmente para complementar Firebase/Authentication.
