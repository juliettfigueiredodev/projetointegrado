// Alterna entre as telas de login (login_doador.html / login_instituicao.html)
document.addEventListener('DOMContentLoaded', function () {
    const btnDoador = document.getElementById('btn-doador');
    const btnInstituicao = document.getElementById('btn-instituicao');

    if (btnDoador && btnInstituicao) {
        btnDoador.addEventListener('click', function () {
            if (!btnDoador.classList.contains('active')) {
                window.location.href = 'login_doador.html';
            }
        });

        btnInstituicao.addEventListener('click', function () {
            if (!btnInstituicao.classList.contains('active')) {
                window.location.href = 'login_instituição.html';
            }
        });
    }

    // Entrar / Continuar com Google -> ainda sem validação de e-mail e senha,
    // Ao clicar em Entrar, dependendo do toggle Doador/Instituição direciona para o perfil doador/instituição
    // Continuar com Google, direciona para a tela principal (index)

    const btnPrimary = document.querySelector('.btn-primary');
    const btnGoogle = document.querySelector('.btn-google');

    if (btnPrimary) {
        btnPrimary.addEventListener('click', function () {
            if (btnDoador.classList.contains('active')) {
                window.location.href = 'perfil-doador.html';
            } else {
                window.location.href = 'perfil-instituicao.html';
            }
        });
    }

    if (btnGoogle) {
        btnGoogle.addEventListener('click', function () {
            window.location.href = 'index.html';
        });
    }

    const forgot = document.querySelector('.forgot');

    if (forgot){
        forgot.addEventListener('click', function (){
            window.location.href = 'tela09.html';
        });
    }
});
