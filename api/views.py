import hashlib
import os
import pdfkit
from datetime import datetime
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserToken,UsersForTkn
from rest_framework.response import Response


def convert_to_md5(username, key):
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    print(current_time)
    input_string = f"{username}{key}{current_time}"
    input_bytes = input_string.encode('utf-8')
    md5_hash = hashlib.md5(input_bytes).hexdigest()
    print(md5_hash)
    return md5_hash


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        current_time = timezone.now()
        access_token_expiry = current_time + access_token_lifetime
        refresh_token_expiry = current_time + refresh_token_lifetime

        data = super().validate(attrs)
        user = self.user
        data['token'] = data['access']
        data['user'] = user.username

        UserToken.objects.create(
            username=user.username,
            access_token=data['access'],
            refresh_token=data['refresh'],
            access_token_expiry=access_token_expiry,
            refresh_token_expiry=refresh_token_expiry,
        )
        data['expire_date'] = access_token_expiry.strftime('%Y-%m-%d %H:%M')
        del data['refresh']
        del data['access']

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# http://192.168.14.167:8000/api/generate-pdf/?token=<your_token>&sub=<your_sub_value>&dan=<your_dan_value>&gacha=<your_gacha_value>
# http://192.168.14.167:8000/api/generate-pdf/?token=your_token&sub=your_sub_value&dan=your_dan_value&gacha=your_gacha_value

@api_view(['GET'])
def generate_pdf(request):
    data=request.query_params
    token = data.get('token', None)
    sub = data.get('sub', None)
    dan = data.get('dan', None)
    gacha = data.get('gacha', None)
    if not all([token, sub, dan, gacha]):
        return Response({"error": "Missing one or more required parameters: 'token', 'sub', 'dan', 'gacha'"}, status=400)
    user_credentials = UsersForTkn.objects.all()
    user_md5s = [convert_to_md5(user.username, user.key) for user in user_credentials]
    if token not in user_md5s:
        return Response({"error": "Invalid token"}, status=400)
    try:
        report = {}
        html_content = render(request, "create_pdf.html", {"report": report}).content.decode('utf-8')
        pdf_path = save_pdf(html_content)
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    except Exception as e:
        return Response({"error": f"An error occurred while generating the PDF: {str(e)}"}, status=500)
            
    

def save_pdf(html_content):
    today_date = datetime.now().strftime('%Y_%m_%d')
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    pdf_filename = f'{today_date}/report_{timestamp}.pdf'

    pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf_reports', pdf_filename)
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    options = {
        'no-outline': None,
        'zoom': 1.0,
        'disable-smart-shrinking': True,
        'page-width': '210mm',
        'page-height': '297mm',
    }

    pdfkit.from_string(html_content, pdf_path, configuration=config, options=options)
    return pdf_path


def test_view(request):
    return render(request, 'create_pdf.html')
