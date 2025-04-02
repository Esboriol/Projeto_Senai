const statusConfig = {
    colors: {
        'ongoing': '#FFC222',
        'finished': '#28a745',
        'most-urgent': '#dc3545',
        'urgent': '#ff7b07',
        'common': '#007bff',
        'no-status': '#6c757d'
    },
    priority: {
        'most-urgent': 1,
        'urgent': 2,
        'ongoing': 3,
        'common': 4,
        'finished': 5,
        'no-status': 6
    }
};

// Função para ordenar os cards com base no status
function sortCards() {
    const container = document.getElementById('card-container');
    const forms = Array.from(container.querySelectorAll('form'));

    const sortedForms = forms.sort((a, b) => {
        const aStatus = a.querySelector('.status-selector').value;
        const bStatus = b.querySelector('.status-selector').value;
        return statusConfig.priority[aStatus] - statusConfig.priority[bStatus];
    });

    sortedForms.forEach(sortedForm => container.appendChild(sortedForm));
}
function editTitle(icon) {
    const h1 = icon.closest('h1');
    const currentTitle = h1.textContent.trim();
    const newTitle = prompt("Editar título:", currentTitle);

    if (newTitle && newTitle !== currentTitle) {
        h1.textContent = newTitle;
        // Aqui você pode adicionar uma chamada ao backend para salvar o novo título
    }
}
function makeTextEditable() {
    document.querySelectorAll('.editable-text').forEach(element => {
        element.addEventListener('click', function() {
            // Verifica se já há um input de edição ativo
            if (this.querySelector('input')) {
                return;
            }

            const currentText = this.textContent.trim(); // Remove espaços em branco
            const input = document.createElement('input');
            input.type = 'text';
            input.value = currentText; // Exibe o texto atual no input
            input.style.width = `${this.offsetWidth}px`; // Ajusta o tamanho do input
            this.textContent = ''; // Limpa o conteúdo do elemento
            this.appendChild(input); // Adiciona o input ao elemento
            input.focus(); // Foca no input

            // Salva o texto ao perder o foco do input
            input.addEventListener('blur', () => {
                const newText = input.value;
                this.textContent = newText; // Atualiza o texto do elemento

                // Reinsere o ícone de edição
                const editIcon = document.createElement('i');
                editIcon.classList.add('fas', 'fa-pencil-alt', 'edit-title-icon');
                this.appendChild(editIcon);

                // Reaplica o evento de clique no ícone
                editIcon.addEventListener('click', () => {
                    makeTextEditable(); // Reativa a edição
                });

                // Aqui você pode adicionar uma chamada ao backend para salvar o novo texto
                const chamadoId = this.closest('form').querySelector('input[name="chamado_id"]').value;
                fetch('/atualizarDescricao', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ chamadoId, descricao: newText }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('Descrição atualizada com sucesso!');
                    } else {
                        console.error('Erro ao atualizar descrição.');
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                });
            });

            // Salva o texto ao pressionar "Enter"
            input.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    this.blur(); // Remove o foco do input, acionando o evento 'blur'
                }
            });
        });
    });
}

// Função para salvar as alterações no backend
function saveChanges(form) {
    const formData = new FormData(form); // Captura os dados do formulário
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
}

// Função para upload de imagem
function handleImageUpload(input) {
    const container = input.closest('.image-upload-container');
    const preview = container.querySelector('.image-preview');
    const file = input.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            container.classList.add('has-image');
        }
        reader.readAsDataURL(file);
    }
}

// Função para remover imagem
function removeImage(btn) {
    const container = btn.closest('.image-upload-container');
    const input = container.querySelector('.image-input');
    const preview = container.querySelector('.image-preview');

    container.classList.remove('has-image');
    input.value = '';
    preview.src = '';
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Configurar cores dos status
        makeTextEditable(); // Habilita a edição de texto

    // Configura o evento de submit dos formulários
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Impede o envio padrão do formulário
            saveChanges(this); // Chama a função para salvar as alterações
        });
    });
    document.querySelectorAll('.status-selector').forEach(select => {
        select.style.backgroundColor = statusConfig.colors[select.value];

        select.addEventListener('change', function() {
            this.style.backgroundColor = statusConfig.colors[this.value];
        });
    });


    // Configurar upload de imagens
    document.querySelectorAll('.image-input').forEach(input => {
        input.addEventListener('change', function() {
            handleImageUpload(this);
        });
    });

    // Configurar remoção de imagens
    document.querySelectorAll('.delete-image-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            removeImage(this);
        });
    });

    // Ordenar os cards inicialmente
    sortCards();
});