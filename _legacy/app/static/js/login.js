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
    if (data.success) 
    {
        window.location.href = data.redirect;
    } 
    else 
    {
        toast_create("Błąd! Problem z logowaniem.", -500, 20);
    }
});