from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .forms import CForm, CustomerForm,PForm,CovidForm


from .models import Customer, Medicine,Category,Order,OrderItem,Covid, Prescription
# Create your views here.
def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"user does not exist")

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')
    context={'page':page}
    return render(request,'base/login.html',context)


def layout(request):
    return render(request,'base/layout.html')


def home(request):
    return render(request,'base/home.html')


def billing(request,ck):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    medicines=Medicine.objects.filter(Q(category__name__icontains=q)| Q(name__icontains=q)| Q(description__icontains=q))
    categories=Category.objects.all()

    context={"categories":categories,"medicines":medicines,"ck":ck}

    return render(request,'base/billing.html',context)






def add_to_cart(request,pk,ck):
    
    item = get_object_or_404(Medicine, id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        customer=Customer.objects.get(phno=ck),
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('cart',ck=ck)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('billing',ck=ck)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date,customer=Customer.objects.get(phno=ck))
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('billing',ck=ck)


def order_summary(request,ck):
    order = Order.objects.get(user=request.user, ordered=False,customer=Customer.objects.get(phno=ck))
    
    ali=0
    items=OrderItem.objects.filter(order=order)
    for each_item in items:
        if each_item.item.ali==True:
            ali=1

    context = {'object': order,'ck':ck,'ali':ali}
    return render(request,'base/cart.html',context)


def checkout(request,ck,ali):
    if ali==1:
        customer=Customer.objects.get(phno=ck)
        form=CustomerForm(instance=customer)
        if request.method == 'POST':
            form = CustomerForm(request.POST,instance=customer)
            if form.is_valid():
                form.save()
                return redirect('checkout2',ck=ck)

        return render(request,"base/covid_form.html",{'form': form})
    else:
        order = Order.objects.get(user=request.user, ordered=False,customer=Customer.objects.get(phno=ck))
        customer=Customer.objects.get(phno=ck)
        form=PForm()
        if request.method == 'POST':
            form = PForm(request.POST, request.FILES)
            if form.is_valid():
                prescription=form.save(commit=False)
                prescription.order=order;
                prescription.save()
                return redirect('bill',ck=ck)
                
            

        return render(request,"base/checkout.html",{'form': form,'order':order})

def c_form(request,ck):

    form=CovidForm()

    if request.method == 'POST':
        
        
        form=CovidForm(request.POST)
        if form.is_valid:
            form.save
        return redirect('checkout',ck=ck,ali=0)
        


    return render(request,"base/cform.html",{'form': form})




def remove_from_cart(request, pk,ck):
    item = get_object_or_404(Medicine, id=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        customer=Customer.objects.get(phno=ck)
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                
                ordered=False,
                customer=Customer.objects.get(phno=ck)
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("cart",ck=ck)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart",ck=ck)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart",ck=ck)


def remove_single_item_from_cart(request, pk,ck):
    item = get_object_or_404(Medicine, id=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
        customer=Customer.objects.get(phno=ck)

    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                
                ordered=False,
                customer=Customer.objects.get(phno=ck)
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cart",ck=ck)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart",ck=ck)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart",ck=ck)



def bill(request,ck):
    order = Order.objects.get(user=request.user, ordered=False,customer=Customer.objects.get(phno=ck))
    customer=Customer.objects.get(phno=ck)
    context={'object':order,'customer':customer}
    return render(request,'base/bill.html',context)


def register(request):
    form=CForm()
    if request.method == 'POST':
            form = CForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()

            return redirect('home')

    return render(request,'base/register.html',{'form':form})


def billing1(request):
    if request.method=='POST':
        phno=request.POST.get('phno')
        try:
            customer=Customer.objects.get(phno=phno)
            return redirect('billing',ck=phno)
        except:
            return redirect('billing1')
    return render(request,'base/billing1.html')
