document.addEventListener("DOMContentLoaded", () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    const toast = document.querySelector("[data-toast]");
    if (toast) {
        setTimeout(() => toast.classList.add("opacity-0"), 3500);
    }

    const registrationForm = document.querySelector("#student-registration-form");
    if (registrationForm) {
        registrationForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const formData = new FormData(registrationForm);
            const payload = Object.fromEntries(formData.entries());
            try {
                const response = await fetch("/api/registrations", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    throw new Error("Unable to submit registration");
                }
                registrationForm.reset();
                alert("Registration submitted successfully!");
                window.location.reload();
            } catch (error) {
                alert(error.message);
            }
        });
    }
});

