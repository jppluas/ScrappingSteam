import requests
from bs4 import BeautifulSoup
import csv

linkPopulares='https://steamcharts.com/top'
preciosPopulares=[]
caracteristicasPopulares=[]
esMultijugador=[]
categoriasPopulares=[]


def scrapGlobal_text(url, hasMany, label, hasClass, labelClass):
  htmlElement=''
  htmlElements=[]
  elements=[]
  response = requests.get(url)
  if response.status_code == 200:
    html = BeautifulSoup(response.text, 'html.parser')
    if hasMany:
      if hasClass:
        htmlElements = html.find_all(label, class_=labelClass)
      else:
        htmlElements = html.find_all(label)
      for htmlElement in htmlElements:
        elements.append(htmlElement.text.strip())
        #print(htmlElement.text.strip())
    else:
      if hasClass:
        htmlElement = html.find(label, class_=labelClass)
        #print (htmlElement.text.strip())
        return htmlElement.text.strip()
      else:
        htmlElement = html.find(label)
        #print (htmlElement.text.strip())
        return htmlElement.text.strip()

  else:
    print('Error al acceder a la página:', response.status_code)
  return elements


def scrapSpecific_text(url, hasMany, container, containerClass, label, hasClass, labelClass):
  htmlElements=[]
  elements=[]
  response = requests.get(url)
  if response.status_code == 200:
    html = BeautifulSoup(response.text, 'html.parser')
    htmlContainer = html.find(container, class_=containerClass)
    if htmlContainer:
      if hasMany:
        if hasClass:
          htmlElements = htmlContainer.find_all(label, class_=labelClass)
        else:
          htmlElements = htmlContainer.find_all(label)
        for htmlElement in htmlElements:
          elements.append(htmlElement.text.strip())
          #print(htmlElement.text.strip())
      else:
        if hasClass:
          htmlElement = htmlContainer.find(label, class_= labelClass)
          #print (htmlElement.text.strip())
          return htmlElement.text.strip()
        else:
          htmlElement = htmlContainer.find(label)
          #print (htmlElement.text.strip())
          return htmlElement.text.strip()

    else:
      print(
          f"No se encontró el contenedor con la clase {containerClass} en la página.")
  else:
    print('Error al acceder a la página:', response.status_code)
  return elements


def scrapIds(url, hasMany, container, containerClass, label, hasClass, labelClass):
  htmlElements=[]
  links = []
  response = requests.get(url)
  if response.status_code == 200:
      html = BeautifulSoup(response.text, 'html.parser')
      htmlContainer = html.find(container, class_=containerClass)
      if htmlContainer:
          if hasMany:
            if hasClass:
                htmlElements = htmlContainer.find_all(label, class_=labelClass)
            else:
                htmlElements = htmlContainer.find_all(label)
            for htmlElement in htmlElements:
                link = htmlElement.get('href')
                if link:
                    links.append(link.split('/')[-1])

                    #print(link)
                else:
                    print('La etiqueta no tiene atributo href.')  
          else:
            if hasClass:
              htmlElement = htmlContainer.find(label, class_=labelClass)
              return htmlElement.get('href').split('/')[-1]
            else:
              htmlElement = htmlContainer.find(label)
              return htmlElement.get('href').split('/')[-1]

      else:
          print(f"No se encontró el contenedor con la clase {containerClass} en la página.")
  else:
      print('Error al acceder a la página:', response.status_code)
  return links


nombresJuegos=scrapSpecific_text(linkPopulares,True, 'table','common-table','a', False, 'x')
jugadoresPico=scrapGlobal_text(linkPopulares,True,'td',True, 'peak-concurrent')
ids=scrapIds(linkPopulares, True, 'table','common-table','a', False, 'x')


for juego in nombresJuegos:
  nombre_format= juego.lower().replace(":", "").replace(" ", "+")
  url='https://gg.deals/games/?title='+nombre_format
  precio=scrapSpecific_text(url, False, 'span','lowest-recorded','span',True,'price-inner')
  if precio == 'Free':
    precio = 0
  else:
    precio = float(precio.replace('$', '').replace('~', ''))
  preciosPopulares.append(precio)

for id in ids:
  carac=''
  url='https://store.steampowered.com/app/'+id
  caracteristicas=scrapGlobal_text(url, True,'div', True, 'label')
  categorias=scrapGlobal_text(url, True,'a', True, 'app_tag')

  categoriasPopulares.append(categorias)
  for caracteristica in caracteristicas:  
    #print(caracteristica)
    carac=carac+' '+caracteristica
  #print(carac)
  if ('Online' in carac) or ('Multiplayer' in carac) or ('Anti-Cheat' in carac):
    esMultijugador.append('Multijugador')
  else:
    esMultijugador.append('No multijugador')

juegosPopulares={}

for i in range(len(nombresJuegos)):
  if nombresJuegos[i] not in juegosPopulares:
    juegosPopulares[nombresJuegos[i]] = []
  juegosPopulares[nombresJuegos[i]].append(ids[i])
  juegosPopulares[nombresJuegos[i]].append(jugadoresPico[i])
  juegosPopulares[nombresJuegos[i]].append(preciosPopulares[i])
  juegosPopulares[nombresJuegos[i]].append(esMultijugador[i])
  juegosPopulares[nombresJuegos[i]].append(categoriasPopulares[i])


print(juegosPopulares)


ruta_archivo_csv = 'datosPluas.csv'
with open(ruta_archivo_csv, 'w', newline='', encoding='utf-8') as archivo_csv:
  escritor_csv = csv.writer(archivo_csv, delimiter=';')

  escritor_csv.writerow(['Nombre', 'ID', 'Jugadores pico diarios', 'Precio en $', 'Jugabilidad', 'Categorías'])

  for datos in zip(nombresJuegos, ids, jugadoresPico, preciosPopulares, esMultijugador, categoriasPopulares):
    datos = list(datos[:4]) + [','.join(map(str, sublist)) if isinstance(sublist, list) else sublist for sublist in datos[4:5]] + [','.join(map(str, datos[5]))]
    escritor_csv.writerow(datos)