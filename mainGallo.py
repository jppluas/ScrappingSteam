import requests
from bs4 import BeautifulSoup

url= "https://store.steampowered.com/search/?maxprice=60&supportedlang=spanish&ndl=1"
head = {'cookie': 'sessionid=190254028ba4d6a7206526f1'}
r = requests.get(url,headers=head)

soup = BeautifulSoup(r.text, 'html.parser')

titulos = soup.find_all('div',class_='col search_name ellipsis')
precios= soup.find_all('div',class_='discount_final_price')
reseñas= soup.find_all("div",class_='col search_reviewscore responsive_secondrow')
fechas=soup.find_all("div",class_="col search_released responsive_secondrow")
archivo = 'datosGallo.csv'
with open(archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
  escritor_csv = csv.writer(archivo, delimiter=';')

  escritor_csv.writerow(['Nombre', 'Precio','Fechas','Reseñas'])
  for title,precio,reseña,fecha in zip(titulos,precios,reseñas,fechas):
     escritor_csv.writerow([title.text.strip(), precio.text, fecha.text.strip(),str(reseña).split(" ")[str(reseña).split(" ").index("user")-1]])