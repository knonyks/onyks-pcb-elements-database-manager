class Explorer 
{
    constructor(id, path, filter, pathStartIndex=0) 
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
        this.pathStartIndex = pathStartIndex
        this.multifileMarking = false
    }
    init()
    {
        this.initSocket()
    }
    getMarkedFiles()
    {
        let list = this.ui.container.querySelectorAll('.marked')
        let result = []
        for(let i of list)
        {
            result.push(i.querySelector('.explorer-content-obj-name').innerText)
        }
        return result
    }
    getCurrentPath()
    {
        return this.pathChain.slice(this.pathStartIndex, this.pathChain.length).join('/')
    }
    initSocket()
    {
        this.socket = io()
        this.socket.on('explorer-files', (data) =>
        {   
            for(let file of data)
            {
                this.appendFile(file[0], file[1])
            }
        })
    }
    __markObj(src)
    {
        if(src.classList.contains('symbol') || src.classList.contains('footprint'))
        {
            let marked = this.ui.container.querySelector('.marked')
            if(marked == null)
            {
                src.classList.add('marked')
            }
            else
            {
                console.log(src, marked, src == marked)
                if(src == marked)
                {
                    src.classList.remove('marked')
                }
                else
                {
                    marked.classList.remove('marked')
                    src.classList.add('marked')
                }
                // marked.classList.remove('marked')
                // src.classList.add('marked')
            }



        }
        
        // if(src.manager.ui.container.querySelector('marked') != null)
        // {
        //     src.manager.ui.container.querySelector('marked').classList.remove('marked')
            
        // }
        // else
        // {

        // }
    }
    explorerEvent(e)
    {
        if(e.type === "click")
        {
            //PATH
            if(e.target.classList.contains("explorer-path-obj"))
            {
                let id = parseInt(e.target.dataset.setId)
                this.manager.pathChain = this.manager.pathChain.slice(0, id + 1)
                this.manager.updateExplorerUI()
            }
            //MARK THE CHOOSEN SYMBOL
            else if(e.target.classList.contains("explorer-content-obj"))
            {  
                this.manager.__markObj(e.target)
                // if(this.manager.ui.container.querySelector('marked') != null)
                // {
                //     this.manager.ui.container.querySelector('marked').classList.remove('marked')
                // }
                // e.target.classList.add('marked')
                // if(this.manager.querySelector('marked'))
                // {

                // }
            }
            else if(e.target.classList.contains("explorer-content-obj-name"))
            {
                this.manager.__markObj(e.target.parentElement)
            }
        }
        else if(e.type === "dblclick")
        {
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
                let parent = e.target.parentElement
                let condition = parent.classList.contains("folder")
                condition |= parent.classList.contains('pcblib')
                condition |= parent.classList.contains('schlib')
                if(condition)
                {
                    this.manager.pathChain.push(e.target.innerText)
                    this.manager.updateExplorerUI()
                }
            }
        }
    }
    updateExplorerUI()
    {
        this.ui.paths.innerHTML = ''
        this.ui.container.innerHTML = ''
        for(let i = this.pathStartIndex; i < this.pathChain.length; i++)
        {
            let ui = document.createElement('div')
            ui.classList.add('explorer-path-obj')
            ui.dataset.setId = i
            ui.innerText = this.pathChain[i]
            this.ui.paths.appendChild(ui)
        }
        this.socket.emit('explorer-get-files', {'path': this.pathChain.join('/')})
    }
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
}