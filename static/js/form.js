function previewImage(event) {
    const fileInput = event.target;
    const files = fileInput.files;
    const container = document.getElementById("image-container");

    if (files.length > 0) {
        Array.from(files).forEach((file, index) => {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                // Cria um novo contêiner de pré-visualização
                const div = document.createElement("div");
                div.classList.add("image-preview");

                // Exibe a imagem
                const img = document.createElement("img");
                img.src = e.target.result;
                img.alt = "Pré-visualização da imagem";
                img.style.maxWidth = "100px"; // Tamanho máximo da imagem

                // Adiciona a imagem ao contêiner
                div.appendChild(img);

                // Cria um novo campo para enviar mais imagens
                const newFileInput = document.createElement("input");
                newFileInput.type = "file";
                newFileInput.name = "arquivo[]";
                newFileInput.accept = "image/*,audio/*,video/*";
                newFileInput.onchange = previewImage; // Torna esse campo funcional para mais imagens

                // Adiciona o novo input à div
                div.appendChild(newFileInput);

                // Adiciona a div ao container
                container.appendChild(div);
            };

            reader.readAsDataURL(file);
        });
    }
}
