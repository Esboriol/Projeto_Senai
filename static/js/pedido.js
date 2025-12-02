    const statusColors = {
        'ongoing': '#FFC222',
        'finished': '#28a745',
        'most-urgent': '#dc3545',
        'urgent': '#ff7b07',
        'common': '#007bff',
        'no-status': '#6c757d'
    };

    const statusPriority = {
        'ongoing': 1,
        'most-urgent': 2,
        'urgent': 3,
        'common': 4,
        'finished': 5,
        'no-status': 6
    };

    // Função para ordenar os cards com base no status
    function sortCards() {
        const container = document.getElementById('card-container');
        const forms = Array.from(container.querySelectorAll('form'));

        const sortedForms = forms.sort((a, b) => {
            const aStatus = a.querySelector('.status-select select').value;
            const bStatus = b.querySelector('.status-select select').value;
            return statusPriority[aStatus] - statusPriority[bStatus];
        });

        sortedForms.forEach(sortedForm => container.appendChild(sortedForm));
    }

    // Variável para guardar o índice do chamado selecionado
    let chamadoSelecionadoIndex = null;

    // Tornar a função global para funcionar no onchange do HTML
    window.onSelectedCard = function(index, status) {
        if (status === 'finished') {
            chamadoSelecionadoIndex = index;
            abrirModal();
        }
    }

    // Funções do modal
    function abrirModal() {
        document.getElementById("emailModal").style.display = "block";
    }

    function fecharModal() {
        document.getElementById("emailModal").style.display = "none";
    }

    function confirmarEmail() {
        const email = document.getElementById("emailInput").value;
        if (!email) {
            alert("Digite um email válido!");
            return;
        }
        // Preenche o campo hidden do form com o email
        document.getElementById(`email-finalizador-${chamadoSelecionadoIndex}`).value = email;
        fecharModal();
    }

    // Inicializa ao carregar a página
    document.addEventListener('DOMContentLoaded', () => {
        const container = document.getElementById('card-container');
        const cards = container.querySelectorAll('.card');

        cards.forEach(card => {
            const select = card.querySelector('.status-select select');

            // Define a cor de fundo do seletor com base no status atual
            select.style.backgroundColor = statusColors[select.value];

            // Atualiza o card quando o status for alterado
            select.addEventListener('change', (event) => {
                const newStatus = event.target.value;
                select.style.backgroundColor = statusColors[newStatus];
            });
        });

        // Ordena os cards ao carregar a página
        sortCards();
    });