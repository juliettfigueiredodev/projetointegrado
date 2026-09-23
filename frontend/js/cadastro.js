let ultimoTipoCadastrado = 'instituicao';

/* Script para alternar as telas */
function switchScreen(screenName) {
    if (screenName !== 'sucesso') {
        ultimoTipoCadastrado = screenName;
    }
    document.querySelectorAll('.form-screen').forEach(el => el.classList.remove('active'));
    document.getElementById(`screen-${screenName}`).classList.add('active');

    const header = document.querySelector('.auth-header');
    const backLink = document.querySelector('.back-link');
    if (screenName === 'sucesso') {
        header.style.display = 'none';
    } else {
        header.style.display = 'block';
        if (backLink) {
            backLink.href = screenName === 'instituicao' ? 'login_instituicao.html' : 'login_doador.html';
        }
    }
}

function irParaLogin() {
    if (ultimoTipoCadastrado === 'doador') {
        window.location.href = 'login_doador.html';
    } else {
        window.location.href = 'login_instituicao.html';
    }
}

/* VALIDAÇÃO JAVASCRIPT [PF3]
   Cada formulário (instituicao / doador) tem seus próprios campos, mas a
   lógica de validação é a mesma: percorre os campos obrigatórios daquele
   formulário, confere se estão preenchidos, confere o formato do e-mail
   com uma regex simples, e confere se as duas senhas coincidem. Se algo
   falhar, mostra a mensagem de erro embaixo do campo e uma mensagem geral
   no topo do formulário, sem trocar de tela. Se tudo passar, mostra a
   mensagem de sucesso e chama switchScreen('sucesso')  */

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;  // Regex simples: algumacoisa@agulmacoisa.algumacoisa

function limparErros(prefixoCampo, tipoTela) {
    document.querySelectorAll(`[id^="${prefixoCampo}-"][id$="-error"]`)
        .forEach(span => span.textContent = '');
    document.querySelectorAll(`#screen-${tipoTela} input`)
        .forEach(input => input.classList.remove('input-invalid'));
}

function mostrarErroCampo(inputId, mensagem) {
    const erroSpan = document.getElementById(`${inputId}-error`);
    const input = document.getElementById(inputId);
    if (erroSpan) erroSpan.textContent = mensagem;
    if (input) input.classList.add('input-invalid');
}

function mostrarMensagemFormulario(prefixo, tipo, texto) {
    const msg = document.getElementById(`${prefixo}-form-msg`);
    if (!msg) return;
    msg.textContent = texto;
    msg.className = `form-message ${tipo}`; // tipo: 'error' ou 'success'
}

function validarFormulario(event, tipo) {
    event.preventDefault();

    ultimoTipoCadastrado = tipo;
    const prefixo = tipo === 'instituicao' ? 'inst' : 'doa';
    const screenId = tipo; // 'instituicao' ou 'doador'
    limparErros(prefixo, screenId);

    let valido = true;

    // Campos de texto/telefone obrigatórios (exceto e-mail e senhas,
    // tratados à parte abaixo)
    const camposTexto = tipo === 'instituicao'
        ? ['inst-nome', 'inst-cnpj', 'inst-tel']
        : ['doa-nome', 'doa-cpf'];

    camposTexto.forEach(id => {
        const campo = document.getElementById(id);
        if (!campo.value.trim()) {
            mostrarErroCampo(id, 'Este campo é obrigatório.');
            valido = false;
        }
    });

    // E-mail: obrigatório + formato válido
    const emailId = `${prefixo}-email`;
    const email = document.getElementById(emailId);
    if (!email.value.trim()) {
        mostrarErroCampo(emailId, 'Informe um e-mail.');
        valido = false;
    } else if (!EMAIL_REGEX.test(email.value.trim())) {
        mostrarErroCampo(emailId, 'Informe um e-mail válido.');
        valido = false;
    }

    // Senha + confirmação: obrigatórias e iguais
    const senhaId = `${prefixo}-senha`;
    const confSenhaId = `${prefixo}-conf-senha`;
    const senha = document.getElementById(senhaId);
    const confSenha = document.getElementById(confSenhaId);

    if (!senha.value) {
        mostrarErroCampo(senhaId, 'Informe uma senha.');
        valido = false;
    } else if (senha.value.length < 8) {
        mostrarErroCampo(senhaId, 'A senha deve ter pelo menos 8 caracteres.');
        valido = false;
    }
    if (!confSenha.value) {
        mostrarErroCampo(confSenhaId, 'Confirme sua senha.');
        valido = false;
    } else if (senha.value && confSenha.value !== senha.value) {
        mostrarErroCampo(confSenhaId, 'As senhas não coincidem.');
        valido = false;
    }

    // Termos de uso
    const termsId = `${prefixo}-terms`;
    const terms = document.getElementById(termsId);
    if (!terms.checked) {
        mostrarErroCampo(termsId, 'Você precisa aceitar os Termos de Uso para continuar.');
        valido = false;
    }

    if (!valido) {
        mostrarMensagemFormulario(screenId, 'error', 'Corrija os campos destacados antes de continuar.');
        return false;
    }

    mostrarMensagemFormulario(screenId, 'success', 'Cadastro validado com sucesso!');
    switchScreen('sucesso');
    return false;
}

/* ==========================================================================
   Máscaras de Entrada em Tempo Real e Alternância de Visualização de Senha
   ========================================================================== */

function aplicarMascaraCPF(valor) {
    return valor
        .replace(/\D/g, '')
        .slice(0, 11)
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
}

function aplicarMascaraCNPJ(valor) {
    return valor
        .replace(/\D/g, '')
        .slice(0, 14)
        .replace(/(\d{2})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1/$2')
        .replace(/(\d{4})(\d{1,2})$/, '$1-$2');
}

function aplicarMascaraTelefone(valor) {
    const digits = valor.replace(/\D/g, '').slice(0, 11);
    if (digits.length <= 10) {
        return digits
            .replace(/(\d{2})(\d)/, '($1) $2')
            .replace(/(\d{4})(\d)/, '$1-$2');
    }
    return digits
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{5})(\d)/, '$1-$2');
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

document.addEventListener('DOMContentLoaded', function () {
    // Máscaras de entrada
    const cpfInput = document.getElementById('doa-cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', function () {
            this.value = aplicarMascaraCPF(this.value);
        });
    }

    const cnpjInput = document.getElementById('inst-cnpj');
    if (cnpjInput) {
        cnpjInput.addEventListener('input', function () {
            this.value = aplicarMascaraCNPJ(this.value);
        });
    }

    const telInput = document.getElementById('inst-tel');
    if (telInput) {
        telInput.addEventListener('input', function () {
            this.value = aplicarMascaraTelefone(this.value);
        });
    }

    // Inicializa botões de visualização de senha
    configurarToggleSenha();

    // Limpeza reativa de erros enquanto o usuário digita
    document.querySelectorAll('.auth-form input').forEach(input => {
        input.addEventListener('input', function () {
            this.classList.remove('input-invalid');
            const erroSpan = document.getElementById(`${this.id}-error`);
            if (erroSpan) erroSpan.textContent = '';

            const screenEl = this.closest('.form-screen');
            if (screenEl) {
                const screenId = screenEl.id.replace('screen-', '');
                const msg = document.getElementById(`${screenId}-form-msg`);
                if (msg && msg.classList.contains('error')) {
                    msg.textContent = '';
                    msg.className = 'form-message';
                }
            }
        });
    });
});
