let explorer = new Explorer('explorer', 'svn', (x) => {return x})


explorer.init()
explorer.updateExplorerUI()

// explorer.removeAllFiles()

// socket.emit('explorer-get-files', {'path': 'svn'})

// socket.on('explorer-files', (data) =>
// {  
//     for(let file of data)
//     {
//         explorer.appendFile(file[0], file[1])
//         console.log(file)
//     }
// })