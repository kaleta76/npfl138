import qrcode

# URL, ktorú chcete zakódovať do QR kódu
url = "https://www.slovensko.sk/sk/detail-sluzby?externalCode=sluzba_egov_1046"

# Vytvorenie inštancie QRCode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

# Pridanie dát do QRCode
qr.add_data(url)
qr.make(fit=True)

# Vytvorenie obrázka QRCode
img = qr.make_image(fill='black', back_color='white')

# Uloženie obrázka QRCode
img.save("C:\\Users\\kalet\\Documents\\npfl138\\labs\\01\\qr_code.png")
