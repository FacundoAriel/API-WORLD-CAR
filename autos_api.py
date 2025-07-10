from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/precios")
def obtener_precios(dias: int = Query(1, ge=1, description="Cantidad de días de alquiler")):
    url = "https://www.worldcar.com.ar/elegi-tu-auto?agencyGuid&commercialAgreementCode&customPromotionId&dateFrom=01-08-2025&dateTo=08-08-2025&driverAge&dropOffEndpoint=World%20Car&dropOffId=1&hourFrom=09%3A00&hourTo=09%3A00&ilimitedKm=false&onlyFullAvailability=false&pickUpEndpoint=World%20Car&pickUpId=1&promotionCode&promotions=10"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "No se pudo acceder al cotizador"}

    soup = BeautifulSoup(response.text, "html.parser")

    autos = []

    cards = soup.select("div.vehicle-card")
    for card in cards:
        nombre = card.select_one("h3")
        precio = card.select_one(".price-value")

        if nombre and precio:
            nombre_texto = nombre.text.strip()
            precio_texto = precio.text.strip().replace("$", "").replace(".", "").replace(",", ".")
            try:
                precio_por_dia = float(precio_texto)
                total = round(precio_por_dia * dias, 2)
            except ValueError:
                precio_por_dia = None
                total = None

            autos.append({
                "nombre": nombre_texto,
                "precio_por_dia": precio_por_dia,
                "dias": dias,
                "total": total
            })

    return {"autos": autos}
