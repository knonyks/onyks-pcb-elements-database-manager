function toast_create(message, top_invisible, top_visible)
{
    let animation_name = 'custom_animation_' + Date.now();
    let toast_keyframe = `
    @keyframes ${animation_name} {
        0% { top: ${top_invisible}px; }
        20% { top: ${top_visible}px; }
        80% { top: ${top_visible}px; }
        100% { top: ${top_invisible}px; }
    }
    `;

    let styleSheet = document.createElement('style');
    styleSheet.type = 'text/css';
    styleSheet.innerHTML = toast_keyframe;
    document.head.appendChild(styleSheet);

    let toast = document.createElement('div')
    toast.style.animation = `${animation_name} 5s ease-in-out forwards`;
    toast.classList.add('toast')
    toast.innerText = message
    document.querySelector('body').appendChild(toast)
    setTimeout(() => {toast.remove()}, 5000)
}

