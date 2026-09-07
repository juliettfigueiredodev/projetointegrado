/**
 * EducaSolidário - Lógica de Login
 * Alternância dinâmica de perfis (Doador / Instituição) e validação de formulário
 */

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Estado global do perfil ativo no login ('doador' ou 'instituicao')
let perfilAtivo = 'doador';

document.addEventListener('DOMContentLoaded', function () {
    const btnDoador = document.getElementById('btn-doador');
    const btnInstituicao = document.getElementById('btn-instituicao');
    const loginSubtitle = document.getElementById('login-subtitle');
    const loginForm = document.getElementById('login-form');
    const btnGoogle = document.querySelector('.btn-google');

    // Detecta o perfil inicial a partir da classe .active do botão no HTML
    if (btnInstituicao && btnInstituicao.classList.contains('active')) {
        perfilAtivo = 'instituicao';
    } else {
        perfilAtivo = 'doador';
    }

    // Alternância dinâmica de perfil sem recarregar a página
    function trocarPerfil(novoPerfil) {
        perfilAtivo = novoPerfil;
        limparErros();

        if (novoPerfil === 'instituicao') {
            if (btnInstituicao) btnInstituicao.classList.add('active');
            if (btnDoador) btnDoador.classList.remove('active');
            if (loginSubtitle) loginSubtitle.textContent = 'Entre na conta da sua Instituição para continuar';
        } else {
            if (btnDoador) btnDoador.classList.add('active');
            if (btnInstituicao) btnInstituicao.classList.remove('active');
            if (loginSubtitle) loginSubtitle.textContent = 'Entre na sua conta de Doador para continuar';
        }
    }

    if (btnDoador) {
        btnDoador.addEventListener('click', function () {
            if (perfilAtivo !== 'doador') {
                trocarPerfil('doador');
            }
        });
    }

    if (btnInstituicao) {
        btnInstituicao.addEventListener('click', function () {
            if (perfilAtivo !== 'instituicao') {
                trocarPerfil('instituicao');
            }
        });
    }

    // Submissão do formulário
    if (loginForm) {
        loginForm.addEventListener('submit', validarLogin);
    }

    // Botão Continuar com Google
    if (btnGoogle) {
        btnGoogle.addEventListener('click', function () {
            window.location.href = 'index.html';
        });
    }

    // Limpeza reativa de erros enquanto o usuário digita
    ['email', 'senha'].forEach(campoId => {
        const input = document.getElementById(campoId);
        if (input) {
            input.addEventListener('input', function () {
                this.classList.remove('input-invalid');
                const erroSpan = document.getElementById(`${campoId}-error`);
                if (erroSpan) erroSpan.textContent = '';

                const formMsg = document.getElementById('login-form-msg');
                if (formMsg && formMsg.classList.contains('error')) {
                    formMsg.textContent = '';
                    formMsg.className = 'form-message';
                }
            });
        }
    });

    // Configura botões de alternar visualização de senha (mostrar/ocultar)
    configurarToggleSenha();
});

function configurarToggleSenha() {
    document.querySelectorAll('.toggle-password').forEach(btn => {
        btn.addEventListener('click', function () {
            const inputId = this.dataset.target;
            const input = document.getElementById(inputId);
            if (!input) return;

            if (input.type === 'password') {
                input.type = 'text';
                this.classList.add('visible');
                this.setAttribute('aria-label', 'Ocultar senha');
                this.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`;
            } else {
                input.type = 'password';
                this.classList.remove('visible');
                this.setAttribute('aria-label', 'Mostrar senha');
                this.innerHTML = `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;
            }
        });
    });
}

/* ==========================================================================
   Funções de Validação e Mensagens de Erro
   ========================================================================== */

function limparErros() {
    document.querySelectorAll('.field-error').forEach(span => span.textContent = '');
    document.querySelectorAll('#login-form input').forEach(input => input.classList.remove('input-invalid'));

    const formMsg = document.getElementById('login-form-msg');
    if (formMsg) {
        formMsg.textContent = '';
        formMsg.className = 'form-message';
    }
}

function mostrarErroCampo(inputId, mensagem) {
    const erroSpan = document.getElementById(`${inputId}-error`);
    const input = document.getElementById(inputId);
    if (erroSpan) erroSpan.textContent = mensagem;
    if (input) input.classList.add('input-invalid');
}

function mostrarMensagemFormulario(tipo, texto) {
    const msg = document.getElementById('login-form-msg');
    if (!msg) return;
    msg.textContent = texto;
    msg.className = `form-message ${tipo}`; // tipo: 'error' ou 'success'
}

function validarLogin(event) {
    if (event) event.preventDefault();

    limparErros();

    const emailInput = document.getElementById('email');
    const senhaInput = document.getElementById('senha');
    let valido = true;

    const emailValor = emailInput ? emailInput.value.trim() : '';
    const senhaValor = senhaInput ? senhaInput.value : '';

    // Validação de E-mail
    if (!emailValor) {
        mostrarErroCampo('email', 'Informe seu e-mail.');
        valido = false;
    } else if (!EMAIL_REGEX.test(emailValor)) {
        mostrarErroCampo('email', 'Informe um e-mail válido.');
        valido = false;
    }

    // Validação de Senha
    if (!senhaValor) {
        mostrarErroCampo('senha', 'Informe sua senha.');
        valido = false;
    } else if (senhaValor.length < 8) {
        mostrarErroCampo('senha', 'A senha deve ter pelo menos 8 caracteres.');
        valido = false;
    }

    if (!valido) {
        mostrarMensagemFormulario('error', 'Corrija os campos destacados antes de continuar.');
        return false;
    }

    // Sucesso na validação
    mostrarMensagemFormulario('success', 'Login realizado com sucesso! Redirecionando...');

    // Redirecionamento de acordo com o perfil selecionado
    const destino = perfilAtivo === 'instituicao' ? 'perfil-instituicao.html' : 'perfil-doador.html';
    setTimeout(() => {
        window.location.href = destino;
    }, 600);

    return false;
}
