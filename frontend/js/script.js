// Arquivo JavaScript do projeto EducaSolidário
// As interações serão desenvolvidas nas próximas etapas.

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