document.addEventListener("DOMContentLoaded", () => {
    const analyzerForm = document.querySelector(".analyzer-form");

    if (analyzerForm) {
        analyzerForm.addEventListener("submit", (event) => {
            const submitter = event.submitter;

            // DOCX download button-க்கு "Analyzing..." தேவையில்லை
            if (
                submitter &&
                submitter.classList.contains("secondary-button")
            ) {
                return;
            }

            if (submitter) {
                setTimeout(() => {
                    submitter.disabled = true;
                    submitter.textContent = "Analyzing...";
                }, 0);
            }
        });
    }
});