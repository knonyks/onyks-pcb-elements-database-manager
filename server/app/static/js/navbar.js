document.querySelector('.navbar').addEventListener('click', (e) => 
{
    if(e.target.classList.contains('navbar-show-hide-btn'))
    {
        e.currentTarget.classList.toggle('open')
    }
})