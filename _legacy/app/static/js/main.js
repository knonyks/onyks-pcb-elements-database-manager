const socket = io();

function dashboardUpdateUI()
{
    toast_create('Repozytorium SVN zostało zaktualizowane')
}


socket.on('update', function(data) 
{
    switch(data['source'])
    {
        case 'svn':
            dashboardUpdateUI(data['content'])
    }
});