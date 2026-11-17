def generar_codigo_destino(instrucciones_optimizadas):
    arquitectura = "Arquitectura RISC Hipotética de 32 bits con Registros Generales (R1..Rn)"
    codigo_ensamblador = [
        f"; Arquitectura Destino: {arquitectura}",
        "; Sección de Código (.text)"
    ]

    mapa_operadores = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "/": "DIV"
    }

    def es_numero(valor):
        return valor.lstrip('-').isdigit()

    # Recorremos cada instrucción limpia que dejó el optimizador
    for inst in instrucciones_optimizadas:
        dest = inst["destino"]

        if inst["tipo"] == "ASIGNACION":
            val = inst["valor"]
            # Cargamos el valor (número inmediato o variable en memoria) en R1
            if es_numero(val):
                codigo_ensamblador.append(f"MOV R1, #{val}      ; Cargar constante {val} en R1")
            else:
                codigo_ensamblador.append(f"LOAD R1, {val}      ; Cargar variable '{val}' en R1")
            
            # Guardamos R1 en la variable destino
            codigo_ensamblador.append(f"STORE {dest}, R1    ; Guardar R1 en '{dest}'")

        elif inst["tipo"] == "OPERACION":
            izq = inst["izq"]
            der = inst["der"]
            mnemonico = mapa_operadores[inst["operador"]]

            # 1. Cargar operando izquierdo en R1
            if es_numero(izq):
                codigo_ensamblador.append(f"MOV R1, #{izq}      ; Cargar constante {izq} en R1")
            else:
                codigo_ensamblador.append(f"LOAD R1, {izq}      ; Cargar '{izq}' en R1")

            # 2. Cargar operando derecho en R2
            if es_numero(der):
                codigo_ensamblador.append(f"MOV R2, #{der}      ; Cargar constante {der} en R2")
            else:
                codigo_ensamblador.append(f"LOAD R2, {der}      ; Cargar '{der}' en R2")

            # 3. Ejecutar operación aritmética: R1 = R1 op R2
            codigo_ensamblador.append(f"{mnemonico} R1, R1, R2  ; Operar R1 {inst['operador']} R2 y dejar en R1")

            # 4. Almacenar el resultado final en memoria
            codigo_ensamblador.append(f"STORE {dest}, R1    ; Almacenar resultado en '{dest}'")

    codigo_ensamblador.append("HALT              ; Fin de ejecución del programa")

    return {
        "exito": True,
        "arquitectura": arquitectura,
        "ensamblador": codigo_ensamblador,
        "mensaje": "Traducción a código ensamblador completada exitosamente."
    }