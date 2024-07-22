from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, FragLine
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
from reportlab.lib.colors import HexColor

def create_pdf(events, summary, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'fonts/DejaVuSans-Bold.ttf'))

    styles = getSampleStyleSheet() 
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontName='DejaVuSans')
    bold_style = ParagraphStyle('Bold', parent=styles['Normal'], fontName='DejaVuSans-Bold')


    data = [['Data', 'Opis']] + events

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#d0d0d0')),  # Заголовок таблицы
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#000000')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#000000')),
        ('VALIGN', (0, 1), (0, -1), 'MIDDLE'),  # Выравнивание текста по вертикали в колонке даты
    ])
    table_style.add('BACKGROUND', (0, 1), (0, len(data)-1), HexColor('#f0f0f0'))
    table_style.add('BACKGROUND', (1, 1), (1, len(data)-1), HexColor('#ffffff'))

    table = Table(data)
    table.setStyle(table_style)

    elements = []
    elements.append(Paragraph("Raport z wydarzenia", bold_style))  # Заголовок отчета
    elements.append(Spacer(1, 12))  # Внешний отступ сверху
    elements.append(table)
    elements.append(Spacer(1, 12))  # Внешний отступ снизу
    
    # Добавление сводки
    elements.append(Paragraph("Detale:", bold_style))
    elements.append(Spacer(1, 12))
    
    for title, value in summary.items():
        elements.append(Paragraph(title, normal_style))
        elements.append(Spacer(1, 6))
        
        # Разделение текста на абзацы и обработка <span> тегов
        for paragraph in value.split('\n'):   
            elements.append(Paragraph(paragraph, normal_style)) 
            elements.append(Spacer(1, 6)) 

    elements.append(Spacer(1, 12))  # Внешний отступ снизу
    elements.append(Paragraph("Wyniki:\n\nWszystkie dane zostały pomyślnie zebrane i przedstawione w powyższej tabeli", bold_style))  # Итоги

    doc.build(elements, onFirstPage=lambda canvas, _: canvas.setTitle(f"{filename.strip('.pdf')}"))  # Создание PDF




def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_events(driver, reg_number, vin, reg_date):
    driver.get("https://historiapojazdu.gov.pl/strona-glowna")

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "_historiapojazduportlet_WAR_historiapojazduportlet_:rej")))

        reg_num = driver.find_element(By.ID, "_historiapojazduportlet_WAR_historiapojazduportlet_:rej")
        reg_num.send_keys(reg_number)

        vin_field = driver.find_element(By.ID, "_historiapojazduportlet_WAR_historiapojazduportlet_:vin")
        vin_field.send_keys(vin)

        date_reg = driver.find_element(By.ID, "_historiapojazduportlet_WAR_historiapojazduportlet_:data")
        date_reg.click()
        date_reg.send_keys(Keys.HOME)
        date_reg.send_keys(reg_date)

        submit_button = driver.find_element(By.ID, "_historiapojazduportlet_WAR_historiapojazduportlet_:btnSprawdz")
        submit_button.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#timeline .event')))
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser') 
        
        events = []
        summary = {}
        
        # парсинг событий
        for event in soup.select('#timeline .event'):
            date = event.select_one('.date').get_text(strip=True)
            description = "\n".join(p.get_text(strip=True) for p in event.select('.description p') if p.get_text(strip=True))
            events.append((date, description))

        # Парсинг сводки
        summary_box = soup.select_one('#timeline-summary-box')
        for group in summary_box.select('.group-box'):
            title = group.select_one('h3').get_text(strip=True)
            paragraphs = [p.get_text(strip=True) for p in group.select('p') if p.get_text(strip=True)]
            summary[title] = '\n'.join(paragraphs) 
        return events , summary
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
 


async def find_car_data(plate, vin, date):
    
    pdf_filename = f'{plate}.pdf'

    driver = initialize_driver()
    events, summary = fetch_events(driver, plate, vin, date) 
    create_pdf(events, summary, pdf_filename)
    driver.quit()

# if __name__ == "__main__":
#     main()



