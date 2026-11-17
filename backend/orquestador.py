from lexico import analizar_lexico
from sintactico import analizar_sintactico
from semantico import analizar_semantico
from intermedio import generar_codigo_intermedio
from optimizador import optimizar_codigo
from destino import generar_codigo_destino

def compilar_codigo(codigo_fuente):
    # Estructura base de respuesta para el Frontend
    reporte = {
        "exito_total": False,
        "fase_error": None,
        "mensaje_error": None,
        "fases": {
            "lexico": None,
            "sintactico": None,
            "semantico": None,
            "intermedio": None,
            "optimizacion": None,
            "destino": None
        }
    }

    # 1. FASE LÉXICA
    res_lexico = analizar_lexico(codigo_fuente)
    reporte["fases"]["lexico"] = res_lexico
    if not res_lexico["exito"]:
        reporte["fase_error"] = "Análisis Léxico"
        reporte["mensaje_error"] = res_lexico["error"]
        return reporte

    # 2. FASE SINTÁCTICA
    res_sintactico = analizar_sintactico(res_lexico["tokens"])
    reporte["fases"]["sintactico"] = res_sintactico
    if not res_sintactico["exito"]:
        reporte["fase_error"] = "Análisis Sintáctico"
        reporte["mensaje_error"] = res_sintactico["error"]
        return reporte

    # 3. FASE SEMÁNTICA
    res_semantico = analizar_semantico(res_sintactico["arbol"])
    reporte["fases"]["semantico"] = res_semantico
    if not res_semantico["exito"]:
        reporte["fase_error"] = "Análisis Semántico"
        reporte["mensaje_error"] = res_semantico["error"]
        return reporte

    # 4. GENERACIÓN DE CÓDIGO INTERMEDIO
    res_intermedio = generar_codigo_intermedio(res_sintactico["arbol"])
    reporte["fases"]["intermedio"] = res_intermedio

    # 5. OPTIMIZACIÓN DE CÓDIGO
    res_optimizado = optimizar_codigo(res_intermedio["instrucciones"])
    reporte["fases"]["optimizacion"] = res_optimizado
    if not res_optimizado["exito"]:
        reporte["fase_error"] = "Optimización de Código"
        reporte["mensaje_error"] = res_optimizado["error"]
        return reporte

    # 6. GENERACIÓN DE CÓDIGO DESTINO
    res_destino = generar_codigo_destino(res_optimizado["instrucciones"])
    reporte["fases"]["destino"] = res_destino

    # Si llegó hasta aquí, ¡compilación 100% exitosa!
    reporte["exito_total"] = True
    return reporte