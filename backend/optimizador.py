def optimizar_codigo(instrucciones_tac):
    # Hacemos una copia para no alterar los datos originales de la Fase 4
    codigo = [inst.copy() for inst in instrucciones_tac]
    registro_tecnicas = []  # Aquí anotaremos qué optimizaciones se lograron

    def es_numero(valor):
        return valor.lstrip('-').isdigit()

    # Ejecutamos dos pasadas para que una optimización alimente a la siguiente
    for _ in range(2):
        constantes_conocidas = {}  # Ej: {"t1": "6", "a": "5"}
        nuevo_codigo = []

        for inst in codigo:
            if inst["tipo"] == "OPERACION":
                izq = inst["izq"]
                der = inst["der"]
                op = inst["operador"]
                dest = inst["destino"]

                # 1. PROPAGACIÓN DE CONSTANTES: Reemplazar variables con valor fijo conocido
                if izq in constantes_conocidas:
                    izq = constantes_conocidas[izq]
                    registro_tecnicas.append(f"Propagación de constantes: '{inst['izq']}' reemplazado por {izq}")
                if der in constantes_conocidas:
                    der = constantes_conocidas[der]
                    registro_tecnicas.append(f"Propagación de constantes: '{inst['der']}' reemplazado por {der}")

                # 2. PLEGADO DE CONSTANTES: Si ambos son números, calcular de una vez
                if es_numero(izq) and es_numero(der):
                    n1, n2 = int(izq), int(der)
                    if op == "+": res = n1 + n2
                    elif op == "-": res = n1 - n2
                    elif op == "*": res = n1 * n2
                    elif op == "/":
                        if n2 == 0:
                            return {"exito": False, "error": "Error en Optimización: División por cero detectada."}
                        res = n1 // n2  # División entera

                    res_str = str(res)
                    constantes_conocidas[dest] = res_str
                    nuevo_codigo.append({"tipo": "ASIGNACION", "destino": dest, "valor": res_str})
                    registro_tecnicas.append(f"Plegado de constantes: {n1} {op} {n2} -> {res_str}")
                    continue

                # 3. SIMPLIFICACIÓN ALGEBRAICA: Identidades matemáticas (x+0, x*1, x*0, etc.)
                simplificado = None
                if (op == "+" and der == "0") or (op == "-" and der == "0"):
                    simplificado = izq
                elif op == "+" and izq == "0":
                    simplificado = der
                elif op == "*" and der == "1":
                    simplificado = izq
                elif op == "*" and izq == "1":
                    simplificado = der
                elif op == "*" and (izq == "0" or der == "0"):
                    simplificado = "0"
                elif op == "/" and der == "1":
                    simplificado = izq

                if simplificado is not None:
                    if es_numero(simplificado):
                        constantes_conocidas[dest] = simplificado
                    nuevo_codigo.append({"tipo": "ASIGNACION", "destino": dest, "valor": simplificado})
                    registro_tecnicas.append(f"Simplificación algebraica: {izq} {op} {der} -> {simplificado}")
                    continue

                # Si no se pudo reducir a asignación simple, actualizamos sus operandos
                nuevo_codigo.append({"tipo": "OPERACION", "destino": dest, "izq": izq, "operador": op, "der": der})

            elif inst["tipo"] == "ASIGNACION":
                val = inst["valor"]
                dest = inst["destino"]

                # Propagación en asignaciones directas (ej: x = t2 -> x = 11)
                if val in constantes_conocidas:
                    val = constantes_conocidas[val]
                    registro_tecnicas.append(f"Propagación de constantes: '{inst['valor']}' reemplazado por {val}")

                if es_numero(val):
                    constantes_conocidas[dest] = val
                elif dest in constantes_conocidas:
                    # Si la variable cambia a un valor desconocido, la sacamos de constantes
                    del constantes_conocidas[dest]

                nuevo_codigo.append({"tipo": "ASIGNACION", "destino": dest, "valor": val})

        codigo = nuevo_codigo

    # 4. ELIMINACIÓN DE CÓDIGO MUERTO: Borrar temporales (t1, t2...) que ya nadie usa
    variables_usadas = set()
    for inst in codigo:
        if inst["tipo"] == "OPERACION":
            variables_usadas.add(inst["izq"])
            variables_usadas.add(inst["der"])
        elif inst["tipo"] == "ASIGNACION":
            variables_usadas.add(inst["valor"])

    codigo_final = []
    for inst in codigo:
        dest = inst["destino"]
        # Si es una variable temporal (empieza con 't' + número) y nadie la lee, es código muerto
        if dest.startswith("t") and dest[1:].isdigit() and dest not in variables_usadas:
            registro_tecnicas.append(f"Eliminación de código muerto: temporal '{dest}' descartado por no usarse.")
            continue
        codigo_final.append(inst)

    # Convertimos el resultado a texto legible para la web
    codigo_texto = []
    for inst in codigo_final:
        if inst["tipo"] == "OPERACION":
            codigo_texto.append(f"{inst['destino']} = {inst['izq']} {inst['operador']} {inst['der']}")
        else:
            codigo_texto.append(f"{inst['destino']} = {inst['valor']}")

    # Eliminamos mensajes duplicados manteniendo el orden
    tecnicas_unicas = list(dict.fromkeys(registro_tecnicas))
    if not tecnicas_unicas:
        tecnicas_unicas.append("El código ya estaba óptimo; no se requirieron reducciones.")

    return {
        "exito": True,
        "instrucciones": codigo_final,
        "codigo_texto": codigo_texto,
        "tecnicas_aplicadas": tecnicas_unicas,
        "mensaje": f"Optimización completada ({len(codigo_texto)} instrucciones finales)."
    }