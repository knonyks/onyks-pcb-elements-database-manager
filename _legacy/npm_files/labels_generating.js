const PDFDocument = require('pdfkit');
const blobStream = require('blob-stream');
var QRCode = require('qrcode')

let blob;
let doc = null; 
let stream = null;

const a4_width = 595.28
const a4_height = 841.89
const label_width = a4_width / 2
const label_height = a4_height / 4

let print_list_btn = document.getElementById('print-list-btn')
let generate_labels_btn = document.getElementById('generate-labels-btn')

function get_rows()
{
    let marked = []
    for(let row of tbody.querySelectorAll('tr'))
    {
        let checkbox = row.querySelector('td input[type="checkbox"]')
        if(checkbox.checked)
        {
            let row_data = {}
            let row_ui = row.querySelectorAll('td')
            let counter = 1
            for(let el of row_keys)
            {
                row_data[el] = row_ui[counter].textContent
                counter += 1;
            }
            marked.push(row_data)
        }
    }
    return marked
}

async function urlToBase64(url) 
{
    const response = await fetch(url);
    if (!response.ok) throw new Error("Error");
    const blob = await response.blob();
    return new Promise((resolve, reject) => {
    const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

async function invertBase64Image(base64) {
  return new Promise((resolve) => {
    const img = new Image();
    img.crossOrigin = "Anonymous"; // jeśli URL CORS
    img.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;

      // odwracamy kolory
      for (let i = 0; i < data.length; i += 4) {
        data[i] = 255 - data[i];       // R
        data[i+1] = 255 - data[i+1];   // G
        data[i+2] = 255 - data[i+2];   // B
        // alpha pozostaje bez zmian
      }

      ctx.putImageData(imageData, 0, 0);
      resolve(canvas.toDataURL()); // nowy base64
    };
    img.src = base64;
  });
}

let base64Image;
let inverted;

(async () => 
{
    base64Image = await urlToBase64(`${window.location.protocol}//${window.location.host}` + '/static/img/logo.png');
    inverted = await invertBase64Image(base64Image);
})()



async function generate_label(doc, data, index)
{
    const relative_index = index % 8
    const relative_top_left_corner_x = (relative_index % 2) * label_width
    const relative_top_left_corner_y = Math.floor(relative_index / 2) * label_height

    if (index > 7)
    {
        doc.addPage();
    }

    const qr_uuid = await QRCode.toDataURL(data.uuid, {
        errorCorrectionLevel: 'H',
        margin: 0
    });

    if(relative_index % 2 == 0 && relative_index < 6)
    {
        doc.moveTo(0, label_height * ((relative_index / 2) + 1))
        .lineTo(label_width, label_height * ((relative_index / 2) + 1))
        .lineTo(label_width, label_height * (relative_index / 2))
        .dash(5, {space: 10})
        .stroke()
        .save()
    }
    else if(relative_index < 7 && relative_index % 2 != 0)
    {
        doc.moveTo(label_width, label_height * ((relative_index + 1)/2))
        .lineTo(label_width * 2, label_height * ((relative_index + 1)/2))
        .dash(5, {space: 10})
        .stroke()
        .save()
    }
    else
    {
        doc.moveTo(label_width, label_height * ((relative_index / 2) + 1))
        .lineTo(label_width, label_height * (relative_index / 2))
        .dash(5, {space: 10})
        .stroke()
        .save()
    }

    doc.image(inverted, relative_top_left_corner_x + 10, relative_top_left_corner_y + 10, { width: 70 }); 
    doc.image(qr_uuid, relative_top_left_corner_x + 10, relative_top_left_corner_y + 5 + 50, { width: 70 });
    doc.save() 

    doc.fontSize(8);
    doc.text("Manufacturer", relative_top_left_corner_x + 85, relative_top_left_corner_y + 10)
    doc.save() 

    doc.fontSize(16);
    doc.text(data.manufacturer, relative_top_left_corner_x + 85 - 1, relative_top_left_corner_y + 10 + 10)
    doc.save() 

    doc.fontSize(8);
    doc.text("Part Name", relative_top_left_corner_x + 85, relative_top_left_corner_y + 15 + 10 + 16)
    doc.save() 

    doc.fontSize(25);
    doc.text(data.part_name, relative_top_left_corner_x + 85 - 1, relative_top_left_corner_y + 10 + 15 + 5 + 16 + 5)
    doc.save() 

    doc.fontSize(8);
    doc.text("Value", relative_top_left_corner_x + 85 - 1, relative_top_left_corner_y + 10 + 15 + 5 + 16 + 5 + 25)
    doc.save() 

    doc.fontSize(12);
    doc.text(data.value, relative_top_left_corner_x + 85 - 1, relative_top_left_corner_y + 10 + 15 + 5 + 16 + 5 + 35)
    doc.save() 

    doc.fontSize(8);
    doc.text("UUID", relative_top_left_corner_x + 85 - 1, relative_top_left_corner_y + 10 + 15 + 5 + 16 + 5 + 50)
    doc.save() 

    doc.fontSize(10);
    doc.text(data.uuid, relative_top_left_corner_x + 85 - 1, relative_top_left_corner_y + 10 + 15 + 5 + 16 + 5 + 60, {width: 200})
    doc.save() 

    doc.fontSize(8);
    doc.text("Description", relative_top_left_corner_x + 10, relative_top_left_corner_y + 10 + 15 + 5 + 16 + 5 + 60 + 20)
    doc.save() 

    description = data.description

    if(description.length > 550)
    {
        const lastSpaceIndex = description.lastIndexOf(' ', 550);
        if (lastSpaceIndex > 0) {
            description = description.substring(0, lastSpaceIndex) + '...';
        } else {
            description = description.substring(0, 550) + '...';
        }
    }

    doc.fontSize(7);
    doc.text(description, relative_top_left_corner_x + 10, relative_top_left_corner_y + 10 + 15 + 5 + 16 + 5 + 60 + 20 + 10, {width: label_width - 20, align: 'justify'})
    doc.save() 
}

async function generate_labels(data)
{
    doc = new PDFDocument({size: 'A4', margins: { top: 0, bottom: 0, left: 0, right: 0 }});
    stream = doc.pipe(blobStream());

    for(let i=0; i<data.length; i++)
    {
        await generate_label(doc, data[i], i);
    }

    doc.end();

    stream.on("finish", function() 
    {
        let downloader = document.createElement('a')
        downloader.style.display = 'none'
        document.querySelector('body').appendChild(downloader)
        blob = stream.toBlob("application/pdf");
        var url = window.URL.createObjectURL(blob);
        downloader.href = url;
        downloader.download = 'onyks-labels-' + new Date().toISOString().replace(/[:.]/g, '-') + '.pdf'
        downloader.click();
        window.URL.revokeObjectURL(url);
    });
}

generate_labels_btn.addEventListener('click', () =>
{
    let data = get_rows()
    if(data.length > 0)
    {
        generate_labels(data)
    }
})





print_list_btn.addEventListener('click', () =>
{
    let data = get_rows()
    console.log(data)
})