import PIL.Image

# https://stackoverflow.com/questions/23064549/get-date-and-time-when-photo-was-taken-from-exif-data-using-pil
def read_image_date(image):
    img = PIL.Image.open(image)
    exif_data = img._getexif()

    date_taken = None

    try:
        date_taken = exif_data[36867]
    except:
        print(image)
        print(exif_data)

    return date_taken

def parse_exif_date(file, exif_date):
    try:
        year, month, day_hour, minute, second = exif_date.split(":")
        day = day_hour.split(" ")[0]
        return year, month, day, exif_date
    except:
        print(exif_date)
        print(file)