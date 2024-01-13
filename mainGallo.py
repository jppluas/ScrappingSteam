import requests
from bs4 import BeautifulSoup
import csv

url = "https://store.steampowered.com/search/?maxprice=60&supportedlang=spanish&ndl=1"
head = {'cookie': 'sessionid=190254028ba4d6a7206526f1'}
#obtener generos de diferentes juegos
accion = "https://store.steampowered.com/search/?maxprice=60&supportedlang=spanish&tags=19%2C492&ndl=1"  
familia = "https://store.steampowered.com/search/?maxprice=60&supportedlang=spanish&tags=492%2C5350&ndl=1"  
puzzle = "https://store.steampowered.com/search/?maxprice=60&supportedlang=spanish&tags=492%2C1664&ndl=1"  
estrategia = "https://store.steampowered.com/search/?maxprice=60&supportedlang=spanish&tags=492%2C9&ndl=1"  
generos = [url, accion, familia, puzzle, estrategia]
with open('datosGallo.csv', 'w'):
  pass
with open('datosGeneros.csv', 'w'):
  pass
for i in generos:
  request = requests.get(i, headers=head)
  soup = BeautifulSoup(request.text, 'html.parser')
  titulos = soup.find_all('div', class_='col search_name ellipsis')
  precios = soup.find_all('div', class_='discount_final_price')
  reseñas = soup.find_all("div",
                          class_='col search_reviewscore responsive_secondrow')
  fechas = soup.find_all("div",
                         class_="col search_released responsive_secondrow")
  archivo = 'datosGallo.csv'
  if(i!=url):
    archivo='datosGeneros.csv'
  
  with open(archivo, 'a', newline='', encoding='utf-8') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv, delimiter=';')

    escritor_csv.writerow(['Nombre', 'Precio', 'Fechas', 'Reseñas'])
    if(i==url):
      for title, precio, reseña, fecha in zip(titulos, precios, reseñas, fechas):
        escritor_csv.writerow([
            title.text.strip(), precio.text,
            fecha.text.strip(),
            str(reseña).split(" ")[str(reseña).split(" ").index("user") - 1]
        ])
    for title, precio, reseña, fecha in zip(titulos[:10], precios[:10], reseñas[:10], fechas[:10]):
      vnames = [name for name in globals() if globals()[name] is i]
      escritor_csv.writerow([vnames[0],
          title.text.strip(), precio.text,
          fecha.text.strip(),
          str(reseña).split(" ")[str(reseña).split(" ").index("user") - 1]
      ])
