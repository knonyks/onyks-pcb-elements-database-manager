let edit_btn = document.getElementById('edit-btn')
let duplicate_btn = document.getElementById('duplicate-btn')
let delete_btn = document.getElementById('delete-btn')
let print_list_btn = document.getElementById('print-list-btn')
let generate_labels_btn = document.getElementById('generate-labels-btn')
let details_btn = document.getElementById('details-btn')

let categories_container = document.getElementById('categories')
let fields_container = document.getElementById('fields')
let search_input = document.getElementById('search')
let counter = document.getElementById('counter')
let table_container = document.querySelector('.table-container')
let tbody = table_container.querySelector('tbody')

let offset = 0
let current = 0
let total = 0

const row_keys = [
    "uuid",
    "category",
    "part_name",
    "manufacturer",
    "manufacturer_part_name",
    "datasheet",
    "description",
    "value",
    "availability",
    "library_ref",
    "library_path",
    "footprint_ref_1",
    "footprint_path_1",
    "footprint_ref_2",
    "footprint_path_2",
    "footprint_ref_3",
    "footprint_path_3",
    "created_at"
]

search_input.addEventListener('input', (e) =>
{
    offset = 0
    send_and_process_query(0).then((data) =>
    {
        console.log("Loaded more data:", data)
        update_ui(data)
    })
})

categories_container.addEventListener('click', (e) =>
{
    if(e.target.classList.contains('category'))
    {
        offset = 0
        send_and_process_query(0).then((data) =>
        {
            console.log("Loaded more data:", data)
            update_ui(data)
        })
    }
})

fields_container.addEventListener('click', (e) =>
{
    if(e.target.classList.contains('field'))
    {
        offset = 0
        send_and_process_query(0).then((data) =>
        {
            console.log("Loaded more data:", data)
            update_ui(data)
        })
    }
})


function get_marked_rows()
{
    let marked = []
    for(let row of tbody.querySelectorAll('tr'))
    {
        let checkbox = row.querySelector('td input[type="checkbox"]')
        if(checkbox.checked)
        {
            let uuid = row.querySelector('td:nth-child(2)').innerText
            marked.push(uuid)
        }
    }
    return marked
}

edit_btn.addEventListener('click', () =>
{
    result = get_marked_rows()

    if(result.length > 0)
    {
        window.open(`/element/edit/${result[0]}`, "_blank");
    }
}) 

duplicate_btn.addEventListener('click', () =>
{
    result = get_marked_rows()

    if(result.length > 0)
    {
        window.open(`/element/duplicate/${result[0]}`, "_blank");
    }
})

delete_btn.addEventListener('click', async () =>
{
    result = get_marked_rows()
    offset = 0

    if(result.length != 0)
    {
        let query = {}
        query.uuids = result

        const response = await fetch("/api/remove_entries", 
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(query)
        })

        const data = await response.json();
        console.log("Delete response:", data) 
        
        send_and_process_query(0).then((data) =>
        {
            console.log("Loaded more data:", data)
            update_ui(data)
        })
    }
})

print_list_btn.addEventListener('click', () =>
{
    console.log("Print list button clicked")
})

generate_labels_btn.addEventListener('click', () =>
{
    console.log("Generate labels button clicked")
})

details_btn.addEventListener('click', () =>
{
    result = get_marked_rows()

    if(result.length > 0)
    {
        window.open(`/element/details/${result[0]}`, "_blank");
    }
})

function create_table_tow(row)
{
    let result = document.createElement('tr')
    let checkbox_parent = document.createElement('td')
    let checkbox = document.createElement('input')
    checkbox.type = "checkbox"
    checkbox_parent.appendChild(checkbox)
    result.appendChild(checkbox_parent)
    for(let i=0; i<row_keys.length; i++)
    {
        let column = document.createElement('td')
        column.innerText = row[row_keys[i]]
        result.appendChild(column)
    }
    return result
}

function update_ui(data)
{
    if(offset === 0)
    {
        tbody.innerHTML = ""
        current = data.items.length
        total = data.total_count
        counter.innerText = `${current}/${total}`
    }
    else
    {
        current += data.items.length
        counter.innerText = `${current}/${total}`
    }

    for(let row of data.items)
    {
        let row_ui = create_table_tow(row)
        tbody.appendChild(row_ui)
    }
}

function create_query(offset)
{
    let query = {}
    query.offset = offset
    query.limit = 50
    query.fields = []
    query.categories = []
    for(let category of categories_container.querySelectorAll('.category'))
    {
        if(category.checked)
        {
            query.categories.push(category.dataset.name)
        }
    }
    for(let field of fields_container.querySelectorAll('.field'))
    {
        if(field.checked)
        {
            query.fields.push(field.dataset.name)
        }
    }
    query.search_value = search_input.value
    return query
}

async function send_and_process_query(offset)
{
    let query = create_query(offset)
    console.log("Sending query:", query)
    const response = await fetch("/api/get_entries", 
    {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(query)
    })
    const data = await response.json();
    return data
}

table_container.addEventListener("scroll", () => 
{
    let lastTop = table_container._lastScrollTop || 0
    let currentTop = table_container.scrollTop

    if (currentTop === lastTop) return
    table_container._lastScrollTop = currentTop

    if (currentTop + table_container.clientHeight >= table_container.scrollHeight - 1) 
    {
        offset += 50
        send_and_process_query(offset).then((data) =>
        {
            console.log("Loaded more data:", data)
            update_ui(data)
        })
        console.log('aa')
    }
});

send_and_process_query(0).then((data) =>
{
    console.log("Initial data load:", data)
    update_ui(data)
})