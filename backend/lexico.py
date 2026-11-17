import re  # Herramienta de Python para buscar patrones de texto (como letras o números)

def analizar_lexico(codigo_fuente):
    # 1. Definimos las reglas (el diccionario) de nuestro lenguaje MiniLang
    reglas_tokens = [
        ('NUMERO',      r'\d+'),             # Uno o más dígitos (ej: 5, 120)
        ('ID',          r'[a-zA-Z_]\w*'),    # Letras para variables (ej: x, total, num1)
        ('ASIGNACION',  r'='),               # El signo igual
        ('SUMA',        r'\+'),              # El signo más
        ('RESTA',       r'-'),               # El signo menos
        ('MULT',        r'\*'),              # El signo multiplicar
        ('DIV',         r'/'),               # El signo dividir
        ('PAR_IZQ',     r'\('),              # Paréntesis abierto
        ('PAR_DER',     r'\)'),              # Paréntesis cerrado
        ('PUNTO_COMA',  r';'),               # Fin de instrucción
        ('ESPACIO',     r'[ \t\n]+'),        # Espacios y saltos de línea (los ignoraremos)
        ('ERROR',       r'.'),               # Cualquier otro símbolo raro no permitido
    ]

    # Unimos todas las reglas en una sola fórmula maestra para Python
    patron_maestro = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in reglas_tokens)

    tokens_encontrados = []

    # 2. Recorremos el código fuente pedazo por pedazo
    for coincidencia in re.finditer(patron_maestro, codigo_fuente):
        tipo = coincidencia.lastgroup   # Qué regla coincidió (ej: NUMERO, ID)
        valor = coincidencia.group()    # El texto exacto (ej: "10", "x")
        posicion = coincidencia.start() # En qué letra ocurrió

        if tipo == 'ESPACIO':
            continue  # Los espacios no nos interesan, pasamos al siguiente
        elif tipo == 'ERROR':
            # Si encontramos un símbolo ilegal, devolvemos el error inmediatamente
            return {
                "exito": False,
                "error": f"Error Léxico en la posición {posicion}: El carácter '{valor}' no pertenece al lenguaje."
            }
        else:
            # Si es válido, lo guardamos en nuestra lista de tokens
            tokens_encontrados.append({
                "tipo": tipo,
                "valor": valor
            })

    # Verificamos que el usuario no haya enviado el cuadro vacío
    if not tokens_encontrados:
        return {
            "exito": False,
            "error": "Error Léxico: El código fuente está vacío."
        }

    # 3. Si todo salió bien, devolvemos éxito y la lista de tokens
    return {
        "exito": True,
        "tokens": tokens_encontrados
    }