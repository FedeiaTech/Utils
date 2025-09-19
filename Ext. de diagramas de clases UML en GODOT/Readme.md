# 🤖 GDScript UML Generator V 1.0

### **Autor: Fedeia.dev**

Este es un script de Python que genera automáticamente un diagrama de clases UML (Lenguaje Unificado de Modelado) a partir de tus archivos GDScript en un proyecto de Godot. Analiza tu código para encontrar clases, atributos, métodos, señales, herencia y dependencias. El diagrama se genera en formato PlantUML, listo para ser visualizado.

---

### **🚀 Cómo usar el código**

#### **Opción 1: Descargar y usar el ejecutable**

Si no quieres instalar Python, puedes descargar el archivo ejecutable (`gdscript_uml.exe` para Windows o `gdscript_uml` para macOS/Linux) que se encuentra en la sección de "Releases" del repositorio.

1.  **Coloca el ejecutable** en la carpeta principal de tu proyecto de Godot.
2.  **Abre una terminal** o línea de comandos en esa misma carpeta.
3.  **Ejecuta el archivo** con el comando:

    ```bash
    ./gdscript_uml
    ```

    El script creará un archivo llamado `diagrama.puml` en la misma carpeta.

#### **Opción 2: Ejecutar el script de Python**

Si prefieres usar el script directamente, sigue estos pasos:

1.  **Asegúrate de tener Python instalado** en tu computadora. Puedes verificarlo con el comando `python --version`. Si no lo tienes, descárgalo e instálalo desde [python.org](https://www.python.org/).
2.  **Copia el código** del script Python en un archivo nuevo y guárdalo como `gdscript_uml.py` dentro de la carpeta principal de tu proyecto de Godot.
3.  **Abre una terminal** y navega hasta esa carpeta.
4.  **Ejecuta el script** con el siguiente comando:

    ```bash
    python gdscript_uml.py
    ```

    Al igual que con el ejecutable, se creará un archivo `diagrama.puml` con el código del diagrama.

---

### **✨ Visualiza tu diagrama**

El archivo `diagrama.puml` es solo un texto. Para ver el diagrama, necesitas un visor de PlantUML.

1.  **Copia todo el contenido** del archivo `diagrama.puml`.
2.  **Pégalo en un visor en línea** como el [visor oficial de PlantUML](http://www.plantuml.com/plantuml/uml/).
3.  Si usas un editor como **Visual Studio Code**, puedes instalar la extensión "PlantUML" para ver el diagrama en tiempo real.

---

### **⚠️ Limitaciones**

Es importante tener en cuenta que el script utiliza un análisis de texto rudimentario. Aunque es muy preciso, tiene algunas limitaciones:

* **Composición y Agregación**: No puede distinguir entre estas relaciones. Ambas se representarán como una simple **dependencia** (`.>`).
* **Polimorfismo y Cargas Dinámicas**: El script no detecta relaciones que se crean de forma dinámica en tiempo de ejecución.
* **Multiplicidad**: No puede inferir si una relación es de uno a uno, de uno a muchos, etc.
* **Nodos y `$**`: Las referencias a nodos mediante la ruta (`$Player/`) no se analizan como dependencias. La detección se basa únicamente en llamadas a métodos (`.`) entre clases.