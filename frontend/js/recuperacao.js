/**
 * EducaSolidário - Lógica do Fluxo de Recuperação de Senha
 * Abrange: recuperar-senha.html, verificar-codigo.html e nova-senha.html
 */

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

document.addEventListener('DOMContentLoaded', function () {
    configurarTelaSolicitacao();
    configurarTelaCodigo();
    configurarTelaNovaSenha();
    configurarToggleSenha();
});

/* ==========================================================================
   1. Tela: recuperar-senha.html (Solicitação de e-mail)
   ========================================================================== */
function configurarTelaSolicitacao() {
    const form = document.getElementById('form-recuperar');
    const emailInput = document.getElementById('email');

    if (!form || !emailInput) return;

    // Limpa erro enquanto digita
    emailInput.addEventListener('input', function () {
        this.classList.remove('input-invalid');
        const err = document.getElementById('email-error');
        if (err) err.textContent = '';
        limparMensagemGeral();
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        limparErros();

        const emailValor = emailInput.value.trim();
        let valido = true;

        if (!emailValor) {
            mostrarErroCampo('email', 'Informe o seu e-mail cadastrado.');
            valido = false;
        } else if (!EMAIL_REGEX.test(emailValor)) {
            mostrarErroCampo('email', 'Informe um e-mail válido.');
            valido = false;
        }

        if (!valido) {
            mostrarMensagemFormulario('error', 'Verifique o e-mail digitado antes de continuar.');
            return false;
        }

        // Salva e-mail na sessão para exibir na próxima tela
        try {
            sessionStorage.setItem('recuperar_email', emailValor);
        } catch (e) {
            // Suporte silencioso caso sessionStorage esteja bloqueado
        }

        mostrarMensagemFormulario('success', 'Instruções enviadas! Redirecionando...');
        setTimeout(() => {
            window.location.href = 'verificar-codigo.html';
        }, 600);
    });
}

/* ==========================================================================
   2. Tela: verificar-codigo.html (Código de 6 dígitos)
   ========================================================================== */
function configurarTelaCodigo() {
    const form = document.getElementById('form-codigo');
    const inputs = document.querySelectorAll('.codigo input');
    const displayEmail = document.getElementById('email-destinatario');
    const btnReenviar = document.getElementById('btn-reenviar');

    if (!form || inputs.length === 0) return;

    // Preenche o e-mail real armazenado na tela anterior, se houver
    try {
        const emailSalvo = sessionStorage.getItem('recuperar_email');
        if (emailSalvo && displayEmail) {
            displayEmail.textContent = emailSalvo;
        }
    } catch (e) {}

    // Navegação automática e restrição numérica entre os 6 inputs
    inputs.forEach((input, index) => {
        input.addEventListener('input', function (e) {
            // Aceita apenas números
            this.value = this.value.replace(/\D/g, '');

            this.classList.remove('input-invalid');
            limparMensagemGeral();

            if (this.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', function (e) {
            if (e.key === 'Backspace' && !this.value && index > 0) {
                inputs[index - 1].focus();
            }
        });

        // Suporte a colar código completo
        input.addEventListener('paste', function (e) {
            e.preventDefault();
            const dadosColados = (e.clipboardData || window.clipboardData).getData('text');
            const numeros = dadosColados.replace(/\D/g, '').slice(0, inputs.length);

            numeros.split('').forEach((num, i) => {
                if (inputs[i]) {
                    inputs[i].value = num;
                    inputs[i].classList.remove('input-invalid');
                }
            });

            const proximoIndex = Math.min(numeros.length, inputs.length - 1);
            if (inputs[proximoIndex]) {
                inputs[proximoIndex].focus();
            }
        });
    });

    // Clique em reenviar código com feedback visual
    if (btnReenviar) {
        btnReenviar.addEventListener('click', function (e) {
            e.preventDefault();
            mostrarMensagemFormulario('success', 'Novo código enviado para seu e-mail!');
            setTimeout(() => {
                limparMensagemGeral();
            }, 3500);
        });
    }

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        limparErros();

        let codigoCompleto = '';
        let temVazio = false;

        inputs.forEach(inp => {
            const val = inp.value.trim();
            codigoCompleto += val;
            if (!val) {
                inp.classList.add('input-invalid');
                temVazio = true;
            }
        });

        if (temVazio || codigoCompleto.length < inputs.length) {
            mostrarMensagemFormulario('error', 'Por favor, digite todos os 6 dígitos do código.');
            return false;
        }

        mostrarMensagemFormulario('success', 'Código verificado com sucesso! Redirecionando...');
        setTimeout(() => {
            window.location.href = 'nova-senha.html';
        }, 600);
    });
}

/* ==========================================================================
   3. Tela: nova-senha.html (Definição de nova senha)
   ========================================================================== */
function configurarTelaNovaSenha() {
    const form = document.getElementById('form-nova-senha');
    const senhaInput = document.getElementById('senha');
    const confInput = document.getElementById('confirmar');

    if (!form || !senhaInput || !confInput) return;

    [senhaInput, confInput].forEach(inp => {
        inp.addEventListener('input', function () {
            this.classList.remove('input-invalid');
            const err = document.getElementById(`${this.id}-error`);
            if (err) err.textContent = '';
            limparMensagemGeral();
        });
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        limparErros();

        const senhaVal = senhaInput.value;
        const confVal = confInput.value;
        let valido = true;

        if (!senhaVal) {
            mostrarErroCampo('senha', 'Informe sua nova senha.');
            valido = false;
        } else if (senhaVal.length < 8) {
            mostrarErroCampo('senha', 'A nova senha deve ter pelo menos 8 caracteres.');
            valido = false;
        }

        if (!confVal) {
            mostrarErroCampo('confirmar', 'Confirme sua nova senha.');
            valido = false;
        } else if (senhaVal && confVal !== senhaVal) {
            mostrarErroCampo('confirmar', 'As senhas não coincidem.');
            valido = false;
        }

        if (!valido) {
            mostrarMensagemFormulario('error', 'Corrija os campos destacados antes de continuar.');
            return false;
        }

        mostrarMensagemFormulario('success', 'Senha redefinida com sucesso! Redirecionando...');
        setTimeout(() => {
            window.location.href = 'senha-redefinida.html';
        }, 600);
    });
}

/* ==========================================================================
   Funções de Utilidade (Erros, Feedback e Olho)
   ========================================================================== */
function limparErros() {
    document.querySelectorAll('.field-error').forEach(el => el.textContent = '');
    document.querySelectorAll('input').forEach(el => el.classList.remove('input-invalid'));
    limparMensagemGeral();
}

function limparMensagemGeral() {
    const msg = document.getElementById('form-msg');
    if (msg) {
        msg.textContent = '';
        msg.className = 'form-message';
    }
}

function mostrarErroCampo(inputId, mensagem) {
    const erroSpan = document.getElementById(`${inputId}-error`);
    const input = document.getElementById(inputId);
    if (erroSpan) erroSpan.textContent = mensagem;
    if (input) input.classList.add('input-invalid');
}

function mostrarMensagemFormulario(tipo, texto) {
    const msg = document.getElementById('form-msg');
    if (!msg) return;
    msg.textContent = texto;
    msg.className = `form-message ${tipo}`;
}

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
