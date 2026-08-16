// Arquivo JavaScript do projeto EducaSolidário
// As interações serão desenvolvidas nas próximas etapas.

// Botão ENTRAR / CADASTRAR do menu -> leva para a tela de cadastro de doador
document.addEventListener('DOMContentLoaded', function () {
    const btnEntrar = document.querySelector('.btn-entrar');
    const btnCadastrar = document.querySelector('.btn-cadastrar');

    if (btnEntrar) {
        btnEntrar.addEventListener('click', function () {
            window.location.href = 'login_doador.html';
        });
    }

    if (btnCadastrar) {
        btnCadastrar.addEventListener('click', function () {
            window.location.href = 'cadastro.html';
        });
    }
});

// Troca de abas nas páginas de perfil (doador / instituição)
document.addEventListener('DOMContentLoaded', function () {
    const botoesAbas = document.querySelectorAll('.perfil-abas button');
    const paineis = document.querySelectorAll('.painel');

    if (botoesAbas.length === 0) {
        return; // página sem abas, não faz nada
    }

    botoesAbas.forEach(function (botao) {
        botao.addEventListener('click', function () {
            // tira "ativa" de todas as abas e "visivel" de todos os painéis
            botoesAbas.forEach(function (b) { b.classList.remove('ativa'); });
            paineis.forEach(function (p) { p.classList.remove('visivel'); });

            // liga só a aba clicada e o painel correspondente
            botao.classList.add('ativa');
            const alvo = document.getElementById(botao.dataset.alvo);
            if (alvo) {
                alvo.classList.add('visivel');
            }
        });
    });
});

// Função para iniciar o slideshow do banner 
function iniciarSlideshow() {
    const slides = document.querySelectorAll('.banner .slide');
    let atual = 0;

    setInterval(() => {
        slides[atual].classList.remove('active');
        atual = (atual + 1) % slides.length; // volta pro 0 depois do último
        slides[atual].classList.add('active');
    }, 4000); // troca a cada 4 segundos
}

iniciarSlideshow();
