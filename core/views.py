from django.shortcuts import render, redirect ,get_object_or_404
from .forms import Registerform, Authenticateform , userchange ,AdminProfileForm , changepasswordform , Userform
from django.contrib.auth import authenticate, login, logout , update_session_auth_hash
from django.contrib import messages
from . models import new_arrival,CartUpperwear,Userdetails,Order


#============================= Paypal ===============================

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse


#================ Forgot Password ======================
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import HttpResponse


def index(request):
    return render(request, 'core/index.html')

####################  REGISTER AND LOGIN #########################

def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            rf = Registerform(request.POST)
            if rf.is_valid():
                rf.save()
                messages.success(request, 'Registration Successful')
                email = request.POST['email']
                user = User.objects.filter(email=email).first()
                if user:
                   send_mail(
                    'Registration Successful',
                    'Dear User,\n\nThank you for registering with us! We are excited to have you on board and look forward to providing you with the best experience. If you have any questions or need assistance, feel free to reach out to us.\n\nBest regards,\n[Red Flame & Team]',
                    'redflamepremium@gmail.com',  # Use a verified email address
                    [email],
                    fail_silently=False,
)
                return redirect('login')
        else:
            rf = Registerform()
        return render(request, 'core/register.html', {'rf': rf})
    else:
        return redirect('profile')

def log_in(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            rf = Authenticateform(request, request.POST)
            if rf.is_valid():
                name = rf.cleaned_data['username']
                pas = rf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)  
                    return redirect('/')
                else:
                    messages.error(request, 'Invalid username or password')
        else:
            rf = Authenticateform()
        return render(request, 'core/login.html', {'rf': rf})
    else:
        return redirect('profile')

def log_out(request):
    logout(request)
    return redirect('register')



def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.is_superuser:
                rf = AdminProfileForm(request.POST, instance=request.user)
            else:
                rf = userchange(request.POST, instance=request.user)

            if rf.is_valid():
                rf.save()
                messages.success(request, 'Profile Updated Successfully !!')
        else:
            if request.user.is_superuser:
                rf = AdminProfileForm(instance=request.user)
            else:
                rf = userchange(instance=request.user)
                
        return render(request, 'core/profile.html', {'name': request.user, 'rf': rf})
    else:
        return redirect('login')


def changepassword(request):                                                     
    if request.user.is_authenticated:                              
        if request.method == 'POST':                               
            rf =changepasswordform(request.user,request.POST)
            if rf.is_valid():
                rf.save()
                update_session_auth_hash(request,rf.user)
                return redirect('profile')
        else:
            rf = changepasswordform(request.user)
        return render(request,'core/changepassword.html',{'rf':rf})
    else:
        return redirect('login')

    

        

####################  FETCHING IMAGE THROUGH DATABASE AND REDIRECT TO DETAILS PAGE #########################

def trending(request):
    rf=new_arrival.objects.filter(category='TRENDING')
    return render(request,'core/trending.html',{'rf':rf})

def newarrival(request):
    rf=new_arrival.objects.filter(category='NEWARRIVAL')
    return render (request,'core/newarrival.html',{'rf':rf})

def shirt(request):
    rf=new_arrival.objects.filter(category='SHIRTS')
    return render (request,'core/shirt.html',{'rf':rf})


def Tshirt(request):
    rf=new_arrival.objects.filter(category='T_SHIRTS')
    return render (request,'core/Tshirt.html',{'rf':rf})
    

def bigcard(request,id):
    rf=new_arrival.objects.get(pk=id)

    return render(request,'core/bigcard.html',{'rf':rf})






####################  ADD TO CART #########################




from django.contrib import messages
from django.shortcuts import redirect
from .models import CartUpperwear, new_arrival

def add_to_cart(request, id):
    if request.user.is_authenticated: 
        na = new_arrival.objects.get(pk=id)
        user = request.user
        if CartUpperwear.objects.filter(user=user, product=na).exists():
            messages.error(request, 'This item is already in your cart!')
        else:
            CartUpperwear(user=user, product=na).save()
            messages.success(request, 'Item added to cart successfully!')       
        return redirect('bigcard', id)  
    else:
        return redirect('login')  



def showcart(request):
    if request.user.is_authenticated:
        ca=CartUpperwear.objects.filter(user=request.user)
        return render (request,'core/showcart.html',{'ca':ca})
    else:
        return redirect('login')

def delete_cart(request, id):
    if request.user.is_authenticated:
        ca = CartUpperwear.objects.get(pk=id) 
        ca.delete()
        return redirect('showcart') 
    else:
        return redirect('login')


def add_item(request,id):
    if request.user.is_authenticated:
        product =get_object_or_404(CartUpperwear,pk=id)
        if product.quantity >=4:
            messages.error(request, "You cannot add more than 4 of this item.")
            return redirect('showcart')
        product.quantity +=1
        product.save()
        return redirect('showcart')
    else:
        return redirect('login')

def delete_item(request,id):
    if request.user.is_authenticated:
        product=get_object_or_404(CartUpperwear,pk=id)
        if product.quantity>1:
            product.quantity -=1
            product.save()
        return redirect('showcart')
    else:
        return redirect ('login')

########################## ADDRESS PAGE #########################

def address(request):
    if request.method == 'POST':
        rf=Userform(request.POST)
        if rf.is_valid():
            user=request.user
            name= rf.cleaned_data['name']
            address= rf.cleaned_data['address']
            city= rf.cleaned_data['city']
            state= rf.cleaned_data['state']
            pincode= rf.cleaned_data['pincode']
            Userdetails(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
            return redirect('showaddress')
    else:
        rf =Userform()
        address = Userdetails.objects.filter(user=request.user)
    return render(request,'core/address.html',{'rf':rf,'address':address})


def delete_address(request,id):
    if request.method == 'POST':
        rf = Userdetails.objects.get(pk=id)
        rf.delete()
    return redirect('showaddress')

def showaddress(request):
    address = Userdetails.objects.filter(user=request.user)
    return render(request,'core/showaddress.html',{'address':address})

###################################  CHECKOUT PAGE ####################################

def checkout(request):
    if request.user.is_authenticated:
        ca=CartUpperwear.objects.filter(user=request.user)
        total=0
        Delivery_charge = 149 
        for c in ca :
            total+=(c.product.discounted_price*c.quantity)
            final_price = total+Delivery_charge
        address=Userdetails.objects.filter(user=request.user)
        return render(request, 'core/checkout.html', {'ca': ca,'total':total,'final_price':final_price,'address':address})
    else:
        return redirect ('login')
    


def payment(request):
    if request.method == 'POST':
        selected_address_id= request.POST.get('selected_address')
    ca=CartUpperwear.objects.filter(user=request.user)
    total=0
    Delivery_charge = 149 
    for c in ca :
        total+=(c.product.discounted_price*c.quantity)
        final_price = total+Delivery_charge
    address=Userdetails.objects.filter(user=request.user)
    #============== Paypal Code =====================
   
    host = request.get_host()   # Will fecth the domain site is currently hosted on.
   
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,   #This is typically the email address associated with the PayPal account that will receive the payment.
        'amount': final_price,    #: The amount of money to be charged for the transaction. 
        'item_name': 'Pet',       # Describes the item being purchased.
        'invoice': uuid.uuid4(),  #A unique identifier for the invoice. It uses uuid.uuid4() to generate a random UUID.
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",         #The URL where PayPal will send Instant Payment Notifications (IPN) to notify the merchant about payment-related events
        'return_url': f"http://{host}{reverse('paymentsuccess',args=[selected_address_id])}",     #The URL where the customer will be redirected after a successful payment. 
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",      #The URL where the customer will be redirected if they choose to cancel the payment. 
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

        #=============== Paypal Code  End =====================

    return render(request,'core/payment.html',{'paypal':paypal_payment})


def payment_success(request, selected_address_id):
    user = request.user
    address_data = Userdetails.objects.get(pk=selected_address_id)
    cart = CartUpperwear.objects.filter(user=request.user)
    
    for cart in cart:
        Order(
            user=user,
            customer=address_data,
            quantity=cart.quantity,
            cloth=cart.product).save()
        cart.delete() 
    send_mail(
                'Thank You for Your Order',
                f'Hello ,\n\nThank you for placing your order with us! We appreciate your business and are processing your order. You will receive an update soon with the details of your shipment.\n\nIn the meantime, you can track your order on our website .\n\nIf you have any questions, feel free to contact us.\n\nBest regards,\nRed Flame & Team',
                'redflamepremium@gmail.com',  # Use a verified email address
                [request.user.email],
                fail_silently=False,
            )

    return render(request, 'core/payment_success.html')



def payment_failed(request):
    return render(request,'core/payment_failed.html')

def order(request):
    ord=Order.objects.filter(user=request.user)
    return render (request,'core/order.html',{'ord':ord})


def buynow(request,id):
    na=new_arrival.objects.get(pk=id)
    Delivery_charge = 149 
    final_price=Delivery_charge + na.discounted_price
    address=Userdetails.objects.filter(user=request.user)
    return render(request,'core/buynow.html',{'final_price':final_price,'address':address,'na':na})

def buynow_payment(request,id):
    if request.method == 'POST':
        selected_address_id= request.POST.get('buynow_selected_address')
    na=new_arrival.objects.get(pk=id)
    Delivery_charge = 149 
    final_price=Delivery_charge + na.discounted_price
    #================= Paypal Code ======================================

    host = request.get_host()   # Will fecth the domain site is currently hosted on.

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'Pet',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('buynowpaymentsuccess', args=[selected_address_id,id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    #========================================================================
    return render(request,'core/payment.html',{'final_price':final_price,'address':address,'na':na,'paypal':paypal_payment})

def buynowpaymentsuccess(request,selected_address_id,id):
    
    user=request.user
    print(user)
    user_data=Userdetails.objects.get(pk=selected_address_id)
    na=new_arrival.objects.get(pk=id)
    Order(user=user,customer=user_data,cloth=na,quantity=1).save()
    return render (request,'core/buynowpaymentsuccess.html')



#================================== Forget Password ====================================================

def forgot_password(request):          
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')           
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_url}',
                'redflamepremium@gmail.com',  # Use a verified email address
                [email],
                fail_silently=False,
            )
            return redirect('passwordresetdone')
        else:
            messages.success(request,'please enter valid email address')
    return render(request, 'core/forgot_password.html')
                                         
    # return render(request,'core/forgot_password.html',)

def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('login')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'core/reset_password.html')

def password_reset_done(request):
    return render(request, 'core/password_reset_done.html')