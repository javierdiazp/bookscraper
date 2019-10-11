INSTRUCCIONES DE USO

0. REQUERIMIENTOS
Python 3.7+

1. SCRAPING
El proceso de scraping se realiza bajo la interfaz manage.py de Django.
Para invocarla se debe ejecutar el comando 'python manage.py scrapebooks.py'

El scraping de cada categoria (junto a sus respectivos libros) se realiza de
manera concurrente por medio de ThreadPoolExecutor (Python 3.7+)

2. API ENDPOINTS
  Se provee de un archivo de colección para ejecutar algunas pruebas en Postman

  2a. api-token-auth/
    Autenticacion por token.
    Para obtener un token se debe ejecutar un POST con campos username y password válidos
    Para efectos de testing se suministra el usuario siguiente: username=admin password=k14v3123

  2b. book/
    Retorna una lista paginada con los libros scrapeados

  2c. book/{id}
    Retorna el detalle de un libro por su identificados {id}

  2d. categories/
    Retorna una lista paginada con las categorias scrapeadas