
let element_form = document.getElementById('myForm');
let confirmationDialog = new Dialog('confirmationDialog')

confirmationDialog.yes = (e) =>
{   
    confirmationDialog.hide()
    element_form.submit()
}

confirmationDialog.no = (e) =>
{
    confirmationDialog.hide()
}

element_form.addEventListener('submit', (e) => 
{
    e.preventDefault();
    confirmationDialog.show()
});