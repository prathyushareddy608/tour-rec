from django.shortcuts import render, redirect
from qrcode import *
import razorpay
from .mail import sendMail
from django.views.decorators.csrf import csrf_exempt
from .models import MonumentTickets, MonumentTickets
from django.http import HttpResponse


def safe_int(value):
    """Safely convert value to int, return 0 if conversion fails"""
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0


@csrf_exempt
def book(request):
    global MonumentTickets
    print(request.POST)
    name=request.POST["name"]
    city=request.POST['city']
    monument=request.POST['monument']
    date=request.POST['date']
    phone = request.POST['phone']
    email=request.POST['emailID']

    count_children=safe_int(request.POST['count_children'])
    count_adult=safe_int(request.POST['count_adult'])
    count_abroad=safe_int(request.POST['count_abroad'])
    count_senior=safe_int(request.POST.get('count_senior', 0))
    total_count = count_abroad + count_adult + count_children + count_senior

    price_adult=safe_int(request.POST['price_adult'])
    price_children=safe_int(request.POST['price_children'])
    price_abroad=safe_int(request.POST['price_abroad'])
    price_senior=safe_int(request.POST.get('price_senior', 0))

    total_cost = (price_abroad * count_abroad) + (price_adult * count_adult) + (price_children * count_children) + (price_senior * count_senior)

    # Validate total cost
    if total_cost <= 0:
        return HttpResponse(
            "Invalid order total: amount must be greater than 0",
            status=400,
            content_type="text/plain"
        )

    doc_type=request.POST['doc_type']
    personal_id_no=request.POST['personal_id_no']
    
    # Handle file upload
    aadhar_file = request.FILES.get('aadharCard')

    global payment
    client = razorpay.Client(auth=('rzp_test_A0pbku9Y5vKP6Z', 'V70rauYt6WIeDQi7vfMmhQD5')) # create Razorpay client

    response_payment = client.order.create(dict(amount=total_cost*100, currency='INR'))# create order
    order_id = response_payment['id']
    order_status = response_payment['status']
    if order_status == 'created':
        Ticket=MonumentTickets(name=name, city=city, monument =monument, date=date, email=email, phone=phone, count_abroad=count_abroad,
        count_adult=count_adult,
        count_children=count_children,
        count_senior=count_senior,

        price_abroad=price_abroad,
        price_adult=price_adult,
        price_children=price_children,
        price_senior=price_senior,
         
        total_count=total_count,
        total_cost=total_cost,
        order_id=order_id,
        doc_type=doc_type,
        personal_id_no=personal_id_no,
        aadhar_card_file=aadhar_file)
        
        Ticket.save()
        response_payment['name'] = name
        response_payment['number'] = phone
        print(response_payment)
        # return Response(response_payment)
        return render(request,'coffee_payment.html',{ 'payment': response_payment})    

    return redirect("homepage")

def payment_status(request):
    responses = request.POST['razorpay_order_id']
    response=request.POST
    print(responses)
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=('rzp_test_A0pbku9Y5vKP6Z', 'V70rauYt6WIeDQi7vfMmhQD5'))
    status = client.utility.verify_payment_signature(params_dict)
    cold_coffee = MonumentTickets.objects.get(order_id=response['razorpay_order_id'])
    cold_coffee.razorpay_payment_id = response['razorpay_payment_id']
    cold_coffee.paid = True
    cold_coffee.save()
    # Generate QR code
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_data = f"Booking ID: {response['razorpay_order_id']}\nName: {cold_coffee.name}\nMonument: {cold_coffee.monument}\nDate: {cold_coffee.date}\nVisitors: {cold_coffee.total_count}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = "Frontend/build/static/Generated_QR/test.png"
        
        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        img.save(img_path)
    except Exception as e:
        print(f"QR Code generation failed: {e}")
        # Use a placeholder QR code image
        img_path = "https://via.placeholder.com/200x200/000000/FFFFFF?text=QR+CODE"
    context_dict={
                    'name': cold_coffee.name,
                    'date':cold_coffee.date,
                    'city':cold_coffee.city,
                    'monument': cold_coffee.monument,
                    'count_adult':cold_coffee.count_adult,
                    'count_children':cold_coffee.count_children,
                    'count_abroad':cold_coffee.count_abroad,
                    'total_count':cold_coffee.total_count,
                    'total_cost':cold_coffee.total_cost,
                    'img':img_path,
                    'status': True,
                    'safar_logo_1':"Frontend/build/static/Images/banner.png",
                    'safar_logo_2':"Frontend/build/static/Images/banner1.png",
                    'safar_logo_3':"Frontend/build/static/Images/solid-color-image-2.png",
                    'id':response['razorpay_order_id'],
                    'doc_type':cold_coffee.doc_type,
                    'personal_id_no':cold_coffee.personal_id_no,
                }
    
    # Generate PDF ticket
    try:
        filename = "Frontend/build/static/Generated_ticket/"+response['razorpay_order_id']+".pdf"
        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        write_pdf('monumentTicket.html', context_dict, filename, cold_coffee)
        context_dict['pdf_generated'] = True
        context_dict['pdf_path'] = filename
    except Exception as e:
        print(f"PDF generation failed: {e}")
        context_dict['pdf_generated'] = False
        context_dict['pdf_error'] = str(e)
    
    # Send email (with error handling)
    try:
        sendMail(cold_coffee.email, response['razorpay_order_id'],cold_coffee,context_dict)
        context_dict['email_sent'] = True
    except Exception as e:
        print(f"Email sending failed: {e}")
        context_dict['email_sent'] = False
    
    return render(request, 'payment_status.html', context_dict)
    # except:
    #     return render(request, 'payment_status.html', {'status': False})

from django.template.loader import get_template
from django.template import Context
from io import BytesIO

def write_pdf(template_src, context_dict, filename, cold_coffee):
    # PDF generation is disabled in this deployment because xhtml2pdf and its
    # dependencies do not install reliably in Render's readonly build environment.
    # If you need PDF ticket generation, enable a supported PDF library here.
    raise RuntimeError('PDF generation is disabled in this deployment.')