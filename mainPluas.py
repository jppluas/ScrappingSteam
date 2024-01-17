import requests
from bs4 import BeautifulSoup
import csv

linkPopulares = 'https://steamcharts.com/top'
preciosPopulares = []
caracteristicasPopulares = []
esMultijugador = []
categoriasPopulares = []


def agecheckpass():
  url = 'https://store.steampowered.com/agecheck/app/271590/'
  response = requests.get(url)
  html = BeautifulSoup(response.text, 'html.parser')

  form_data = {}
  for select in html.find_all('select'):
    select_name = select.get('name')
    if select_name:
      form_data[select_name] = select.find('option')['value']
  form_data['ageDay'] = '1'
  form_data['ageMonth'] = 'January'
  form_data['ageYear'] = '1980'

  response = requests.post(url, data=form_data)
  if response.status_code == 200:
    print('Formulario enviado con éxito!')
    return True
  else:
    print('Error al enviar el formulario:', response.status_code)
    print('Contenido de la respuesta:', response.text)
    return False


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

ruta_archivo_csv = 'datosPluas.csv'
with open(ruta_archivo_csv, 'w', newline='', encoding='utf-8') as archivo_csv:
  escritor_csv = csv.writer(archivo_csv, delimiter=';')

  escritor_csv.writerow([
      'Nombre de juego', 'ID', 'Jugadores pico diarios', 'Precio en $',
      'Jugabilidad', 'Categorías'
  ])

  # Escribe los datos de las listas paralelas
  for datos in zip(nombresJuegos, ids, jugadoresPico, preciosPopulares,
    esMultijugador, categoriasPopulares):
      escritor_csv.writerow(datos)
