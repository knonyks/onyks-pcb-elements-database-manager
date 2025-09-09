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

////////////////////////////////
let explorerDialog = new Dialog('explorerDialog')
explorerDialog.ok = (e) =>
{
    explorerDialog.hide()
}

let explorer = new Explorer('explorer', 'svn/symbols', (x) => {return x})
explorer.init()
explorer.updateExplorerUI()