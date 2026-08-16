/* Script para alternar as telas */
function switchScreen(screenName) {
    document.querySelectorAll('.form-screen').forEach(el => el.classList.remove('active'));
    document.getElementById(`screen-${screenName}`).classList.add('active');

    const header = document.querySelector('.auth-header');
    if (screenName === 'sucesso') {
        header.style.display = 'none';
    } else {
        header.style.display = 'block';
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
