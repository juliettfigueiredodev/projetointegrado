// EducaSolidário — Interações das páginas de perfil (doador e instituição)

document.addEventListener('DOMContentLoaded', function () {
    configurarDropdownAvatar();
    configurarBotaoFavoritosDoador();
    configurarBotaoFavoritarInst();
    configurarModalEditarPerfil();
    configurarModalDoacao();
    animarBarrasProgresso();
    aplicarStatusBadges();
});

/* ── DROPDOWN DO AVATAR ─────────────────────────── */
function configurarDropdownAvatar() {
    var avatar = document.querySelector('.avatar-container');
    var dropdown = document.querySelector('.avatar-dropdown');
    if (!avatar || !dropdown) return;

    avatar.addEventListener('click', function (e) {
        e.stopPropagation();
        dropdown.classList.toggle('visivel');
    });

    document.addEventListener('click', function () {
        dropdown.classList.remove('visivel');
    });

    dropdown.addEventListener('click', function (e) {
        e.stopPropagation();
    });

    var btnSair = dropdown.querySelector('.dropdown-sair');
    if (btnSair) {
        btnSair.addEventListener('click', function () {
            window.location.href = 'index.html';
        });
    }
}

/* ── BOTÃO ♡ FAVORITOS → ABA (DOADOR) ───────────── */
function configurarBotaoFavoritosDoador() {
    var btn = document.getElementById('btn-favoritos-doador');
    if (!btn) return;

    btn.addEventListener('click', function () {
        var abaFav = document.querySelector('.perfil-abas button[data-alvo="painel-favoritos"]');
        if (abaFav) {
            abaFav.click();
            abaFav.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    });
}

/* ── TOGGLE FAVORITAR (INSTITUIÇÃO) ──────────────── */
function configurarBotaoFavoritarInst() {
    var btn = document.getElementById('btn-favoritar-inst');
    if (!btn) return;

    btn.addEventListener('click', function () {
        btn.classList.toggle('favoritado');
        if (btn.classList.contains('favoritado')) {
            btn.textContent = '❤️ Favoritado';
        } else {
            btn.textContent = '♡ Favoritar';
        }
    });
}

/* ── MODAL — utilitários ─────────────────────────── */
function abrirModal(modal) {
    if (modal) modal.classList.add('visivel');
}

function fecharModal(modal) {
    if (!modal) return;
    modal.classList.remove('visivel');
    var msg = modal.querySelector('.modal-mensagem');
    if (msg) { msg.className = 'modal-mensagem'; msg.textContent = ''; }
}

function configurarFechamentoModal(modal) {
    if (!modal) return;
    var btnFechar = modal.querySelector('.modal-fechar');
    var btnCancelar = modal.querySelector('.modal-cancelar');

    if (btnFechar) btnFechar.addEventListener('click', function () { fecharModal(modal); });
    if (btnCancelar) btnCancelar.addEventListener('click', function () { fecharModal(modal); });

    modal.addEventListener('click', function (e) {
        if (e.target === modal) fecharModal(modal);
    });
}

/* ── MODAL EDITAR PERFIL (DOADOR) ────────────────── */
function configurarModalEditarPerfil() {
    var btn = document.getElementById('btn-editar-perfil');
    var modal = document.getElementById('modal-editar-perfil');
    if (!btn || !modal) return;

    configurarFechamentoModal(modal);

    btn.addEventListener('click', function () { abrirModal(modal); });

    var btnSalvar = modal.querySelector('.modal-salvar');
    if (btnSalvar) {
        btnSalvar.addEventListener('click', function () {
            var nome = modal.querySelector('#editar-nome');
            var msg = modal.querySelector('.modal-mensagem');

            if (nome && nome.value.trim() === '') {
                if (msg) { msg.className = 'modal-mensagem erro'; msg.textContent = 'Preencha o nome.'; }
                return;
            }

            if (msg) {
                msg.className = 'modal-mensagem sucesso';
                msg.textContent = 'Perfil atualizado com sucesso!';
            }
            setTimeout(function () { fecharModal(modal); }, 1500);
        });
    }
}

/* ── MODAL FAZER DOAÇÃO (INSTITUIÇÃO) ────────────── */
function configurarModalDoacao() {
    var btn = document.getElementById('btn-fazer-doacao');
    var modal = document.getElementById('modal-doacao');
    if (!btn || !modal) return;

    var formBody = modal.querySelector('.modal-body');
    var successView = modal.querySelector('.modal-sucesso');
    var btnConfirmar = modal.querySelector('.modal-confirmar');
    var btnCancelar = modal.querySelector('.modal-cancelar');
    var msg = modal.querySelector('.modal-mensagem');

    function resetarModal() {
        if (formBody) formBody.style.display = '';
        if (successView) successView.style.display = 'none';
        if (btnConfirmar) btnConfirmar.style.display = '';
        if (btnCancelar) btnCancelar.style.display = '';
        if (msg) { msg.className = 'modal-mensagem'; msg.textContent = ''; }
        modal.querySelectorAll('input[type="checkbox"]').forEach(function (cb) { cb.checked = false; });
    }

    btn.addEventListener('click', function () {
        resetarModal();
        abrirModal(modal);
    });

    configurarFechamentoModal(modal);

    if (btnConfirmar) {
        btnConfirmar.addEventListener('click', function () {
            var selecionados = modal.querySelectorAll('input[type="checkbox"]:checked');
            if (selecionados.length === 0) {
                if (msg) { msg.className = 'modal-mensagem erro'; msg.textContent = 'Selecione pelo menos um item para doar.'; }
                return;
            }
            if (formBody) formBody.style.display = 'none';
            if (btnConfirmar) btnConfirmar.style.display = 'none';
            if (btnCancelar) btnCancelar.style.display = 'none';
            if (msg) { msg.className = 'modal-mensagem'; msg.textContent = ''; }
            if (successView) successView.style.display = 'flex';
        });
    }

    var btnFecharSucesso = modal.querySelector('.modal-fechar-sucesso');
    if (btnFecharSucesso) {
        btnFecharSucesso.addEventListener('click', function () { fecharModal(modal); });
    }
}

/* ── ANIMAR BARRAS DE PROGRESSO ──────────────────── */
function animarBarrasProgresso() {
    var barras = document.querySelectorAll('.barra-preenchida, .conquista .progresso span');
    if (barras.length === 0) return;

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var el = entry.target;
                var largura = el.getAttribute('data-largura');
                el.style.width = '0%';
                requestAnimationFrame(function () {
                    requestAnimationFrame(function () {
                        el.style.width = largura;
                    });
                });
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.3 });

    barras.forEach(function (barra) {
        barra.setAttribute('data-largura', barra.style.width);
        observer.observe(barra);
    });
}

/* ── STATUS BADGES COLORIDOS ─────────────────────── */
function aplicarStatusBadges() {
    var badges = document.querySelectorAll('.status-badge');
    badges.forEach(function (badge) {
        var texto = badge.textContent.trim().toLowerCase();
        if (texto === 'concluída') {
            badge.classList.add('status-concluida');
        } else if (texto === 'pendente') {
            badge.classList.add('status-pendente');
        } else if (texto === 'cancelada') {
            badge.classList.add('status-cancelada');
        }
    });
}
