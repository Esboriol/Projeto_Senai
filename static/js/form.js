function previewImage(event) {
    const fileInput = event.target;
    const files = fileInput.files;
    const container = document.getElementById("image-container");

    // Verifique quantas imagens já foram adicionadas
    const currentImages = container.getElementsByClassName("image-preview").length;

    // Se já atingiu o limite de 3 imagens, não adiciona mais nada
    if (currentImages >= 3) {
        alert("Você pode adicionar no máximo 3 imagens!");
        return; // Não adiciona mais imagens se já atingiu o limite
    }

    if (files.length > 0) {
        Array.from(files).forEach((file) => {
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

                // Cria um novo campo para enviar mais imagens, mas só se for menos de 3
                if (currentImages + 1 < 3) { // Só adiciona o input para mais imagens se não tiver 3
                    const newFileInput = document.createElement("input");
                    newFileInput.type = "file";
                    newFileInput.name = "arquivo[]";
                    newFileInput.accept = "image/*,audio/*,video/*";
                    newFileInput.onchange = previewImage; // Torna esse campo funcional para mais imagens

                    // Adiciona o novo input à div
                    div.appendChild(newFileInput);
                }

                // Adiciona a div ao container
                container.appendChild(div);
            };

            reader.readAsDataURL(file);
        });
    }
}
