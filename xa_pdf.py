import csv
import datetime
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet

# Data from CSV
with open('C:/Users/jsbae/csvToPdf/Sample Receipting.csv', "r") as csvfile:
    data = list(csv.reader(csvfile))


def split_data(data):
    list_of_lists = []
    new_list = []
    donor = data[0][0]
    data_without_cat = data[1:]

    for index, row in enumerate(data_without_cat):
        # if new donor
        if row[0] != donor:
            list_of_lists.append(new_list)
            new_list = []
            donor = row[0]
            new_list.append(data[0])
            new_list.append(row)
        # if same donor
        else:
            new_list.append(row)
            # figure out how to get the last index value
            if index == (len(data_without_cat)-1):
                list_of_lists.append(new_list)
    list_of_lists.pop(0)
    return list_of_lists


def make_pdf(donor_data):
    donor = donor_data[1][0]
    elements = []

    # PDF Text
    # PDF Text - Styles
    styles = getSampleStyleSheet()
    styleNormal = styles['Normal']
    styleNormal.wordWrap = 'LTR'

    # PDF Text - Content
    line1 = 'XA Giving Receipt'
    line2 = 'Date: {}'.format(datetime.datetime.now().strftime("%m-%d-%y"))
    line3 = 'Receipt for: {}'.format(f"{donor}")
    line4 = 'Thank you for your generous giving! This receipt is for your tax purposes'

    elements.append(Paragraph(line1, styleNormal))
    elements.append(Paragraph(line2, styleNormal))
    elements.append(Paragraph(line3, styleNormal))
    elements.append(Spacer(inch, .25 * inch))
    elements.append(Paragraph(line4, styleNormal))
    elements.append(Spacer(inch, .25 * inch))

    # PDF Table
    # PDF Table - Styles
    # [(start_column, start_row), (end_column, end_row)]
    all_cells = [(0, 0), (-1, -1)]
    header = [(0, 0), (-1, 0)]
    column0 = [(0, 0), (0, -1)]
    column1 = [(1, 0), (1, -1)]
    column2 = [(2, 0), (2, -1)]
    column3 = [(3, 0), (3, -1)]
    column4 = [(4, 0), (4, -1)]
    column5 = [(5, 0), (5, -1)]
    table_style = TableStyle([
        ('VALIGN', all_cells[0], all_cells[1], 'TOP'),
        ('LINEBELOW', header[0], header[1], 1, colors.black),
        ('ALIGN', column0[0], column0[1], 'LEFT'),
        ('ALIGN', column1[0], column1[1], 'LEFT'),
        ('ALIGN', column2[0], column2[1], 'LEFT'),
        ('ALIGN', column3[0], column3[1], 'RIGHT'),
        ('ALIGN', column4[0], column4[1], 'RIGHT'),
        ('ALIGN', column5[0], column5[1], 'LEFT'),
    ])

    # PDF Table - Column Widths
    colWidths = [
        2.5 * cm,  # Column 0
        2.5 * cm,  # Column 1
        2.0 * cm,  # Column 2
        3.0 * cm,  # Column 3
        2.5 * cm,  # Column 4
        2.5 * cm,  # Column 5
    ]

    wrappedData = [[Paragraph(cell, styleNormal) for cell in row] for row in data]

    # Add table to elements
    t = Table(wrappedData, colWidths=colWidths)

    # styles cell entries
    t.setStyle(table_style)
    elements.append(t)

    # Generate PDF
    archive_pdf = SimpleDocTemplate(
        f'C:/Users/jsbae/csvToPdf/XA Donation Report {donor}.pdf',
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=28)

    archive_pdf.build(elements)
    print(f'XA Donation Report Generated for {donor}!')


new_data = split_data(data)

#make_pdf(new_data[0])
make_pdf((new_data[1]))
