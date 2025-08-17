function toast_create(message)
{
    let toast = document.createElement('div')
    toast.classList.add('toast')
    toast.innerText = message
    document.querySelector('body').appendChild(toast)
    setTimeout(() => {toast.remove()}, 5000)
}

