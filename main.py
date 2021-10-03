from bs4 import BeautifulSoup
import requests
import csv


page = requests.get('https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors')
soup = BeautifulSoup(page.text, 'html.parser')
all_data_table = soup.find_all(class_='data-table__row')


new_row = []
for row in all_data_table:
    new_column = []
    for column in row:
        data = column.find(class_='data-table__value').get_text()
        if '$' in data:
            remove_dollar = data.replace("$", "")
            formatted_data = remove_dollar.replace(",", ".")
            data = float(formatted_data)
        elif '%' in data:
            remove_percent = data.replace("%", "")
            data = float(remove_percent)
        new_column.append(data)
    new_row.append(new_column)

header = ['Major', 'Early Career Pay', 'Mid-Career Pay', '% High Meaning']
with open('payscale_data.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(new_row)
