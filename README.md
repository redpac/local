1. REQUISITOS
==============================================================================
* Una computadora con Windows, macOS o Linux.
* Python 3.10 o posterior.
* Los archivos requirements.txt, messenger.py, chat_basico.ui, chat_basico_ui.py, conectar.ui, conectar_ui.py, crear.ui y crear_ui.py

2. INSTALAR PYTHON
==============================================================================
WINDOWS
-------------------------------------------------------------------------------
1. Descarga Python desde https://www.python.org/downloads/windows/
2. Ejecuta el instalador.
3. Marca obligatoriamente "Add python.exe to PATH".
4. Finaliza la instalación.
Comprueba la instalación desde CMD o PowerShell:
    python --version
    pip --version

macOS
-------------------------------------------------------------------------------
La forma más sencilla es instalar Python desde:
https://www.python.org/downloads/macos/
Otra opcion es usar Homebrew:
    brew install python
Comprueba la instalación desde Terminal:
    python3 --version
    pip3 --version

GNU/LINUX
-------------------------------------------------------------------------------
En Ubuntu o Debian:
    sudo apt update
    sudo apt install python3 python3-pip python3-venv
En otras distribuciones, usa su administrador de paquetes para instalar
python3, pip y el módulo de entorno virtual.
Comprueba:
    python3 --version
    pip3 --version

3. PREPARAR EL PROYECTO
==============================================================================
Abre una terminal dentro de la carpeta que contiene messenger.py.
Windows - PowerShell o CMD:
    cd ruta\al\proyecto
macOS o Linux - Terminal:
    cd ruta/al/proyecto
Para verificar los archivos:
    ls
Debes encontrar al menos:
* messenger.py
* principal.ui
* principal_ui.py
* conectar.ui
* conectar_ui.py
* crear.ui
* crear_ui.py
* requirements.txt
* src/ -- images

4. CREAR Y ACTIVAR UN ENTORNO VIRTUAL (o no, cada quien vdd)
==============================================================================
Un entorno virtual evita conflictos entre dependencias de distintos proyectos.

WINDOWS
-------------------------------------------------------------------------------
Crear:
    python -m venv .venv
Activar con PowerShell:
    .venv\Scripts\Activate.ps1
Si PowerShell bloquea scripts, usa CMD:
    .venv\Scripts\activate.bat

macOS / LINUX
-------------------------------------------------------------------------------
Crear:
    python3 -m venv .venv
Activar:
    source .venv/bin/activate
Cuando el entorno esté activo, la terminal mostrará normalmente:
    (.venv)
Para salir:
    deactivate

5. INSTALAR DEPENDENCIAS
==============================================================================
Con el entorno virtual activo (o no, cada quien vdd):

WINDOWS
-------------------------------------------------------------------------------
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

macOS / LINUX
-------------------------------------------------------------------------------
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt

6. EJECUTAR EL CLIENTE
==============================================================================
WINDOWS
-------------------------------------------------------------------------------
    python messenger.py

macOS / LINUX
-------------------------------------------------------------------------------
    python3 messenger.py
Si aparece un error de bibliotecas gráficas en Linux, instala los componentes
Qt correspondientes con el administrador de paquetes de tu distribución.
Para Ubuntu/Debian es frecuente necesitar:
    sudo apt install libxcb-cursor0
En macOS, si Python procede de python.org y PySide6 no inicia, verifica que
el entorno virtual esté activo y que pip haya instalado PySide6 dentro de
ese entorno.

==============================================================================

El proyecto sigue la arquitectura cliente-servidor:

    [messenger.py]  <---- TCP texto plano ---->  [server.py]
          |                                          |
          |                                      [database.py]
          |                                          |
          +------ PySide6: interfaz gráfica          +---- SQL Server

1. messenger.py
   Contiene la interfaz gráfica y el hilo de conexión. Convierte respuestas
   recibidas desde el servidor en eventos Qt para mostrarlas en pantalla.

2. server.py
   Acepta conexiones TCP, identifica a cada usuario autenticado y procesa
   comandos enviados como texto. Aplica reglas de autoría, suscripción y
   pertenencia a grupos o canales.

3. database.py
   Centraliza todas las operaciones SQL. Los demás archivos no ejecutan
   sentencias SQL directamente.

La comunicación no usa JSON. Usa protocolos basados en prefijos y doble guion:

    Comando sin datos:
        --retrieveGroup

    Comando con datos:
        --retrieveGroup--15--

    Respuesta del servidor:
        --group--15--Nombre del grupo--

La doble terminación "--" indica el inicio y fin de campos delimitados. Para
comandos que no llevan datos, no debe añadirse "--" al final.
