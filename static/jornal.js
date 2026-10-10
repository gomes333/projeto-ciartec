// jornal.js — comportamento comum a todas as páginas:
// data do dia, modo noturno, menu retrátil no celular e barra de leitura.
(function () {
    "use strict";

    // Data de hoje (o HTML já traz a data do build como reserva)
    var hoje = document.querySelector("[data-hoje]");
    if (hoje) {
        hoje.textContent = new Date().toLocaleDateString("pt-BR", {
            weekday: "long", day: "numeric", month: "long", year: "numeric"
        });
    }

    // Modo noturno
    var raiz = document.documentElement;
    var botaoTema = document.getElementById("tema");

    function rotuloTema() {
        var escuro = raiz.dataset.theme === "dark";
        botaoTema.setAttribute("aria-pressed", escuro ? "true" : "false");
        botaoTema.textContent = escuro ? "Modo claro" : "Modo noturno";
    }

    if (botaoTema) {
        rotuloTema();
        botaoTema.addEventListener("click", function () {
            var novo = raiz.dataset.theme === "dark" ? "light" : "dark";
            raiz.dataset.theme = novo;
            try { localStorage.setItem("voz-ativa-tema", novo); } catch (e) {}
            rotuloTema();
        });
    }

    // Menu retrátil (celular)
    var botaoMenu = document.getElementById("menu-botao");
    var menu = document.getElementById("menu");

    function fecharMenu() {
        if (!menu) return;
        menu.classList.remove("aberto");
        botaoMenu.setAttribute("aria-expanded", "false");
    }

    if (botaoMenu && menu) {
        botaoMenu.addEventListener("click", function () {
            var abrir = !menu.classList.contains("aberto");
            menu.classList.toggle("aberto", abrir);
            botaoMenu.setAttribute("aria-expanded", abrir ? "true" : "false");
        });
        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape") { fecharMenu(); botaoMenu.focus(); }
        });
        document.addEventListener("click", function (e) {
            if (!menu.contains(e.target) && !botaoMenu.contains(e.target)) fecharMenu();
        });
    }

    // Barra: mostra o nome pequeno ao rolar e desenha o progresso de leitura
    var barra = document.getElementById("barra");
    var progresso = document.getElementById("progresso");
    var esperando = false;

    function atualizar() {
        esperando = false;
        var topo = window.scrollY || document.documentElement.scrollTop;
        var total = document.documentElement.scrollHeight - window.innerHeight;
        if (barra) barra.classList.toggle("rolou", barra.getBoundingClientRect().top <= 0 && topo > 0);
        if (progresso) progresso.style.transform = "scaleX(" + (total > 0 ? Math.min(topo / total, 1) : 0) + ")";
    }

    window.addEventListener("scroll", function () {
        if (!esperando) { esperando = true; requestAnimationFrame(atualizar); }
    }, { passive: true });
    window.addEventListener("resize", atualizar);
    atualizar();
})();
