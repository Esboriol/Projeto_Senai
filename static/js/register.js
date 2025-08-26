function previewImage(event) {
    const fileInput = event.target;
    const files = fileInput.files;
    const container = document.getElementById("image-container");

    // Limpa a imagem anterior, se houver
    container.innerHTML = "";

    if (files.length > 0) {
        const file = files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            const img = document.createElement("img");
            img.src = e.target.result;
            img.alt = "Pré-visualização da imagem";
            img.style.maxWidth = "100px";
            img.style.display = "block";
            img.style.marginTop = "10px";

            container.appendChild(img);
        };

        reader.readAsDataURL(file);
    }
}
