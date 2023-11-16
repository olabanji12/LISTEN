import qrcode
from io import BytesIO
from .models import PlaylistQRCode
from django.core.files import File

def generate_playlist_qrcode(request, url):
    if not PlaylistQRCode.objects.filter(url=url).exists():
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        image_stream = BytesIO()
        img.save(image_stream)
        image_stream.seek(0)

        # Save the image to the database
        qr_code = PlaylistQRCode(url=url)
        qr_code.image.save(f'{url}.png', File(image_stream), save=True)
