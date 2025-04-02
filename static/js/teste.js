document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.querySelector('.search-bar input');
    const tableRows = document.querySelectorAll('.table-container tbody tr');
    const resultsCount = document.getElementById('results-count');
    const prevPageButton = document.getElementById('prev-page');
    const nextPageButton = document.getElementById('next-page');
    const currentPageElement = document.getElementById('current-page');

    let currentPage = 1;
    const rowsPerPage = 5; // Exibir 5 linhas por página
    let visibleRows = []; // Armazenar as linhas visíveis globalmente

    searchInput.addEventListener('input', function () {
        currentPage = 1; // Resetar para a primeira página ao pesquisar
        filterTable();
    });

    prevPageButton.addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            updatePagination();
        }
    });

    nextPageButton.addEventListener('click', function () {
        const totalPages = Math.ceil(visibleRows.length / rowsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            updatePagination();
        }
    });

    function filterTable() {
        const searchTerm = searchInput.value.toLowerCase();
        visibleRows = []; // Resetar as linhas visíveis

        tableRows.forEach(row => {
            const description = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
            if (description.includes(searchTerm)) {
                visibleRows.push(row); // Adicionar à lista de linhas visíveis
            }
        });

        // Esconder todas as linhas inicialmente
        tableRows.forEach(row => row.style.display = 'none');

        updatePagination();
        updateResultsCount();
    }

    function updatePagination() {
        const totalPages = Math.ceil(visibleRows.length / rowsPerPage);
        currentPageElement.textContent = `Página ${currentPage}`;
        prevPageButton.disabled = currentPage === 1;
        nextPageButton.disabled = currentPage === totalPages;

        // Calcular índices da página atual
        const startIndex = (currentPage - 1) * rowsPerPage;
        const endIndex = startIndex + rowsPerPage;

        // Mostrar apenas as linhas da página atual
        visibleRows.forEach((row, index) => {
            if (index >= startIndex && index < endIndex) {
                row.style.display = ''; // Exibir linha
            } else {
                row.style.display = 'none'; // Esconder linha
            }
        });
    }

    function updateResultsCount() {
        const startIndex = (currentPage - 1) * rowsPerPage + 1;
        const endIndex = Math.min(startIndex + rowsPerPage - 1, visibleRows.length);
        resultsCount.textContent = `Exibindo ${startIndex} a ${endIndex} de ${visibleRows.length}`;
    }

    // Inicializar
    filterTable();
});