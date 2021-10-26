from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'ShopCons/home.html')


# For showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'ShopCons/adminclick.html')


# For showing signup/login button for shopkeeper
def shopclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'ShopCons/shopclick.html')


# For showing signup/login button for consumer
def consclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'ShopCons/consclick.html')


def shop_signup_view(request):
    if request.method == 'POST':
        userForm = forms.ShopkeeperUserForm(request.POST)
        shopForm = forms.ShopkeeperForm(request.POST, request.FILES)
        if userForm.is_valid() and shopForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            shop = shopForm.save(commit=False)
            shop.user = user
            shop.save()
            my_shop_group = Group.objects.get_or_create(name='SHOP')
            my_shop_group[0].user_set.add(user)
            return redirect('shoplogin')
    else:
        userForm = forms.ShopkeeperUserForm()
        shopForm = forms.ShopkeeperForm()
    mydict = {'userForm': userForm, 'shopForm': shopForm}
    return render(request, 'ShopCons/shopsignup.html', context=mydict)


def cons_signup_view(request):
    if request.method == 'POST':
        userForm = forms.ConsumerUserForm(request.POST)
        consForm = forms.ConsumerForm(request.POST, request.FILES)
        if userForm.is_valid() and consForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            cons = consForm.save(commit=False)
            cons.user = user
            cons.assignedShopId = request.POST.get('assignedShopId')
            cons.save()
            my_cons_group = Group.objects.get_or_create(name='CONS')
            my_cons_group[0].user_set.add(user)
            return redirect('conslogin')
    else:
        userForm = forms.ConsumerUserForm()
        consForm = forms.ConsumerForm()
    mydict = {'userForm': userForm, 'consForm': consForm}
    return render(request, 'ShopCons/conssignup.html', context=mydict)


# For checking User is Shopkeeper , Consumer or Admin
def is_admin(user):
    if user.is_staff or user.is_superuser:
        return True
    return False


def is_shop(user):
    return user.groups.filter(name='SHOP').exists()


def is_cons(user):
    return user.groups.filter(name='CONS').exists()


@login_required
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-shop')
    elif is_shop(request.user):
        accountapproval = models.Shopkeeper.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('shop-view-cons')
        else:
            return render(request, 'ShopCons/shop_wait_for_approval.html')
    elif is_cons(request.user):
        accountapproval = models.Consumer.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('cons-admit')
        else:
            return render(request, 'ShopCons/cons_wait_for_approval.html')


# ADMIN RELATED VIEWS START

# This view for sidebar click on Admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_shop_view(request):
    shop = models.Shopkeeper.objects.all().order_by('-id')

    mydict = {
        'shop': shop,
    }
    return render(request, 'ShopCons/admin_shop.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_shop_view(request):
    shop = models.Shopkeeper.objects.all().filter(status=True)
    return render(request, 'ShopCons/admin_view_shop.html', {'shop': shop})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_shop_view(request, pk):
    shop = models.Shopkeeper.objects.get(id=pk)
    user = models.User.objects.get(id=shop.user_id)
    user.delete()
    shop.delete()
    return redirect('admin-view-shop')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_shop_view(request, pk):
    shop = models.Shopkeeper.objects.get(id=pk)
    user = models.User.objects.get(id=shop.user_id)

    userForm = forms.ShopkeeperUserForm(instance=user)
    shopForm = forms.ShopkeeperForm(request.FILES, instance=shop)
    if request.method == 'POST':
        userForm = forms.ShopkeeperUserForm(request.POST, instance=user)
        shopForm = forms.ShopkeeperForm(request.POST, request.FILES, instance=shop)
        if userForm.is_valid() and shopForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            shop = shopForm.save(commit=False)
            shop.status = True
            shop.save()
            return redirect('admin-view-shop')
    mydict = {'userForm': userForm, 'shopForm': shopForm}
    return render(request, 'ShopCons/admin_update_shop.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_shop_view(request):
    if request.method == 'POST':
        userForm = forms.ShopkeeperUserForm(request.POST)
        shopForm = forms.ShopkeeperForm(request.POST, request.FILES)
        if userForm.is_valid() and shopForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            shop = shopForm.save(commit=False)
            shop.user = user
            shop.status = True
            shop.save()

            my_shop_group = Group.objects.get_or_create(name='SHOP')
            my_shop_group[0].user_set.add(user)
            return redirect('admin-view-shop')
    else:
        userForm = forms.ShopkeeperUserForm()
        shopForm = forms.ShopkeeperForm()
    mydict = {'userForm': userForm, 'shopForm': shopForm}
    return render(request, 'ShopCons/admin_add_shop.html', context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_shop_view(request):
    shop = models.Shopkeeper.objects.all().filter(status=False)
    return render(request, 'ShopCons/admin_approve_shop.html', {'shop': shop})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_shop_view(request, pk):
    shop = models.Shopkeeper.objects.get(id=pk)
    shop.status = True
    shop.save()
    return redirect(reverse('admin-approve-shop'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_shop_view(request, pk):
    shop = models.Shopkeeper.objects.get(id=pk)
    user = models.User.objects.get(id=shop.user_id)
    user.delete()
    shop.delete()
    return redirect('admin-approve-shop')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_shop_depart_view(request):
    shop = models.Shopkeeper.objects.all().filter(status=True)
    return render(request, 'ShopCons/admin_view_shop_depart.html', {'shop': shop})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_cons_view(request):
    return render(request, 'ShopCons/admin_cons.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_cons_view(request):
    cons = models.Consumer.objects.all().filter(status=True)
    return render(request, 'ShopCons/admin_view_cons.html', {'cons': cons})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_cons_view(request, pk):
    cons = models.Consumer.objects.get(id=pk)
    user = models.User.objects.get(id=cons.user_id)
    user.delete()
    cons.delete()
    return redirect('admin-view-cons')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_cons_view(request, pk):
    cons = models.Consumer.objects.get(id=pk)
    user = models.User.objects.get(id=cons.user_id)

    userForm = forms.ConsumerUserForm(instance=user)
    consForm = forms.ConsumerForm(request.FILES, instance=cons)

    if request.method == 'POST':
        userForm = forms.ConsumerUserForm(request.POST, instance=user)
        consForm = forms.ConsumerForm(request.POST, request.FILES, instance=cons)

        if userForm.is_valid() and consForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            cons = consForm.save(commit=False)
            cons.status = True
            cons.assignedShopId = request.POST.get('assignedShopId')
            cons.save()
            return redirect('admin-view-cons')
    mydict = {'userForm': userForm, 'consForm': consForm}
    return render(request, 'ShopCons/admin_update_cons.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_cons_view(request):
    if request.method == 'POST':
        userForm = forms.ConsumerUserForm(request.POST)
        consForm = forms.ConsumerForm(request.POST, request.FILES)
        if userForm.is_valid() and consForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            cons = consForm.save(commit=False)
            cons.user = user
            cons.status = True
            cons.assignedShopId = request.POST.get('assignedShopId')
            cons.save()

            my_cons_group = Group.objects.get_or_create(name='CONS')
            my_cons_group[0].user_set.add(user)
            return redirect('admin-view-cons')
    else:
        userForm = forms.ConsumerUserForm()
        consForm = forms.ConsumerForm()
    mydict = {'userForm': userForm, 'consForm': consForm}
    return render(request, 'ShopCons/admin_add_cons.html', context=mydict)


# For approving Consumer by Admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_cons_view(request):
    cons = models.Consumer.objects.all().filter(status=False)
    return render(request, 'ShopCons/admin_approve_cons.html', {'cons': cons})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_cons_view(request, pk):
    cons = models.Consumer.objects.get(id=pk)
    cons.status = True
    cons.save()
    return redirect(reverse('admin-approve-cons'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_cons_view(request, pk):
    cons = models.Consumer.objects.get(id=pk)
    user = models.User.objects.get(id=cons.user_id)
    user.delete()
    cons.delete()
    return redirect('admin-approve-cons')


# Admit Start
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_admit_view(request):
    return render(request, 'ShopCons/admin_admit.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_admit_view(request):
    admits = models.Admit.objects.all().filter(status=True)
    return render(request, 'ShopCons/admin_view_admit.html', {'admits': admits})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_admit_view(request):
    admitForm = forms.AdmitForm()
    mydict = {'admitForm': admitForm, }
    if request.method == 'POST':
        admitForm = forms.AdmitForm(request.POST)
        if admitForm.is_valid():
            admit = admitForm.save(commit=False)
            admit.shopId = request.POST.get('shopId')
            admit.consId = request.POST.get('consId')
            shop = models.Shopkeeper.objects.get(user_id=admit.shopId)
            admit.shopName = shop.shopname
            # admit.shopName = models.User.objects.get(id=request.POST.get('shopId')).shopname
            admit.consName = models.User.objects.get(id=request.POST.get('consId')).first_name
            admit.status = True
            admit.save()
        return HttpResponseRedirect('admin-view-admit')
    return render(request, 'ShopCons/admin_add_admit.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_admit_view(request):
    admits = models.Admit.objects.all().filter(status=False)
    return render(request, 'ShopCons/admin_approve_admit.html', {'admits': admits})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_admit_view(request, pk):
    admit = models.Admit.objects.get(id=pk)
    admit.status = True
    admit.save()
    return redirect(reverse('admin-approve-admit'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_admit_view(request, pk):
    admit = models.Admit.objects.get(id=pk)
    admit.delete()
    return redirect('admin-approve-admit')
# ADMIN RELATED VIEWS END


# SHOPKEEPER RELATED VIEWS START

@login_required(login_url='shoplogin')
@user_passes_test(is_shop)
def shop_cons_view(request):
    mydict = {
        'shop': models.Shopkeeper.objects.get(user_id=request.user.id),  
    }
    return render(request, 'ShopCons/shop_cons.html', context=mydict)


@login_required(login_url='shoplogin')
@user_passes_test(is_shop)
def shop_view_cons_view(request):
    shop = models.Shopkeeper.objects.get(user_id=request.user.id)
    cons = models.Consumer.objects.all().filter(status=True, assignedShopId=shop.shopname)
    return render(request, 'ShopCons/shop_view_cons.html', {'cons': cons, 'shop': shop})


@login_required(login_url='shoplogin')
@user_passes_test(is_shop)
def search_view(request):
    shop = models.Shopkeeper.objects.get(user_id=request.user.id)  
    # Whatever user write in search box we get in query
    query = request.GET['query']
    cons = models.Consumer.objects.all().filter(status=True, assignedShopId=shop.shopname).filter(
        Q(adhaarnum__icontains=query) | Q(user__first_name__icontains=query))
    return render(request, 'ShopCons/shop_view_cons.html', {'cons': cons, 'shop': shop})


@login_required(login_url='shoplogin')
@user_passes_test(is_shop)
def shop_admit_view(request):
    shop = models.Shopkeeper.objects.get(user_id=request.user.id)  
    return render(request, 'ShopCons/shop_admit.html', {'shop': shop})


@login_required(login_url='shoplogin')
@user_passes_test(is_shop)
def shop_view_admit_view(request):
    shop = models.Shopkeeper.objects.get(user_id=request.user.id)  
    admits = models.Admit.objects.all().filter(status=True, shopId=request.user.id)
    considList = []
    for a in admits:
        considList.append(a.consId)
    cons = models.Consumer.objects.all().filter(status=True, user_id__in=considList)
    admits = zip(admits, cons)
    return render(request, 'ShopCons/shop_view_admit.html', {'admits': admits, 'shop': shop})


@login_required(login_url='shoplogin')
@user_passes_test(is_shop)
def shop_delete_admit_view(request):
    shop = models.Shopkeeper.objects.get(user_id=request.user.id)  
    admits = models.Admit.objects.all().filter(status=True, shopId=request.user.id)
    considList = []
    for a in admits:
        considList.append(a.consId)
    cons = models.Consumer.objects.all().filter(status=True, user_id__in=considList)
    admits = zip(admits, cons)
    return render(request, 'ShopCons/shop_delete_admit.html', {'admits': admits, 'shop': shop})


@login_required(login_url='shoplogin')
@user_passes_test(is_shop)
def delete_admit_view(request, pk):
    admit = models.Admit.objects.get(id=pk)
    admit.delete()
    shop = models.Shopkeeper.objects.get(user_id=request.user.id)  
    admits = models.Admit.objects.all().filter(status=True, shopId=request.user.id)
    considList = []
    for a in admits:
        considList.append(a.consId)
    cons = models.Consumer.objects.all().filter(status=True, user_id__in=considList)
    admits = zip(admits, cons)
    return render(request, 'ShopCons/shop_delete_admit.html', {'admits': admits, 'shop': shop})

# SHOPKEEPER RELATED VIEWS END


# CONSUMER RELATED VIEWS START

@login_required(login_url='conslogin')
@user_passes_test(is_cons)
def cons_admit_view(request):
    cons = models.Consumer.objects.get(user_id=request.user.id)  
    return render(request, 'ShopCons/cons_admit.html', {'cons': cons})


@login_required(login_url='conslogin')
@user_passes_test(is_cons)
def cons_book_admit_view(request):
    admitForm = forms.ConAdmitForm()
    cons = models.Consumer.objects.get(user_id=request.user.id)  
    mydict = {'admitForm': admitForm, 'cons': cons}
    if request.method == 'POST':
        admitForm = forms.ConAdmitForm(request.POST)
        if admitForm.is_valid():

            shop = models.Shopkeeper.objects.get(user_id=request.POST.get('shopId'))

            admit = admitForm.save(commit=False)
            admit.shopId = request.POST.get('shopId')
            admit.consId = request.user.id
            admit.shopName = models.Shopkeeper.objects.get(user_id=admit.shopId).shopname
            admit.consName = request.user.first_name
            admit.status = False
            admit.save()
        return HttpResponseRedirect('cons-view-admit')
    return render(request, 'ShopCons/cons_book_admit.html', context=mydict)


def cons_view_shop_view(request):
    shop = models.Shopkeeper.objects.all().filter(status=True)
    cons = models.Consumer.objects.get(user_id=request.user.id)  
    return render(request, 'ShopCons/cons_view_shop.html', {'cons': cons, 'shop': shop})


def search_shop_view(request):
    cons = models.Consumer.objects.get(user_id=request.user.id)  

    # Whatever user write in search box we get in query
    query = request.GET['query']
    shop = models.Shopkeeper.objects.all().filter(status=True).filter(
        Q(shoptype__icontains=query) | Q(shopname__icontains=query) | Q(user__first_name__icontains=query))
    return render(request, 'ShopCons/cons_view_shop.html', {'cons': cons, 'shop': shop})


@login_required(login_url='conslogin')
@user_passes_test(is_cons)
def cons_view_admit_view(request):
    cons = models.Consumer.objects.get(user_id=request.user.id)  
    admits = models.Admit.objects.all().filter(consId=request.user.id)

    shopidList = []
    for a in admits:
        shopidList.append(a.shopId)
    shop = models.Shopkeeper.objects.all().filter(status=True, user_id__in=shopidList)
    admits = zip(admits, shop)

    return render(request, 'ShopCons/cons_view_admit.html', {'admits': admits, 'cons': cons})

# CONSUMER RELATED VIEWS END


# ABOUT US AND CONTACT US VIEWS START
def aboutus_view(request):
    return render(request, 'ShopCons/aboutus.html')

def career_view(request):
    return render(request, 'ShopCons/career.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email), message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'ShopCons/contactussuccess.html')
    return render(request, 'ShopCons/contactus.html', {'form': sub})
