from requests import get
from time import sleep


def datos(html):
    x = get(html)
    if x.status_code == 200:
        return x.json()
    else:
        return print("No se ha podido establecer conexión.")


def recorte(direccion, cuenta):  # Recorta la cuenta según marque la direccion del diccionario de llamada.
    return cuenta // float(direccion) * float(direccion)


def llamada():  # Comprueba los pares y genera un diccionario con la informacion necesaria.
    hitbtc = datos("https://api.hitbtc.com/api/2/public/orderbook")
    size = datos("https://api.hitbtc.com/api/2/public/symbol")
    lista_pares = []
    for par in hitbtc:
        lista_pares.append(par)
    # Este script ve que pares tienen en común USDT y BTC y los agrega a una lista.
    lista_final = []  # Lista en la que se agregan.
    for par in lista_pares:
        if 'USD' in par:  # Si el par contiene la palabra USD comprueba si exite el mismo par remplazando USD y BTC
            p = str(par).replace("USD", "BTC")
            if p in lista_pares:
                lista_final.append(par)
    # El siguiente script genera un diccionario con el nombre del par y una lista del Quantun y Tick respectivamente.
    dicc = {}
    for info in size:
        for n in lista_final:
            if n == info['id']:
                dicc.setdefault(n, [info['quantityIncrement'], info['tickSize']])
            elif str(n).replace("USD", "BTC") == info['id']:
                dicc.setdefault(info['id'], [info['quantityIncrement'], info['tickSize']])
    return dicc


y = llamada()
print("Conectado.")
while True:
    h = datos("https://api.hitbtc.com/api/2/public/orderbook")
    prueba = 1
    maximo = 0
    clave = ''
    for cambio in y:
        if "USD" in cambio:
            final = prueba / float(h[cambio]['ask'][0]['price'])
            final = recorte(float(y[cambio][0]), final)
            final = final * float(h[str(cambio).replace("USD", "BTC")]["bid"][0]["price"])
            final = recorte(float(y[str(cambio).replace("USD", "BTC")][1]), final)
            if final < 0.0002:
                if final > maximo:
                    maximo = final
                    clave = cambio
				elif "BTC" in cambio:
						final = 0.000106 / float(h[cambio]['ask'][0]['price'])
					  final = recorte(float[y[cambio][0], final)
					  final = final * float(y[str(cambio).remplace("BTC", "USD")]["bid"][0]["price"])
					  final = recorte(float(y[str(cambio).remplace("BTC", "USD")][1]), final)
					  print(final)
    print(round(maximo, 8), clave)
    print(round(prueba /float(h["BTCUSD"]["ask"][0]["price"]), 8), "Original")
    print("----------------------")
    sleep(30)
