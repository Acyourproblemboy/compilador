const URL_BACKEND = "http://127.0.0.1:5000/compilar";

function cargarEjemplo(tipo) {
    const editor = document.getElementById("codigo-fuente");
    if (tipo === "valido") {
        editor.value = "a = 10;\nb = a + 5 * 2;";
    } else if (tipo === "optimizable") {
        editor.value = "x = 5 + 3 * 0;\ny = x * 1 + 4;";
    } else if (tipo === "error") {
        editor.value = "x = z + 5;"; // Error semántico: 'z' no ha sido declarada
    }
}

function setEstadoFase(idFase, estado, textoBadge, contenidoHTML) {
    const badge = document.getElementById(`badge-${idFase}`);
    const contenedor = document.getElementById(`res-${idFase}`);

    badge.className = "badge";
    if (estado === "ok") badge.classList.add("ok");
    if (estado === "err") badge.classList.add("err");
    if (estado === "stop") badge.classList.add("stop");

    badge.textContent = textoBadge;
    contenedor.innerHTML = contenidoHTML;
}

function reiniciarTablero() {
    const fases = ["lexico", "sintactico", "semantico", "intermedio", "optimizacion", "destino"];
    fases.forEach(f => setEstadoFase(f, "", "En espera", "Procesando..."));
    const banner = document.getElementById("banner-estado");
    banner.className = "banner oculto";
}

async function ejecutarCompilacion() {
    const codigo = document.getElementById("codigo-fuente").value;
    const banner = document.getElementById("banner-estado");
    reiniciarTablero();

    try {
        const respuesta = await fetch(URL_BACKEND, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ codigo: codigo })
        });

        const data = await respuesta.json();
        const f = data.fases;

        // 1. LÉXICO
        if (f.lexico) {
            if (f.lexico.exito) {
                let tabla = `<table class="tabla-mini"><tr><th>Token</th><th>Tipo</th></tr>`;
                f.lexico.tokens.forEach(t => {
                    tabla += `<tr><td>${t.valor}</td><td>${t.tipo}</td></tr>`;
                });
                tabla += `</table>`;
                setEstadoFase("lexico", "ok", "Completado", tabla);
            } else {
                setEstadoFase("lexico", "err", "Error", f.lexico.error);
            }
        }

        // 2. SINTÁCTICO
        if (!f.sintactico) {
            setEstadoFase("sintactico", "stop", "Detenido", "No ejecutado por error previo.");
        } else if (f.sintactico.exito) {
            setEstadoFase("sintactico", "ok", "Completado", `${f.sintactico.mensaje}\n\nAST generado:\n${JSON.stringify(f.sintactico.arbol, null, 2)}`);
        } else {
            setEstadoFase("sintactico", "err", "Error", f.sintactico.error);
        }

        // 3. SEMÁNTICO
        if (!f.semantico) {
            setEstadoFase("semantico", "stop", "Detenido", "No ejecutado por error previo.");
        } else if (f.semantico.exito) {
            let tablaSimb = `<p>${f.semantico.mensaje}</p><br><table class="tabla-mini"><tr><th>Variable</th><th>Tipo</th><th>Línea</th></tr>`;
            for (const [nombre, info] of Object.entries(f.semantico.tabla_simbolos)) {
                tablaSimb += `<tr><td>${nombre}</td><td>${info.tipo}</td><td>${info.linea_declaracion}</td></tr>`;
            }
            tablaSimb += `</table>`;
            setEstadoFase("semantico", "ok", "Completado", tablaSimb);
        } else {
            setEstadoFase("semantico", "err", "Error", f.semantico.error);
        }

        // 4. INTERMEDIO
        if (!f.intermedio) {
            setEstadoFase("intermedio", "stop", "Detenido", "No ejecutado por error previo.");
        } else {
            setEstadoFase("intermedio", "ok", "Completado", f.intermedio.codigo_texto.join("\n"));
        }

        // 5. OPTIMIZACIÓN
        if (!f.optimizacion) {
            setEstadoFase("optimizacion", "stop", "Detenido", "No ejecutado por error previo.");
        } else if (f.optimizacion.exito) {
            const tecnicas = f.optimizacion.tecnicas_aplicadas.map(t => "• " + t).join("\n");
            setEstadoFase("optimizacion", "ok", "Completado", `Código Optimizado:\n${f.optimizacion.codigo_texto.join("\n")}\n\nTécnicas aplicadas:\n${tecnicas}`);
        } else {
            setEstadoFase("optimizacion", "err", "Error", f.optimizacion.error);
        }

        // 6. DESTINO
        if (!f.destino) {
            setEstadoFase("destino", "stop", "Detenido", "No ejecutado por error previo.");
        } else {
            setEstadoFase("destino", "ok", "Completado", f.destino.ensamblador.join("\n"));
        }

        // BANNER GENERAL
        banner.classList.remove("oculto");
        if (data.exito_total) {
            banner.classList.add("exito");
            banner.textContent = "✅ Compilación exitosa: Todas las fases de análisis y síntesis finalizaron correctamente.";
        } else {
            banner.classList.add("error");
            banner.textContent = `❌ Compilación detenida en [${data.fase_error}]: ${data.mensaje_error}`;
        }

    } catch (error) {
        banner.classList.remove("oculto");
        banner.classList.add("error");
        banner.textContent = "⚠️ No se pudo conectar con el Backend. Asegúrate de ejecutar 'python backend/app.py' en tu terminal.";
    }
}