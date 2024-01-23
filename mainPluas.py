#TIEMPO DE EJECUCION DE SCRAPPING 1:30 MIN
import requests
from bs4 import BeautifulSoup
import csv

linkPopulares = 'https://steamcharts.com/top'
preciosPopulares = []
caracteristicasPopulares = []
esMultijugador = []
categoriasPopulares = []

def scrapGlobal_text(url, hasMany, label, hasClass, labelClass):
  htmlElement = ''
  htmlElements = []
  elements = []
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


def scrapSpecific_text(url, hasMany, container, containerClass, label,
                       hasClass, labelClass):
  htmlElements = []
  elements = []
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
          htmlElement = htmlContainer.find(label, class_=labelClass)
          #print (htmlElement.text.strip())
          return htmlElement.text.strip()
        else:
          htmlElement = htmlContainer.find(label)
          #print (htmlElement.text.strip())
          return htmlElement.text.strip()

    else:
      print(
          f"No se encontró el contenedor con la clase {containerClass} en la página."
      )
  else:
    print('Error al acceder a la página:', response.status_code)
  return elements


def srapSpecific_links(url, hasMany, container, containerClass, label,
                       hasClass, labelClass):
  htmlElements = []
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
            links.append(link)
            #print(link)
          else:
            print('La etiqueta no tiene atributo href.')
      else:
        if hasClass:
          htmlElement = htmlContainer.find(label, class_=labelClass)
          return htmlElement.get('href')
        else:
          htmlElement = htmlContainer.find(label)
          return htmlElement.get('href')

    else:
      print(
          f"No se encontró el contenedor con la clase {containerClass} en la página."
      )
  else:
    print('Error al acceder a la página:', response.status_code)
  return links


nombresJuegos = scrapSpecific_text(linkPopulares, True, 'table',
                                   'common-table', 'a', False, 'x')
jugadoresPico = scrapGlobal_text(linkPopulares, True, 'td', True,
                                 'peak-concurrent')
ids = srapSpecific_links(linkPopulares, True, 'table', 'common-table', 'a',
                         False, 'x')

for juego in nombresJuegos:
  nombre_format = juego.lower().replace(":", "").replace(" ", "+")
  url = 'https://gg.deals/games/?title=' + nombre_format
  precio = scrapSpecific_text(url, False, 'span', 'lowest-recorded', 'span',
                              True, 'price-inner')
  if precio == 'Free':
    precio = 0
  else:
    precio = float(precio.replace('$', '').replace('~', ''))
  preciosPopulares.append(precio)

for id in ids:
  carac = ''
  url = 'https://store.steampowered.com/app/' + id.split('/')[-1]
  caracteristicas = scrapGlobal_text(url, True, 'div', True, 'label')
  categoria= scrapSpecific_text(url, False, 'div', "details_block", 'a', False, 'app_tag')

  categoriasPopulares.append(categoria)
  for caracteristica in caracteristicas:
    #print(caracteristica)
    carac = carac + ' ' + caracteristica
  #print(carac)
  if ('Online' in carac) or ('Multiplayer' in carac) or ('Anti-Cheat'
                                                         in carac):
    esMultijugador.append('Multijugador')
  else:
    esMultijugador.append('No multijugador')

juegosPopulares = {}

for i in range(len(nombresJuegos)):
  if nombresJuegos[i] not in juegosPopulares:
    juegosPopulares[nombresJuegos[i]] = []
  juegosPopulares[nombresJuegos[i]].append(ids[i].split('/')[-1])
  juegosPopulares[nombresJuegos[i]].append(jugadoresPico[i])
  juegosPopulares[nombresJuegos[i]].append(preciosPopulares[i])
  juegosPopulares[nombresJuegos[i]].append(esMultijugador[i])
  juegosPopulares[nombresJuegos[i]].append(categoriasPopulares[i])

print(juegosPopulares)

num_juegos_por_categoria = {}
num_juegos_multijugador = 0
num_juegos_no_multijugador = 0
num_juegos_gratis = 0
num_juegos_no_gratis = 0

for juego, detalles in juegosPopulares.items():
    categoria = detalles[4]  

    if categoria in num_juegos_por_categoria:
        num_juegos_por_categoria[categoria] += 1
    else:
        num_juegos_por_categoria[categoria] = 1

    if detalles[3] == 'Multijugador':
        num_juegos_multijugador += 1
    else:
        num_juegos_no_multijugador += 1

    if detalles[2] == 0.0:
        num_juegos_gratis += 1
    else:
        num_juegos_no_gratis += 1

with open('categorias.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Categoría', 'Número de Juegos'])
    for categoria, cantidad in num_juegos_por_categoria.items():
        writer.writerow([categoria, cantidad])

with open('multijugador.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Tipo', 'Número de Juegos'])
    writer.writerow(['Multijugador', num_juegos_multijugador])
    writer.writerow(['No Multijugador', num_juegos_no_multijugador])

with open('precio.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Tipo', 'Número de Juegos'])
    writer.writerow(['Gratis', num_juegos_gratis])
    writer.writerow(['No Gratis', num_juegos_no_gratis])

with open('juegosPopulares.txt', 'w', newline='') as txtfile:
  txtfile.write("juegosPopulares = {\n")
  for juego, detalles in juegosPopulares.items():
      txtfile.write(f"    '{juego}': {detalles},\n")
  txtfile.write("}\n")
