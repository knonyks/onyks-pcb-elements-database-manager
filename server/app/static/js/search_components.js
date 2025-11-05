let search_container = document.querySelector('.search-container')
let categories = document.querySelectorAll('.category')
let fields = document.querySelectorAll('.field')
let search = document.querySelector('.search')
let table_container = document.querySelector('.table-container')
let tbody = table_container.querySelector('tbody')

let offset = 0
let limit = 10

function get_all_settings()
{
    let result = {}
    result.categories = {}
    result.fields = {}

    for(let category of categories)
    {
        if(category.checked)
        {
            result.categories[category.dataset.name] = true
        }
    }
    for(let field of fields)
    {
        if(field.checked)
        {
            result.fields[field.dataset.name] = true
        }
    }
    result['search'] = search.value
    return result
}

const row_keys = [
    "uuid",
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

async function query_search_elements(config) 
{
    config.limit = limit
    config.offset = offset
    config.search = search.value

    const response = await fetch("/api/get_entries", 
    {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(config)
    })

    const data = await response.json();
    console.log(data)

    for(let row of data)
    {
        let row_ui = create_table_tow(row)
        tbody.appendChild(row_ui)
    }
}   



search_container.addEventListener('click', (e) => 
{
    let truth_table = e.target.classList.contains('category')
    truth_table ||= e.target.classList.contains('field')

    if(truth_table)
    {   
        let result = get_all_settings()
        offset = 0
        tbody.innerHTML = ""
        query_search_elements(result)
        console.log(result)
    }
})



table_container.addEventListener("scroll", () => 
{
    if (table_container.scrollTop + table_container.clientHeight >= table_container.scrollHeight - 1) 
    {
        let result = get_all_settings()
        offset += 10
        result.offset = offset
        query_search_elements(result)
    }
});

   