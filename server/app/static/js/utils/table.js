class Data_Table
{
    constructor(id) 
    {
        this.ui =  document.querySelector(id)
        this.header = this.ui.querySelector('.data-table-header')
        this.header_columns = this.ui.querySelectorAll('.data-table-header-column')
        this.min_width = 50;
        this.resizing = 
        {
            is_resizing: false,
            current_column: null,
        }
        this.rows = this.ui.querySelectorAll('.data-table-row');
    }
    __header_init()
    {
        this.ui.addEventListener('mousedown', (e) => 
        {
            if(e.target.classList.contains('data-table-header-column-resize-handle'))
            {
                this.resizing.is_resizing = true;
                this.resizing.current_column = e.target.parentElement.querySelector('.data-table-header-column-content');
            }
        });

        this.ui.addEventListener('mousemove', (e) => 
        {
            if(this.resizing.is_resizing == true)
            {
                const new_width = e.clientX - this.resizing.current_column.getBoundingClientRect().left;
                this.resizing.current_column.style.width = new_width + 'px';
                for(const row of this.ui.querySelectorAll('.data-table-row'))
                {
                    const cells = row.querySelectorAll('div');
                    // console.log(cells[parseInt(e.target.parentElement.dataset['index']) - 1]);
                    cells[parseInt(e.target.parentElement.dataset['index']) - 1].style.width = new_width + 'px';
                }
            }
        });

        this.ui.addEventListener('mouseup', (e) => 
        {
            if(this.resizing.is_resizing == true)
            {
                this.resizing.is_resizing = false;
            }
        });
    }
    init()
    {
        this.__header_init()
    }
}

