def analizar_sintactico(tokens):
    # Variable para llevar la cuenta de qué token estamos mirando actualmente
    posicion = 0

    # Función auxiliar para mirar el token actual sin avanzar
    def token_actual():
        if posicion < len(tokens):
            return tokens[posicion]
        return None

    # Función auxiliar para consumir un token esperado y avanzar al siguiente
    def consumir(tipo_esperado):
        nonlocal posicion
        actual = token_actual()
        if actual and actual["tipo"] == tipo_esperado:
            posicion += 1
            return actual
        return None

    # --- REGLAS DE LA GRAMÁTICA (Descenso Recursivo) ---

    # Nivel 3 (Mayor prioridad): Números, Variables o Paréntesis
    def factor():
        actual = token_actual()
        if not actual:
            raise SyntaxError("Error Sintáctico: Se esperaba un número, variable o '(' pero el código terminó de repente.")

        if actual["tipo"] == "NUMERO":
            consumir("NUMERO")
            return {"nodo": "NUMERO", "valor": int(actual["valor"])}
        
        elif actual["tipo"] == "ID":
            consumir("ID")
            return {"nodo": "VARIABLE", "nombre": actual["valor"]}
        
        elif actual["tipo"] == "PAR_IZQ":
            consumir("PAR_IZQ")
            nodo_interno = expresion() # Resuelve lo que está dentro del paréntesis
            if not consumir("PAR_DER"):
                raise SyntaxError("Error Sintáctico: Falta cerrar un paréntesis ')'.")
            return nodo_interno
        
        else:
            raise SyntaxError(f"Error Sintáctico: No se esperaba '{actual['valor']}' aquí. Se esperaba un número o variable.")

    # Nivel 2 (Prioridad media): Multiplicación (*) y División (/)
    def termino():
        nodo = factor()
        while token_actual() and token_actual()["tipo"] in ("MULT", "DIV"):
            operador = token_actual()["valor"]
            consumir(token_actual()["tipo"])
            derecho = factor()
            nodo = {
                "nodo": "OPERACION",
                "operador": operador,
                "izquierda": nodo,
                "derecha": derecho
            }
        return nodo

    # Nivel 1 (Menor prioridad): Suma (+) y Resta (-)
    def expresion():
        nodo = termino()
        while token_actual() and token_actual()["tipo"] in ("SUMA", "RESTA"):
            operador = token_actual()["valor"]
            consumir(token_actual()["tipo"])
            derecho = termino()
            nodo = {
                "nodo": "OPERACION",
                "operador": operador,
                "izquierda": nodo,
                "derecha": derecho
            }
        return nodo

    # Regla principal de una línea: variable = expresion ;
    def sentencia():
        id_token = consumir("ID")
        if not id_token:
            actual = token_actual()
            raise SyntaxError(f"Error Sintáctico: Toda instrucción debe iniciar con una variable, no con '{actual['valor']}'.")

        if not consumir("ASIGNACION"):
            actual = token_actual()
            val = actual['valor'] if actual else "fin de línea"
            raise SyntaxError(f"Error Sintáctico: Se esperaba '=' después de la variable '{id_token['valor']}', pero se encontró '{val}'.")

        arbol_expresion = expresion()

        if not consumir("PUNTO_COMA"):
            actual = token_actual()
            val = actual['valor'] if actual else "el final"
            raise SyntaxError(f"Error Sintáctico: Falta ';' al final de la instrucción (antes de '{val}').")

        return {
            "nodo": "ASIGNACION",
            "variable": id_token["valor"],
            "expresion": arbol_expresion
        }

    # --- EJECUCIÓN DEL ANÁLISIS ---
    arbol_sintactico = []
    try:
        while posicion < len(tokens):
            arbol_sintactico.append(sentencia())
        
        return {
            "exito": True,
            "arbol": arbol_sintactico,
            "mensaje": f"Sintaxis correcta. Se validaron {len(arbol_sintactico)} instrucción(es)."
        }
    except SyntaxError as e:
        return {
            "exito": False,
            "error": str(e)
        }