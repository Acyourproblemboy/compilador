def analizar_semantico(arbol_sintactico):
    # La Tabla de Símbolos guardará las variables declaradas y su información
    # Ejemplo: {"x": {"tipo": "INT", "declarada_en_linea": 1}}
    tabla_simbolos = {}

    # Función recursiva para revisar cada pedazo de la operación matemática
    def validar_expresion(nodo, linea):
        tipo_nodo = nodo["nodo"]

        if tipo_nodo == "NUMERO":
            return "INT"  # Todos los números en MiniLang son enteros (INT)

        elif tipo_nodo == "VARIABLE":
            nombre = nodo["nombre"]
            # Regla 1: ¿La variable ya existe en nuestra libreta (Tabla de Símbolos)?
            if nombre not in tabla_simbolos:
                raise ValueError(
                    f"Error Semántico (Línea {linea}): La variable '{nombre}' se está usando antes de ser declarada."
                )
            return tabla_simbolos[nombre]["tipo"]

        elif tipo_nodo == "OPERACION":
            tipo_izq = validar_expresion(nodo["izquierda"], linea)
            tipo_der = validar_expresion(nodo["derecha"], linea)

            # Regla 2: Compatibilidad de tipos
            if tipo_izq != "INT" or tipo_der != "INT":
                raise ValueError(
                    f"Error Semántico (Línea {linea}): Tipos incompatibles para el operador '{nodo['operador']}'."
                )

            # Regla 3: Evitar división literal por cero
            if nodo["operador"] == "/" and nodo["derecha"]["nodo"] == "NUMERO" and nodo["derecha"]["valor"] == 0:
                raise ValueError(
                    f"Error Semántico (Línea {linea}): División por cero no permitida."
                )

            return "INT"

    # --- RECORRIDO DE TODAS LAS INSTRUCCIONES ---
    try:
        for numero_linea, sentencia in enumerate(arbol_sintactico, start=1):
            # Primero validamos el lado derecho del '=' (la operación)
            # Ojo: Hacemos esto ANTES de registrar la variable izquierda, para atrapar errores como: x = x + 1; si 'x' no existía
            tipo_resultado = validar_expresion(sentencia["expresion"], numero_linea)

            # Ahora sí registramos o actualizamos la variable en la Tabla de Símbolos
            nombre_var = sentencia["variable"]
            tabla_simbolos[nombre_var] = {
                "tipo": tipo_resultado,
                "linea_declaracion": numero_linea,
                "estado": "Inicializada"
            }

        return {
            "exito": True,
            "tabla_simbolos": tabla_simbolos,
            "mensaje": f"Análisis semántico exitoso. {len(tabla_simbolos)} variable(s) registrada(s) en la Tabla de Símbolos."
        }

    except ValueError as e:
        return {
            "exito": False,
            "error": str(e)
        }