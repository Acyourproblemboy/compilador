def generar_codigo_intermedio(arbol_sintactico):
    contador_temporales = 1
    instrucciones_tac = []  # Lista de diccionarios (para que el optimizador la lea fácil)
    codigo_texto = []       # Lista de textos (para mostrar bonito en la página web)

    # Función para crear nombres de variables temporales: t1, t2, t3...
    def nuevo_temporal():
        nonlocal contador_temporales
        nombre = f"t{contador_temporales}"
        contador_temporales += 1
        return nombre

    # Función recursiva que desarma el árbol de abajo hacia arriba
    def recorrer_expresion(nodo):
        tipo = nodo["nodo"]

        if tipo == "NUMERO":
            return str(nodo["valor"])

        elif tipo == "VARIABLE":
            return nodo["nombre"]

        elif tipo == "OPERACION":
            # Primero resolvemos el lado izquierdo y el lado derecho
            izq = recorrer_expresion(nodo["izquierda"])
            der = recorrer_expresion(nodo["derecha"])
            operador = nodo["operador"]

            # Creamos una variable temporal para guardar esta operación individual
            temp = nuevo_temporal()

            instrucciones_tac.append({
                "tipo": "OPERACION",
                "destino": temp,
                "izq": izq,
                "operador": operador,
                "der": der
            })
            codigo_texto.append(f"{temp} = {izq} {operador} {der}")

            return temp

    # --- GENERACIÓN PARA CADA LÍNEA DEL PROGRAMA ---
    for sentencia in arbol_sintactico:
        resultado = recorrer_expresion(sentencia["expresion"])
        variable_destino = sentencia["variable"]

        instrucciones_tac.append({
            "tipo": "ASIGNACION",
            "destino": variable_destino,
            "valor": resultado
        })
        codigo_texto.append(f"{variable_destino} = {resultado}")

    return {
        "exito": True,
        "instrucciones": instrucciones_tac,
        "codigo_texto": codigo_texto,
        "mensaje": f"Código de tres direcciones generado ({len(codigo_texto)} instrucciones)."
    }