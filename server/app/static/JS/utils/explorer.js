class Explorer 
{
    constructor(id, path, filter) 
    {
        this.ui =
        {
            main: document.getElementById(id),
            container: document.getElementById(id).querySelector(".explorer-content"),
            paths: document.getElementById(id).querySelector(".explorer-path")
        }
        this.ui.main.manager = this
        this.pathChain = path.split('/')
        this.filter = filter
        this.ui.main.addEventListener("click", this.explorerEvent)
        this.ui.main.addEventListener("dblclick", this.explorerEvent)
    }
    init()
    {
        this.initSocket()
    }
    initSocket()
    {
        this.socket = io()
        this.socket.on('explorer-files', (data) =>
        {  
            for(let file of data)
            {
                explorer.appendFile(file[0], file[1])
            }
        })
    }
    explorerEvent(e)
    {
        if(e.type === "click")
        {
            if(e.target.classList.contains("explorer-path-obj"))
            {
                let id = parseInt(e.target.dataset.setId)
                this.manager.pathChain = this.manager.pathChain.slice(0, id + 1)
                this.manager.updateExplorerUI()
            }
        }
        else if(e.type === "dblclick")
        {
            console.log(e.target)
            //GO INSIDE TO THE FOLDER OR PCBLIB/SCHLIB FILE
            if(e.target.classList.contains("explorer-content-obj"))
            {   
                if(e.target.classList.contains("folder") || e.target.classList.contains('pcblib') || e.target.classList.contains('schlib'))
                {
                    this.manager.pathChain.push(e.target.querySelector('.explorer-content-obj-name').innerText)
                    this.manager.updateExplorerUI()
                }
            }
            else if(e.target.classList.contains("explorer-content-obj-name"))
            {
                console.log(e.target)
                this.manager.pathChain.push(e.target.innerText)
                this.manager.updateExplorerUI()
            }
        }
    }
    updateExplorerUI()
    {
        this.ui.paths.innerHTML = ''
        this.ui.container.innerHTML = ''
        for(let i = 0; i < this.pathChain.length; i++)
        {
            let ui = document.createElement('div')
            ui.classList.add('explorer-path-obj')
            ui.dataset.setId = i
            ui.innerText = this.pathChain[i]
            this.ui.paths.appendChild(ui)
        }
        this.socket.emit('explorer-get-files', {'path': this.pathChain.join('/')})
    }




    // explorerEvent(e)
    // {
    //     if(e.type === "click")
    //     {
    //         if(e.target.classList.contains("explorer-path-obj"))
    //         {
    //             let id = parseInt(e.target.dataset.setId)
    //             this.manager.pathChain = this.manager.pathChain.slice(0, id + 1)
    //             this.manager.socket.emit('explorer-get-files', {'path': this.manager.pathChain.join('/')})
    //         }
    //     }







    //     // else if(e.type === "dblclick")
    //     // {
    //     //     if(e.target.classList.contains("explorer-content-obj"))
    //     //     {
    //     //         console.log(2)
    //     //         if(e.target.classList.contains("folder"))
    //     //         {
    //     //             console.log(this.manager.appendPath(e.target.querySelector('.explorer-content-obj-name').innerText))
    //     //             // this.appendPath(e.target.querySelector('.explorer-content-obj-name').innerText)
    //     //             console.log(this.manager.pathChain.join('/'))
    //     //             this.manager.removeAllFiles()
    //     //             this.manager.socket.emit('explorer-get-files', {'path': this.manager.pathChain.join('/')})

    //     //         }
    //     //     }
    //     // }
    // }











    // removeAllFiles()
    // {
    //     this.ui.container.innerHTML = ''
    // }
    appendFile(name, type)
    {
        let ui = {main: document.createElement('div'), name: document.createElement('div'), infoBtn: document.createElement('div')}
        ui.main.classList.add('explorer-content-obj')
        ui.main.classList.add(type)
        ui.name.innerText = name
        ui.name.classList.add('explorer-content-obj-name')
        ui.infoBtn = document.createElement('div')
        ui.infoBtn.classList.add('explorer-content-obj-info-btn')
        ui.main.appendChild(ui.name)
        ui.main.appendChild(ui.infoBtn)
        this.ui.container.appendChild(ui.main)
    }
    // appendPath(path)
    // {
    //     this.pathChain.push(path)
    //     let ui = document.createElement('div')
    //     ui.classList.add('explorer-path-obj')
    //     ui.dataset.setId = this.pathChain.length - 1
    //     ui.innerText = path
    //     this.ui.paths.appendChild(ui)
    // }
    // removeLastPath()
    // {
    //     if(this.pathChain.length > 1)
    //         this.pathChain.pop()
    //     this.ui.paths.removeChild(this.ui.paths.lastChild)
    // }



    // updateUI()
    // {
    //     this.ui.paths.innerHTML = ''
    //     for(let i = 0; i < this.pathChain.length; i++)
    //     {
    //         let ui = document.createElement('div')
    //         ui.classList.add('explorer-path-obj')
    //         ui.dataset.setId = i
    //         ui.innerText = this.pathChain[i]
    //         this.ui.paths.appendChild(ui)
    //     }

    // }
}