//DIALOGS AND FORM
let elementForm = document.querySelector('#element-form')
let confirmationDialog = new Dialog('confirmation-dialog')
let errorDialog = new Dialog('error-dialog')
let symbolDialog = new Dialog('symbol-dialog')
let footprintDialog = new Dialog('footprint-dialog')

//EXPLORERS
let symbolsExplorer = new Explorer('symbol-explorer', 'svn/symbols', (x) => {return x}, 1)
let footprintExplorer = new Explorer('footprint-explorer', 'svn/footprints', (x) => {return x}, 1)

errorDialog.ok = () => 
{
    errorDialog.hide()
}

//SYMBOL PICKER
document.querySelector('#symbol-picker-btn').addEventListener('click', (e) => 
{
    symbolDialog.ok = () => 
    {
        if(symbolsExplorer.getMarkedFiles().length != 0)
        {
            let library_ref = symbolsExplorer.getMarkedFiles()[0]
            let library_path = symbolsExplorer.getCurrentPath()
            document.querySelector('#library-ref').value = library_ref
            document.querySelector('#library-path').value = library_path
            console.log(library_path, library_ref)
            symbolDialog.hide()
        }
        else
        {
            errorDialog.show()
        }
    }
    symbolsExplorer.init()
    symbolsExplorer.updateExplorerUI()
    symbolDialog.show()
})

//FOOTPRINT PICKER NO 1
document.querySelector('#footprint-picker-1-btn').addEventListener('click', (e) => 
{
    footprintDialog.ok = () => 
    {
        if(footprintExplorer.getMarkedFiles().length != 0)
        {
            let library_ref = footprintExplorer.getMarkedFiles()[0]
            let library_path = footprintExplorer.getCurrentPath()
            document.querySelector('#footprint-ref-1').value = library_ref
            document.querySelector('#footprint-path-1').value = library_path
            footprintDialog.hide()
        }
        else
        {
            errorDialog.show()
        }
    }
    footprintExplorer.init()
    footprintExplorer.updateExplorerUI()
    footprintDialog.show()
})

//FOOTPRINT PICKER NO 2
document.querySelector('#footprint-picker-2-btn').addEventListener('click', (e) => 
{
    footprintDialog.ok = () => 
    {
        if(footprintExplorer.getMarkedFiles().length != 0)
        {
            let library_ref = footprintExplorer.getMarkedFiles()[0]
            let library_path = footprintExplorer.getCurrentPath()
            document.querySelector('#footprint-ref-2').value = library_ref
            document.querySelector('#footprint-path-2').value = library_path
            footprintDialog.hide()
        }
        else
        {
            errorDialog.show()
        }
    }
    footprintExplorer.init()
    footprintExplorer.updateExplorerUI()
    footprintDialog.show()
})

//FOOTPRINT PICKER NO 3
document.querySelector('#footprint-picker-3-btn').addEventListener('click', (e) => 
{
    footprintDialog.ok = () => 
    {
        if(footprintExplorer.getMarkedFiles().length != 0)
        {
            let library_ref = footprintExplorer.getMarkedFiles()[0]
            let library_path = footprintExplorer.getCurrentPath()
            document.querySelector('#footprint-ref-3').value = library_ref
            document.querySelector('#footprint-path-3').value = library_path
            footprintDialog.hide()
        }
        else
        {
            errorDialog.show()
        }
    }
    footprintExplorer.init()
    footprintExplorer.updateExplorerUI()
    footprintDialog.show()
})

elementForm.addEventListener("submit", async (e) => 
{
    e.preventDefault();

    const formData = new FormData(elementForm);

    const clickedButton = e.submitter;
    if (clickedButton && clickedButton.name) 
    {
        formData.append(clickedButton.name, clickedButton.value);
    }

    const response = await fetch(elementForm.action, 
    {
        method: "POST",
        body: formData
    });

    if(response.headers.get("Content-Type")?.includes("application/json"))
    {
        const data = await response.json()
        if(data.mode == "description" && data.status)
        {
            document.querySelector('#description').value = data.content
        }
        else
        {

        }
        console.log(data)
    }
    else
    {
        window.location.href = response.url;
    }


    // const text = await response.text();
    // console.log(text)
    // console.log(response)
    // document.getElementById("response").innerHTML = text;
});


// let element_form = document.getElementById('myForm');
// let confirmationDialog = new Dialog('confirmationDialog')
// confirmationDialog.yes = (e) =>
// {   
//     confirmationDialog.hide()
//     element_form.submit()
// }

// confirmationDialog.no = (e) =>
// {
//     confirmationDialog.hide()
// }

// element_form.addEventListener('submit', (e) => 
// {
//     e.preventDefault();
//     confirmationDialog.show()
// });

// ////////////////////////////////
// let symbol-explorer = new Dialog('symbol-explorer')
// symbol-explorer.ok = (e) =>
// {
//     symbol-explorer.hide()
// }


// let symbolsExplorer = new Explorer('symbol-explorer', 'svn/symbols', (x) => {return x}, 1)
// // let footprintExplorer = new Explorer('symbol-explorer', 'svn/footprints', (x) => {return x}, 1)




// //////
// document.querySelector('#symbol-picker-btn').addEventListener('click', (e) => 
// {
//     symbolsExplorer.init()
//     symbolsExplorer.updateExplorerUI()
//     symbol-explorer.show()
// })  

// // document.querySelector('#symbol-btn').addEventListener('click', (e) => 
// // {
// //     footprintExplorer.init()
// //     footprintExplorer.updateExplorerUI()
// // })  