// quiz.js — desafio interativo do Jornal Voz Ativa.
// Os dados vêm de quiz.py (embutidos na página como JSON).
// Fluxo: pergunta -> feedback imediato + nota da redação -> resultado final.
(function () {
    "use strict";

    var raiz = document.getElementById("quiz");
    var fonte = document.getElementById("quiz-data");
    if (!raiz || !fonte) return;

    var dados = JSON.parse(fonte.textContent);
    var CHAVE_MELHOR = "voz-ativa-melhor";
    var LETRAS = ["A", "B", "C", "D", "E", "F"];
    var reduzirMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var estado;

    // ---------- utilidades ----------

    function el(tag, atributos) {
        var e = document.createElement(tag);
        Object.keys(atributos || {}).forEach(function (k) {
            if (k === "texto") e.textContent = atributos[k];
            else if (k === "classe") e.className = atributos[k];
            else e.setAttribute(k, atributos[k]);
        });
        for (var i = 2; i < arguments.length; i++) {
            if (arguments[i]) e.appendChild(arguments[i]);
        }
        return e;
    }

    function embaralhar(lista) {
        var a = lista.slice();
        for (var i = a.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var t = a[i]; a[i] = a[j]; a[j] = t;
        }
        return a;
    }

    function contar(destino, de, ate, ms, sufixo) {
        sufixo = sufixo || "";
        if (reduzirMovimento || de === ate) { destino.textContent = ate + sufixo; return; }
        var inicio = null;
        function passo(t) {
            if (inicio === null) inicio = t;
            var p = Math.min((t - inicio) / ms, 1);
            destino.textContent = Math.round(de + (ate - de) * p) + sufixo;
            if (p < 1) requestAnimationFrame(passo);
        }
        requestAnimationFrame(passo);
    }

    function aviso(texto) {
        var antigo = document.querySelector(".aviso");
        if (antigo) antigo.remove();
        var a = el("div", { classe: "aviso", role: "status", texto: texto });
        document.body.appendChild(a);
        setTimeout(function () { a.remove(); }, 2600);
    }

    function lerMelhor() {
        try { return JSON.parse(localStorage.getItem(CHAVE_MELHOR)); } catch (e) { return null; }
    }
    function gravarMelhor(pontos, total) {
        try { localStorage.setItem(CHAVE_MELHOR, JSON.stringify({ pontos: pontos, total: total })); } catch (e) {}
    }

    // ---------- estado ----------

    function novoJogo() {
        estado = {
            i: 0,
            pontos: 0,
            respondida: false,
            historico: [],
            // as alternativas são embaralhadas a cada tentativa
            perguntas: dados.perguntas.map(function (p) {
                return {
                    pergunta: p.pergunta,
                    resposta: p.resposta,
                    explicacao: p.explicacao,
                    opcoes: embaralhar(p.opcoes)
                };
            })
        };
    }

    // ---------- tela de pergunta ----------

    function desenharSegmentos() {
        var caixa = el("div", { classe: "segmentos", "aria-hidden": "true" });
        estado.perguntas.forEach(function (_, n) {
            var cls = "";
            if (n < estado.historico.length) cls = estado.historico[n].acertou ? "certa" : "errada";
            else if (n === estado.i) cls = "atual";
            caixa.appendChild(el("span", { classe: cls }));
        });
        return caixa;
    }

    function mostrarPergunta() {
        var total = estado.perguntas.length;
        var p = estado.perguntas[estado.i];
        estado.respondida = false;
        raiz.textContent = "";

        var placarNum = el("b", { texto: String(estado.pontos) });
        var placar = el("span", { classe: "placar" }, document.createTextNode("Acertos: "), placarNum);
        var topo = el("div", { classe: "quiz-topo" },
            el("span", { texto: "Pergunta " + (estado.i + 1) + " de " + total }),
            placar
        );

        var titulo = el("h2", { classe: "pergunta", id: "pergunta-titulo", tabindex: "-1", texto: p.pergunta });
        var lista = el("div", { classe: "opcoes", role: "group", "aria-labelledby": "pergunta-titulo" });
        var nota = el("div", { "aria-live": "polite" });
        var acoes = el("div", { classe: "quiz-acoes" });

        p.opcoes.forEach(function (texto, n) {
            var botao = el("button", { type: "button", classe: "opcao", "data-valor": texto },
                el("span", { classe: "letra", "aria-hidden": "true" }, el("span", { texto: LETRAS[n] })),
                el("span", { texto: texto })
            );
            botao.addEventListener("click", function () { responder(botao, p, lista, nota, acoes, placar, placarNum); });
            lista.appendChild(botao);
        });

        raiz.appendChild(desenharSegmentos());
        raiz.appendChild(topo);
        raiz.appendChild(titulo);
        raiz.appendChild(lista);
        raiz.appendChild(nota);
        raiz.appendChild(acoes);

        // quem navega por teclado/leitor de tela cai direto na pergunta
        if (estado.i > 0) titulo.focus({ preventScroll: false });
    }

    function responder(botao, p, lista, nota, acoes, placar, placarNum) {
        if (estado.respondida) return;
        estado.respondida = true;

        var escolhida = botao.getAttribute("data-valor");
        var acertou = escolhida === p.resposta;

        estado.historico.push({ pergunta: p.pergunta, escolhida: escolhida, resposta: p.resposta, acertou: acertou });

        Array.prototype.forEach.call(lista.children, function (b) {
            var valor = b.getAttribute("data-valor");
            b.disabled = true;
            if (valor === p.resposta) b.classList.add("certa");
            else if (b === botao) b.classList.add("errada");
            else b.classList.add("neutra");
        });

        if (acertou) {
            var antes = estado.pontos;
            estado.pontos++;
            contar(placarNum, antes, estado.pontos, 350);
            placar.classList.add("pulso");
        }

        // atualiza o segmento da barra de progresso
        var segmentos = raiz.querySelectorAll(".segmentos span");
        segmentos[estado.i].className = acertou ? "certa" : "errada";

        nota.textContent = "";
        nota.appendChild(el("div", { classe: "nota " + (acertou ? "certa" : "errada") },
            el("strong", { texto: acertou ? "Resposta certa" : "Não foi dessa vez. A resposta é: " + p.resposta }),
            el("p", { texto: p.explicacao })
        ));

        var ultima = estado.i === estado.perguntas.length - 1;
        var proximo = el("button", { type: "button", classe: "botao", texto: ultima ? "Ver resultado" : "Próxima pergunta" });
        proximo.addEventListener("click", function () {
            estado.i++;
            if (estado.i >= estado.perguntas.length) mostrarResultado(); else mostrarPergunta();
        });
        acoes.appendChild(proximo);
        proximo.focus({ preventScroll: true });
        proximo.scrollIntoView({ block: "nearest", behavior: reduzirMovimento ? "auto" : "smooth" });
    }

    // ---------- tela de resultado ----------

    function mensagemPara(fracao) {
        for (var i = 0; i < dados.mensagens.length; i++) {
            if (fracao >= dados.mensagens[i].minimo) return dados.mensagens[i];
        }
        return dados.mensagens[dados.mensagens.length - 1];
    }

    function compartilhar(pontos, total) {
        var texto = "Acertei " + pontos + " de " + total + " no desafio do Jornal Voz Ativa. Consegue superar?";
        var url = location.href.split("#")[0];

        if (navigator.share) {
            navigator.share({ title: document.title, text: texto, url: url }).catch(function (e) {
                if (e && e.name !== "AbortError") copiar(texto + " " + url);
            });
        } else {
            copiar(texto + " " + url);
        }
    }

    function copiar(texto) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(texto).then(
                function () { aviso("Resultado copiado. Cole onde quiser compartilhar."); },
                function () { aviso("Não foi possível copiar. Copie o endereço da página."); }
            );
        } else {
            aviso("Copie o endereço da página para compartilhar.");
        }
    }

    function mostrarResultado() {
        var total = estado.perguntas.length;
        var pontos = estado.pontos;
        var fracao = pontos / total;
        var pct = Math.round(fracao * 100);
        var msg = mensagemPara(fracao);

        var anterior = lerMelhor();
        var novoRecorde = !anterior || pontos > anterior.pontos;
        if (novoRecorde) gravarMelhor(pontos, total);

        raiz.textContent = "";

        // anel de progresso animado
        var R = 70, C = 2 * Math.PI * R;
        var NS = "http://www.w3.org/2000/svg";
        var svg = document.createElementNS(NS, "svg");
        svg.setAttribute("viewBox", "0 0 168 168");
        svg.setAttribute("aria-hidden", "true");
        var trilho = document.createElementNS(NS, "circle");
        var valor = document.createElementNS(NS, "circle");
        [trilho, valor].forEach(function (c) { c.setAttribute("cx", "84"); c.setAttribute("cy", "84"); c.setAttribute("r", String(R)); });
        trilho.setAttribute("class", "trilho");
        valor.setAttribute("class", "valor");
        valor.setAttribute("stroke-dasharray", C.toFixed(2));
        valor.setAttribute("stroke-dashoffset", C.toFixed(2));
        svg.appendChild(trilho);
        svg.appendChild(valor);

        var numero = el("span", { texto: reduzirMovimento ? pct + "%" : "0%" });
        var anel = el("div", { classe: "anel" + (pontos === total ? " perfeito" : ""), role: "img", "aria-label": pontos + " acertos em " + total + " perguntas" },
            svg,
            el("div", { classe: "anel-texto", "aria-hidden": "true" }, numero, el("small", { texto: pontos + " de " + total }))
        );

        requestAnimationFrame(function () {
            requestAnimationFrame(function () {
                valor.setAttribute("stroke-dashoffset", (C * (1 - fracao)).toFixed(2));
                contar(numero, 0, pct, 1000, "%");
            });
        });

        var titulo = el("h2", { texto: msg.titulo, tabindex: "-1" });

        var recap = el("ol", { classe: "recap" });
        estado.historico.forEach(function (h) {
            var detalhe = h.acertou ? "" : "Você marcou: " + h.escolhida + ". Correta: " + h.resposta + ".";
            recap.appendChild(el("li", { classe: h.acertou ? "ok" : "erro" },
                el("span", { classe: "marca", "aria-hidden": "true", texto: h.acertou ? "✓" : "✕" }),
                el("span", {},
                    document.createTextNode(h.pergunta),
                    el("small", { texto: (h.acertou ? "Acertou" : "Errou") + (detalhe ? ". " + detalhe : "") })
                )
            ));
        });

        var reiniciar = el("button", { type: "button", classe: "botao", texto: "Refazer o desafio" });
        reiniciar.addEventListener("click", function () { novoJogo(); mostrarPergunta(); window.scrollTo({ top: raiz.offsetTop - 80 }); });

        var botaoCompartilhar = el("button", { type: "button", classe: "botao sec", texto: "Compartilhar resultado" });
        botaoCompartilhar.addEventListener("click", function () { compartilhar(pontos, total); });

        var zap = el("a", {
            classe: "botao sec",
            href: "https://wa.me/?text=" + encodeURIComponent("Acertei " + pontos + " de " + total + " no desafio do Jornal Voz Ativa. " + location.href.split("#")[0]),
            target: "_blank",
            rel: "noopener",
            texto: "Enviar no WhatsApp"
        });

        var melhorTexto = novoRecorde
            ? (anterior ? "Novo recorde neste navegador." : "Primeiro resultado salvo neste navegador.")
            : "Seu melhor resultado: " + anterior.pontos + " de " + anterior.total + ".";

        var resultado = el("div", { classe: "resultado" },
            el("p", { classe: "chapeu", texto: "Resultado" }),
            anel, titulo,
            el("p", { texto: msg.texto }),
            recap,
            el("p", { classe: "melhor", texto: melhorTexto }),
            el("div", { classe: "quiz-acoes" }, reiniciar, botaoCompartilhar, zap),
            el("div", { classe: "quiz-acoes" }, el("a", { classe: "botao sec", href: "index.html", texto: "Voltar à capa" }))
        );

        raiz.appendChild(resultado);
        titulo.focus({ preventScroll: true });
    }

    // ---------- atalhos de teclado: 1–4 ou A–D escolhem a alternativa ----------

    document.addEventListener("keydown", function (e) {
        if (!estado || estado.respondida || e.ctrlKey || e.metaKey || e.altKey) return;
        var tecla = e.key.toUpperCase();
        var n = /^[1-9]$/.test(tecla) ? parseInt(tecla, 10) - 1 : LETRAS.indexOf(tecla);
        var botoes = raiz.querySelectorAll(".opcao");
        if (n >= 0 && n < botoes.length) botoes[n].click();
    });

    novoJogo();
    mostrarPergunta();
})();
