class Dialog 
{
    static openedDialogsCounter = 0
    constructor(id) 
    {
        this.ui = document.getElementById(id);
        this.ok = null
        this.yes = null
        this.no = null
        this.close = null
        this.ui.addEventListener("click", (e) => 
        {
            console.log(e.target)
            if(e.target.classList.contains("yes"))
            {
                this.yes(e)
                return
            }
            if(e.target.classList.contains("no"))
            {
                this.no(e)
                return
            }
            if(e.target.classList.contains("dialog-top-bar-close"))
            {
                this.hide(e)
                return
            }
            if(e.target.classList.contains("ok"))
            {
                this.ok(e)
                return
            }
        })
    }
    show()
    {
        this.ui.style.display = "flex";
        this.ui.classList.add("fadeIn");
        document.body.classList.add("modal");
        Dialog.openedDialogsCounter += 1
    }
    hide()
    {
        if(Dialog.openedDialogsCounter > 0)
            Dialog.openedDialogsCounter -= 1
        if(Dialog.openedDialogsCounter === 0)
            document.body.classList.remove("modal");

        this.ui.classList.add("fadeOut");
        setTimeout(() => 
        {
            this.ui.style.display = "none";
            this.ui.classList.remove("fadeOut");
            this.ui.classList.remove("fadeIn");
        }, 500);
    }
}