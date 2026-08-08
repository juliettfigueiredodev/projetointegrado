// Alterna entre as telas de login (cadastro-doador.html / cadastro-instituicao.html)
document.addEventListener('DOMContentLoaded', function () {
    const btnDoador = document.getElementById('btn-doador');
    const btnInstituicao = document.getElementById('btn-instituicao');

    if (btnDoador && btnInstituicao) {
        btnDoador.addEventListener('click', function () {
            if (!btnDoador.classList.contains('active')) {
                window.location.href = 'cadastro-doador.html';
            }
        });

        btnInstituicao.addEventListener('click', function () {
            if (!btnInstituicao.classList.contains('active')) {
                window.location.href = 'cadastro-instituicao.html';
            }
        });
    }

    // Entrar / Continuar com Google -> ainda sem validação de e-mail e senha,
    // por enquanto direciona direto para a tela principal (index)
    const btnPrimary = document.querySelector('.btn-primary');
    const btnGoogle = document.querySelector('.btn-google');

    if (btnPrimary) {
        btnPrimary.addEventListener('click', function () {
            window.location.href = 'index.html';
        });
    }

    if (btnGoogle) {
        btnGoogle.addEventListener('click', function () {
            window.location.href = 'index.html';
        });
    }
});
