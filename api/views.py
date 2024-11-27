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
from .db_functions import fetch_received_energy,fetch_transmissed_energy,fetch_object_by_code
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


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
    data = request.query_params
    token = data.get('token', None)
    sub_code = data.get('sub', None)
    start_date = data.get('dan', None)
    end_date = data.get('gacha', None)

    if not all([token, sub_code, start_date, end_date]):
        return Response({"error": "Missing one or more required parameters: 'token', 'sub', 'dan', 'gacha'"}, status=400)

    user_credentials = UsersForTkn.objects.all()
    user_md5s = [convert_to_md5(user.username, user.key) for user in user_credentials]
    if token not in user_md5s:
        return Response({"error": "Invalid token"}, status=400)

    try:
        received = fetch_received_energy(start_date, end_date, sub_code)
        object_data=fetch_object_by_code(sub_code)
        # print('received:',received)
        received_total_ap_kwh = sum(row["ap_kwh"] for row in received if row["ap_kwh"] is not None)
        transmissed=fetch_transmissed_energy(start_date, end_date, sub_code)
        transmissed_total = sum(row["am_kwh"] for row in transmissed if row["am_kwh"] is not None)
        print('object_data:',object_data)
        report = {}
        html_content = render(request, "create_pdf.html", {
                                            'received':received,
                                            'total_ap_kwh':received_total_ap_kwh,
                                            'transmissed':transmissed,
                                            'transmissed_total':transmissed_total,
                                            'object_data':object_data,
                                            'start_date':start_date,
                                            'end_date':end_date}).content.decode('utf-8')
        pdf_path,pdf_filename = save_pdf(html_content)

        # Open the generated PDF file in binary mode and return it as a downloadable response
        response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
        return response

    except Exception as e:
        return Response({"error": f"An error occurred while generating the PDF: {str(e)}"}, status=500)
            
    

def save_pdf(html_content):
    today_date = datetime.now().strftime('%Y_%m_%d')
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    pdf_filename = f'{today_date}/report_{timestamp}.pdf'

    pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf_reports', pdf_filename)
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    path_to_wkhtmltopdf = r'C:\Users\admin\Desktop\api_return_pdf\wkhtmltopdf.exe'

    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    options = {
        'no-outline': None,
        'zoom': 1.0,
        'disable-smart-shrinking': True,
        'page-width': '210mm',
        'page-height': '297mm',
    }

    pdfkit.from_string(html_content, pdf_path, configuration=config, options=options)
    return pdf_path,pdf_filename


# @login_required  # Ensures the user is logged in
def test_view(request):
    # if not request.user.is_staff:  # Checks if the logged-in user is an admin
    #     return HttpResponseForbidden("You are not authorized to view this page.")
    start_date = '01.10.2024'
    end_date = '01.11.2024'
    sub_code = 'sub_00001'
    received = fetch_received_energy(start_date, end_date, sub_code)
    object_data=fetch_object_by_code(sub_code)
    # print('received:',received)
    received_total_ap_kwh = sum(row["ap_kwh"] for row in received if row["ap_kwh"] is not None)
    transmissed=fetch_transmissed_energy(start_date, end_date, sub_code)
    transmissed_total = sum(row["am_kwh"] for row in transmissed if row["am_kwh"] is not None)
    print('object_data:',object_data)
    return render(request, 'create_pdf.html',{'received':received,
                                              'total_ap_kwh':received_total_ap_kwh,
                                              'transmissed':transmissed,
                                              'transmissed_total':transmissed_total,
                                              'object_data':object_data,
                                              'start_date':start_date,
                                              'end_date':end_date,
                                              })
