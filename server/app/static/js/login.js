document.getElementById("login-form").addEventListener("submit", async function(e) 
{
    e.preventDefault();

            const formData = new FormData(this);
            const response = await fetch("/login", 
            {
                method: "POST",
                body: formData,
                headers: { "X-Requested-With": "XMLHttpRequest" }
            });

            const data = await response.json();
            console.log(data)
            if (data.success) 
            {
                window.location.href = data.redirect;
            } 
            else 
            {
                // toast_create("Error")
                Swal.fire({
                    title: 'Ważne okno',
                    text: 'Nie możesz zamknąć tego okna inaczej niż klikając przycisk',
                    icon: 'info',
                    showCancelButton: false,      // brak przycisku anuluj
                    confirmButtonText: 'Rozumiem',
                    allowOutsideClick: false,     // nie zamykaj po kliknięciu poza modal
                    allowEscapeKey: false,        // nie zamykaj przyciskiem ESC
                    }).then((result) => {
                    if (result.isConfirmed) {
                        console.log('Użytkownik kliknął przycisk');
                    }
                    });

            }
});