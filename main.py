from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import csv
import os

class IDTemplate:
    def __init__(self, path, size):
        self.path = path
        self.size = size

def read_data(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                'Name': row['Name'],
                'Title': row['Title'],
                'photo_dir': row['photo_dir'],
                'photo_name': row['photo_name']
            })
    return data

def create_id_card(pdf_file, id_template, data):
    c = canvas.Canvas(pdf_file, pagesize=id_template.size)
    for info in data:
        c.drawImage(id_template.path, 0, 0, width=id_template.size[0], height=id_template.size[1])
        c.setFont("Helvetica", 12)
        c.drawString(30, 50, f"Name: {info['Name']}")
        c.drawString(30, 30, f"Title: {info['Title']}")

        photo_dir = info['photo_dir']
        photo_name = info['photo_name']

        if photo_name:
            photo_path = os.path.join(photo_dir, photo_name)
        else:
            photo_path = photo_dir

        if os.path.exists(photo_path):
            img = ImageReader(photo_path)
            c.drawImage(img, 100, 150, width=100, height=100)  # Adjusted y-coordinate to move image upwards
        c.showPage()
    c.save()

def main():
    id_template = IDTemplate('id_template.png', (204, 324))
    data = read_data('details.csv')
    create_id_card('employee_ids.pdf', id_template, data)

if __name__ == "__main__":
    main()
