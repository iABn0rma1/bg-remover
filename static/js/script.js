document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const resultDiv = document.getElementById("result");
    const loaderDiv = document.getElementById("loader");

    resultDiv.classList.add("hidden");
    loaderDiv.classList.remove("hidden");

    try {
        const response = await fetch("/remove-background/", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            document.getElementById("outputImage").src = url;
            loaderDiv.classList.add("hidden");
            resultDiv.classList.remove("hidden");
        } else {
            throw new Error("Image processing failed.");
        }
    } catch (error) {
        alert("Failed to process the image. Please try again.");
        loaderDiv.classList.add("hidden");
    }
});
