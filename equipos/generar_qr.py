import qrcode 
from django.conf import settings 

def generar_qr(equipo):

    url = f"ttp://127.0.0.1:8000/equipos/api/equipos/{equipo.id}"

    img = qrcode.make(url)

    ruta = f"media/qr_equipos/equipo_{equipo.id}.png"

    img.save(ruta)

    equipo.qr_codigo = ruta 
    equipo.save()