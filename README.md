# Compilador Web — Taller Final de Compiladores

**Institución:** Corporación Universitaria Remington   
**Asignatura:** Compiladores 
**Integrantes:** Andres Stivens Cortes, Danny Alejandro Gallego, Eder Yesidt Arboleda
**Propósito:** Aplicación web modular que recibe código fuente escrito en el lenguaje y visualiza de manera secuencial y organizada cada una de las fases de **Análisis** y **Síntesis** de un compilador.

---

## 1. Descripción y Reglas del Lenguaje 

 es un lenguaje de programación imperativo, sencillo y fuertemente tipado (enteros `INT`), diseñado para evaluar expresiones aritméticas y asignaciones de variables.

### Elementos léxicos soportados
* **Identificadores (`ID`):** Nombres de variables que inician con una letra o guion bajo, seguidos de letras, números o guion bajo (ej. `x`, `total`, `num1`).
* **Literales numéricos (`NUMERO`):** Números enteros positivos (ej. `0`, `5`, `120`).
* **Operadores aritméticos:** Suma (`+`), resta (`-`), multiplicación (`*`) y división (`/`).
* **Operador de asignación:** Igual (`=`).
* **Delimitadores:** Paréntesis de apertura `(`, paréntesis de cierre `)` y punto y coma `;` como terminador obligatorio de instrucción.

### Reglas gramaticales y semánticas
1. Toda sentencia debe tener la estructura: `<ID> = <EXPRESION> ;`
2. Se respeta la jerarquía estándar de operadores: primero paréntesis `()`, luego multiplicación/división (`*`, `/`) y finalmente suma/resta (`+`, `-`).
3. **Declaración previa:** Toda variable utilizada en una expresión debe haber sido declarada e inicializada en una instrucción anterior.
4. **Control de errores:** No se permiten divisiones literales por cero ni caracteres ajenos al alfabeto del lenguaje.

---

## 2. Arquitectura del Proyecto

El proyecto sigue una arquitectura **Cliente-Servidor modular**, separando completamente la interfaz gráfica (**Frontend**) de la lógica de compilación (**Backend**):

```text
compilador/
│
├── backend/                  # Lógica del compilador y API REST (Python + Flask)
│   ├── app.py                # Servidor HTTP y endpoint /compilar
│   ├── orquestador.py        # Controlador secuencial y manejo de parada ante errores
│   ├── lexico.py             # Fase 1: Análisis Léxico
│   ├── sintactico.py         # Fase 2: Análisis Sintáctico (AST)
│   ├── semantico.py          # Fase 3: Análisis Semántico y Tabla de Símbolos
│   ├── intermedio.py         # Fase 4: Generación de Código de Tres Direcciones (TAC)
│   ├── optimizador.py        # Fase 5: Optimización de Código
│   └── destino.py            # Fase 6: Generación de Código Ensamblador
│
├── frontend/                 # Interfaz web independiente (HTML5, CSS3, JavaScript)
│   ├── index.html            # Estructura de entrada y tarjetas por fase
│   ├── styles.css            # Estilos visuales e indicadores de estado
│   └── script.js             # Consumo de la API y renderizado de resultados
│
└── README.md                 # Documentación oficial del proyecto
```

---

## 3. Fases Implementadas

### A. Fases de Análisis
1. **Análisis Léxico (`lexico.py`):** Escanea el código fuente mediante expresiones regulares, ignora espacios en blanco y clasifica cada lexema en tokens (`ID`, `NUMERO`, `SUMA`, `ASIGNACION`, etc.). Detecta símbolos inválidos.
2. **Análisis Sintáctico (`sintactico.py`):** Implementa un analizador **Descendente Recursivo** que verifica el cumplimiento de la gramática y construye un Árbol de Sintaxis Abstracta (AST) en formato JSON respetando la precedencia de operadores.
3. **Análisis Semántico (`semantico.py`):** Recorre el AST construyendo una **Tabla de Símbolos**, validando que toda variable sea declarada antes de su uso, verificando la compatibilidad de tipos (`INT`) y previniendo divisiones entre cero.

### B. Fases de Síntesis
4. **Generación de Código Intermedio (`intermedio.py`):** Traduce el AST mediante recorrido en post-orden a **Código de Tres Direcciones (TAC)** utilizando variables temporales (`t1`, `t2`, ...).
5. **Optimización de Código (`optimizador.py`):** Aplica cuatro técnicas de optimización sobre el código intermedio:
   * *Propagación de constantes*
   * *Plegado de constantes (Constant Folding)*
   * *Simplificación algebraica* (`x + 0`, `x * 1`, `x * 0`, `x / 1`)
   * *Eliminación de código muerto* (descarte de variables temporales sin uso)
6. **Generación de Código Destino (`destino.py`):** Traduce el código optimizado a ensamblador para una **Arquitectura RISC Hipotética de 32 bits con Registros Generales (`R1..Rn`)**, empleando instrucciones `MOV`, `LOAD`, `ADD`, `SUB`, `MUL`, `DIV`, `STORE` y `HALT`.

> **Manejo de errores:** Si ocurre un fallo en cualquiera de las fases, el sistema detiene inmediatamente el flujo de compilación, identifica la fase exacta del error y muestra un mensaje descriptivo sin ejecutar las fases posteriores.

---

## 4. Instrucciones de Instalación y Ejecución

### Requisitos previos
* Tener instalado **Python 3.10 o superior**.
* Navegador web moderno (Chrome, Edge, Firefox).

### Paso 1: Instalar dependencias del Backend
Abra una terminal en la carpeta raíz del proyecto y ejecute:
```bash
pip install flask flask-cors
```

### Paso 2: Iniciar el servidor Backend
En la terminal, ejecute el servidor de Python:
```bash
python backend/app.py
```
El servidor quedará escuchando en `http://127.0.0.1:5000`.

### Paso 3: Ejecutar el Frontend
1. Navegue a la carpeta `frontend/`.
2. Abra el archivo `index.html` con doble clic en su navegador web.
3. Ingrese código fuente (o use los botones de ejemplos precargados) y presione **Compilar Código**.

---

## 5. Casos de Prueba Sugeridos

| Caso de Prueba | Código Fuente | Resultado Esperado |
| :--- | :--- | :--- |
| **Compilación Exitosa** | `a = 10;`<br>`b = a + 5 * 2;` | Completa las 6 fases y genera el ensamblador correspondiente. |
| **Optimización Completa** | `x = 5 + 3 * 0;`<br>`y = x * 1 + 4;` | Reduce expresiones mediante plegado, simplificación algebraica, propagación y elimina temporales muertos (`x = 5`, `y = 9`). |
| **Error Léxico** | `x = 10 @ 2;` | Se detiene en **Fase 1** indicando carácter `@` no válido. |
| **Error Sintáctico** | `x = 10 + 2` | Se detiene en **Fase 2** indicando falta de `;` al final. |
| **Error Semántico** | `x = z + 5;` | Se detiene en **Fase 3** indicando que la variable `z` no ha sido declarada. |