import openpyxl
import requests


def generate_file(structure: dict) -> str:
    """
    :param structure - Структура отчёта

    Функция должна возвращать имя сохранённого файла
    """
    book = openpyxl.Workbook()
    sheet = book.worksheets[0]
    sheet['A1'] = "Номер отчета"
    sheet['B1'] = "Фотография"
    sheet['C1'] = "Название фотографии"
    sheet['M1'] = "URL фотографии"
    sheet['A5'] = "Номер сегмента"
    sheet['B5'] = "Расстояние от начала сегмента"
    sheet['C5'] = "Расстояние до конца сегмента"
    sheet['D5'] = "Имя"
    sheet['E5'] = "Значение"
    sheet['F5'] = "Название свойства"
    sheet['G5'] = "Значение свойства"

    img_data = requests.get(structure['photo_url']).content
    with open('image.jpg', 'wb') as handler:
        handler.write(img_data)

    img = openpyxl.drawing.image.Image('image.jpg')
    sheet.add_image(img, 'M2')
    sheet[2][0].value = structure['report_id']
    sheet[2][1].value = structure['photo_type']
    sheet[2][2].value = structure['photo_name']

    row = 6
    for segment in structure["segments"]:
        for property in segment["properties"]:
            sheet[row][0].value = segment["segment_id"]
            sheet[row][1].value = segment["offset"]
            sheet[row][2].value = segment["len"]
            sheet[row][3].value = property["name"]
            sheet[row][4].value = property["title"]
            sheet[row][5].value = property["value"]["name"]
            sheet[row][6].value = property["value"]["title"]
            row += 1

    book.save("report.xlsx")
    book.close()
    return "report.xlsx"


pass
