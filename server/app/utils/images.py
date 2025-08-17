from PIL import Image, ImageDraw, ImageFont

def createDatabaseConfigImage(dbConfig, sourcePath, destinationPath):
    image = Image.open(sourcePath)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 13)
    except:
        font = ImageFont.load_default()
    draw.text((105, 108), dbConfig["name"], fill="black", font=font) 
    draw.text((105, 135), dbConfig["host"], fill="black", font=font)
    draw.text((105, 163), dbConfig["username"], fill="black", font=font) 

    draw.text((340, 75), 'altium', fill="black", font=font) 
    draw.text((340, 135), str(dbConfig["port"]), fill="black", font=font) 
    draw.text((340, 165), dbConfig["password"], fill="black", font=font) 
    image.save(destinationPath)




