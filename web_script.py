import schedule
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_data():
    url = 'https://www.mercadolibre.com.co/ofertas#nav-header'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        productos = soup.find_all('div', class_='promotions_boxed-width')

        nombres = []
        precios = []
        img_urls = []

        for producto in productos:
            nombre = producto.find('p', class_='promotion-item__title').get_text()
            precio = producto.find('span', class_='andes-money-amount__fraction').get_text()
            img_url = producto.find('img', class_='promotion-item__img')['src']

            nombres.append(nombre)
            precios.append(precio)
            img_urls.append(img_url)

        datos = {
            'Nombre': nombres,
            'Precio': precios,
            'Imagen': img_urls
        }

        df = pd.DataFrame(datos)

        df.to_csv('datos.csv', index=False)

        print("Datos guardados exitosamente.")

    except requests.Timeout:
        print("Tiempo de espera agotado. No se pudo obtener la respuesta del servidor.")
    except requests.RequestException as e:
        print("Error al realizar la solicitud:", str(e))

# Programar la ejecución de la función scrape_data()
schedule.every().hour.do(scrape_data)

# Bucle para mantener el script en ejecución
while True:
    schedule.run_pending()
    time.sleep(1)
