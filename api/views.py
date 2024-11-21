import pdfkit
from django.shortcuts import render
from rest_framework_simplejwt.tokens import AccessToken
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import os
from .models import Report
from .serializers import ReportSerializer,UserSerializer
from django.conf import settings
from rest_framework.exceptions import ValidationError
from .models import UserToken 
from django.utils import timezone
from datetime import datetime
import random
from django.http import FileResponse




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):

        access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        current_time = timezone.now()
        access_token_expiry = current_time + access_token_lifetime
        refresh_token_expiry = current_time + refresh_token_lifetime

        data = super().validate(attrs)
        user = self.user
        data['token']=data['access']
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



@api_view(['GET'])
def generate_pdf(request):
    token = request.GET.get('token', None)
    if not token:
        return HttpResponse("Error: No token provided", status=400)
    
    try:
        decoded_token = AccessToken(token)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=401)
    
    # Retrieve all reports from the database
    report = Report.objects.all()
    
    # Serialize the report data
    serializer = ReportSerializer(report, many=True)
    
    # Render the report content to an HTML string using the template
    html_content = render(request, "create_pdf.html", {"report": serializer.data}).content.decode('utf-8')
    
    pdf_path = save_pdf(html_content)

    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')

def save_pdf(html_content):
    today_date = datetime.now().strftime('%Y_%m_%d')
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    pdf_filename = f'{today_date}/report_{timestamp}.pdf'
    
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf_reports', pdf_filename)
    
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    options = {
        'no-outline': None,  # Disable outlines
        'zoom': 1.0,  # Set zoom level
        'disable-smart-shrinking': True,  # Prevent smart shrinking
        'page-width': '210mm',  # Set page width
        'page-height': '297mm',  # Set page height
    }
    

    pdfkit.from_string(html_content, pdf_path, configuration=config, options=options)
    return pdf_path



def test_view(request):
    return render(request, 'create_pdf.html')