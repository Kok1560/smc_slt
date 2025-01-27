from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages  # Import Django messages
from django.db.models.deletion import ProtectedError
from datetime import date
from django.contrib.auth.models import User

# Create your views here.

# ======================================= Product Functions ==================================================

def page_list_product(request):
    context = {
        'products' : Product.objects.all(),
    }
    return render(request, 'pages/page-list-product.html', context)

def page_add_product(request):
    if request.method == 'POST':
        add_product = ProductForm(request.POST, request.FILES)
        if add_product.is_valid():
            inventory = Inventory.objects.get(product_name=add_product.cleaned_data.get('product_name'))
            if inventory.real_quantity == inventory.inventory_quantity:
                messages.warning(request, "You Can't Add More Devices")
            else:
                product = add_product.save()
                parent_code = product.product_name
                inventory = Inventory.objects.get(product_name=parent_code)
                inventory.real_quantity = Product.objects.filter(product_name=parent_code).count()
                inventory.save()
                return redirect('/page-add-product')
        else:
            messages.warning(request, "This Device Was Exist!")
            

    context = {
        'productform' : ProductForm()
    }

    return render(request, 'pages/page-add-product.html', context)


def page_update_product(request, id):
    product_id = Product.objects.get(id=id)
    if request.method == 'POST':
        product_save = ProductForm(request.POST, request.FILES, instance=product_id)
        if product_save.is_valid():
            product_save.save()
            return redirect('/page-list-product')
    else:
        product_save = ProductForm(instance=product_id)
        product_save.fields['product_name'].widget = forms.TextInput(attrs={'class':'form-control','readonly': 'readonly'})

    context = {
        'productform' : product_save,
    }
    return render(request, 'pages/page-update-product.html', context)


def page_view_product(request, id):
    product_id = Product.objects.get(id=id)
    context = {
        'productform' : product_id,
    }
    return render(request, 'pages/page-view-product.html', context)

def page_delete_product(request, id):
    product_delete = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product_delete.delete()
        inventory = Inventory.objects.get(product_name=product_delete.product_name)
        inventory.real_quantity = Product.objects.filter(product_name=product_delete.product_name).count()
        inventory.save()
        return redirect('/page-list-product')
    return render(request, 'pages/page-delete-product.html')


# ======================================= Inventory Functions ==================================================

def page_list_inventory(request):
    context = {
        'inventories' : Inventory.objects.all()
    }
    return render(request, 'pages/page-list-inventory.html', context)


def page_add_inventory(request):
    if request.method == 'POST':
        add_inventory = InventoryForm(request.POST, request.FILES)
        if add_inventory.is_valid():
            add_inventory.save()

    context = {
        'inventoryform' : InventoryForm(),
    }

    return render(request, 'pages/page-add-inventory.html', context)

def page_update_inventory(request, id):
    inventory_id = Inventory.objects.get(id=id)
    if request.method == 'POST':
        inventory_save = InventoryForm(request.POST, request.FILES, instance=inventory_id)
        if inventory_save.is_valid():
            if inventory_id.inventory_quantity < inventory_id.real_quantity:
                messages.warning(request, "This Quantity Less Than Devices")
            else:
                inventory_save.save()
            return redirect(f'/page-list-inventory')
    else:
        inventory_save = InventoryForm(instance=inventory_id)
    context = {
        'inventoryform' : inventory_save,
    }
    return render(request, 'pages/page-update-inventory.html', context)


def page_delete_inventory(request, id):
    try:
        inventory_delete = get_object_or_404(Inventory, id=id)
        if request.method == 'POST':
            inventory_delete.delete()
            return redirect('/page-list-inventory')
    except ProtectedError:
        messages.warning(request, "You Should Delete Devices Inside This Parent First.")

    return render(request, 'pages/page-delete-inventory.html')

def page_view_inventory(request, id):
    inventory_id = Inventory.objects.get(id=id)
    context = {
        'inventoryform' : inventory_id,
    }
    return render(request, 'pages/page-view-inventory.html', context)

# ======================================= Party Functions ==================================================

def page_add_party(request):
    if request.method == 'POST':
        add_party = PartyForm(request.POST, request.FILES)
        if add_party.is_valid():
            add_party.save()
            return redirect('/page-add-party')


    context = {
        'partyform' : PartyForm()
    }
    return render(request, 'pages/page-add-party.html', context)


def page_list_party(request):
    context = {
        'parties' : Party.objects.all()
    }
    return render(request, 'pages/page-list-party.html', context)

def page_update_party(request, party_code):
    party_id = Party.objects.get(party_code=party_code)
    if request.method == 'POST':
        party_save = PartyForm(request.POST, request.FILES, instance=party_id)
        if party_save.is_valid():
            party_save.save()
            return redirect('/page-list-party')
    else:
        party_save = PartyForm(instance=party_id)
    context = {
        'partyform' : party_save,
    }
    return render(request, 'pages/page-update-party.html', context)

def page_delete_party(request, party_code):
    try:
        party_delete = get_object_or_404(Party, party_code=party_code)
        if request.method == 'POST':
            party_delete.delete()
            return redirect('/page-list-party')
    except ProtectedError:
        messages.warning(request, "Delete Orders Inside Party First")
    return render(request, 'pages/page-delete-party.html')



# ======================================= Order Functions ==================================================

def page_add_order(request, party_code):
    product_choices = [('', 'Select a product or package')] + [(product.product_id, product.product_id) for product in Product.objects.all()] + [(package.pack_name, package.pack_name) for package in Package.objects.all()]
    maint_devices = [product.product_id for product in Maintenance.objects.all()]
    packages = [package.pack_name for package in Package.objects.all()]
    party = get_object_or_404(Party, party_code=party_code)

    if party.end_date is not None:
        messages.warning(request, 'This Party Was End')
        return redirect('/page-list-party')

    elif request.method == 'POST':
        add_order = OrderForm(request.POST, request.FILES)
        if add_order.is_valid():
            product_name  = add_order.cleaned_data.get('product_id')
            filtered_result = Order.objects.filter(product_id=product_name).last()                    
            products = [product.product_id for product in Order.objects.filter(party_code=party_code).filter(state='add')]
            if product_name in products:
                messages.warning(request, "This Device Was Added")
            elif product_name in maint_devices:
                messages.warning(request, "This Device In Maintenace")

                
            elif product_name in packages:
                package = Package.objects.filter(pack_name=product_name).first()
                if package:
                    state = []
                    products_in_package = Product.objects.filter(pack_name=package)
                    # for product in products_in_package:
                    #     filtered_result = Order.objects.filter(product_id=product).last()
                    #     if filtered_result is None:
                            
                    #     elif filtered_result.state == 'add':
                            
                    #     else:

                    for product in products_in_package:
                        filtered_result = Order.objects.filter(product_id=product).last()
                        # if any(state):
                        #     messages.warning(request, "There's Device In Another Party")
                        #     break
                        if filtered_result is None:
                            Order.objects.create(
                                product_id=product.product_id,
                                party_code=party,
                                state='add'
                            )
                            parent = Product.objects.get(product_id=product).product_name
                            inventory = Inventory.objects.get(product_name=parent)
                            inventory.real_quantity -= 1
                            inventory.save()
                            state.append(False)

                        elif filtered_result.state == 'add':
                            state.append(True)
                            if party != filtered_result.party_code:
                                messages.warning(request, f"{filtered_result.product_id} In Another Party")

                            
                        else:
                            Order.objects.create(
                                product_id=product.product_id,
                                party_code=party,
                                state='add'
                            )
                            parent = Product.objects.get(product_id=product).product_name
                            inventory = Inventory.objects.get(product_name=parent)
                            inventory.real_quantity -= 1
                            inventory.save()
                            state.append(False)
                    if all(state):
                        messages.warning(request, "This Package Was Exist")

                    
                else:
                    messages.warning(request, "No package found with this name")


            elif filtered_result is None:
                add_order.save()
                parent = Product.objects.get(product_id=product_name).product_name
                inventory = Inventory.objects.get(product_name=parent)
                inventory.real_quantity -= 1
                inventory.save()

            elif filtered_result.state == 'add':
                messages.warning(request, "This Device In Another Party")

            else:
                add_order.save()
                parent = Product.objects.get(product_id=product_name).product_name
                inventory = Inventory.objects.get(product_name=parent)
                inventory.real_quantity -= 1
                inventory.save()

            return redirect(f'/add-order-{party_code}')
    else:
        add_order = OrderForm(initial={'party_code' : party_code, 'state' : 'add'})
        add_order.fields['product_id'].widget.choices = product_choices

    context = {
        'orderform' : add_order,
        'orders' : Order.objects.filter(party_code=party_code).filter(state='add'),
    }
    return render(request, 'pages/page-add-order.html', context)



# def add_pack():
#     print(Product.objects.filter(pack_name='mixer expression'))



def delete_product_order(request, id):
    product_delete = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        product_delete.delete()
        product_name = product_delete.product_id
        parent = Product.objects.get(product_id=product_name).product_name
        inventory = Inventory.objects.get(product_name=parent)
        inventory.real_quantity += 1
        inventory.save()
        return redirect(f'/add-order-{product_delete.party_code}')
    return render(request, 'pages/page-delete-order.html')


def invoice_page(request, party_code):
    if Party.objects.get(party_code=party_code).end_date is None:
        messages.warning(request, "This Party Wasn't End Yet")
        return redirect('/page-parties-report')
    party_details = Party.objects.get(party_code=party_code)
    party_orders = Order.objects.filter(party_code=party_code).filter(state='add')
    party_returns = Order.objects.filter(party_code=party_code).filter(state='recovery')

    context = {
        'partydetails' : party_details,
        'partyorders' : party_orders,
        'partyreturns' : party_returns
    }
    return render(request, 'pages/pages-invoice.html', context)

def page_return_order(request, party_code):
    product_choices = [('', 'Select a product')] + [(product.product_id, product.product_id) for product in Order.objects.filter(party_code=party_code).filter(state='add')]
    if Party.objects.get(party_code=party_code).end_date != None:
        messages.warning(request, 'This Party Was End')
        return redirect('/page-list-party')
    elif request.method == 'POST':
        return_order = OrderForm(request.POST, request.FILES)
        if return_order.is_valid():
            products = [product.product_id for product in Order.objects.filter(party_code=party_code).filter(state='recovery')]
            if return_order.cleaned_data.get('product_id') in products:
                messages.warning(request, "This Device Was Added")
            else:
                return_order.save()
                product_name = return_order.cleaned_data.get('product_id')
                product = Product.objects.get(product_id=product_name)
                inventory = Inventory.objects.get(product_name=product.product_name)
                inventory.real_quantity += 1
                product.amount_of_parties += 1
                inventory.save()
                product.save()
                add_prouducts = [product.product_id for product in Order.objects.filter(party_code=party_code).filter(state='add')]
                recovery_products = [product.product_id for product in Order.objects.filter(party_code=party_code).filter(state='recovery')]
                add_prouducts.sort()
                recovery_products.sort()

                if add_prouducts == recovery_products:
                    party = Party.objects.get(party_code=party_code)
                    party.end_date = date.today()
                    party.save()

            return redirect(f'/return-order-{party_code}')
    else:
        return_order = OrderForm(initial={'party_code' : party_code, 'state' : 'recovery'})
        return_order.fields['product_id'].widget.choices = product_choices

    context = {
        'returnform' : return_order,
        'orders' : Order.objects.filter(party_code=party_code).filter(state='add'),
        'returnorders' : Order.objects.filter(party_code=party_code).filter(state='recovery')

    }
    return render(request, 'pages/page-return-order.html', context)




# ======================================= Maintenance Functions ==================================================

def page_add_maint(request):
    product_choices = [('', 'Select a product')] + [(product.product_id, product.product_id) for product in Product.objects.all()]
    if request.method == 'POST':
        add_maint = MaintForm(request.POST, request.FILES)
        if add_maint.is_valid():
            product_name = add_maint.cleaned_data.get('product_id')
            filtered_result = Order.objects.filter(product_id=product_name).last()                    
            products = [product.product_id for product in Maintenance.objects.all()]
            if add_maint.cleaned_data.get('product_id') in products:
                messages.warning(request, "This Device Was Added")

            elif filtered_result is None:
                add_maint.save()
                parent = Product.objects.get(product_id=product_name).product_name
                inventory = Inventory.objects.get(product_name=parent)
                inventory.real_quantity -= 1
                inventory.save()

            elif filtered_result.state == 'add':
                messages.warning(request, "This Device In Party")

            else:
                add_maint.save()
                parent = Product.objects.get(product_id=product_name).product_name
                inventory = Inventory.objects.get(product_name=parent)
                inventory.real_quantity -= 1
                inventory.save()

            return redirect('/page-add-maint')

    else:
        add_maint = MaintForm()
        add_maint.fields['product_id'].widget.choices = product_choices

    context = {
        'maintform' : add_maint
    }

    return render(request, 'pages/page-add-maint.html', context)


def page_list_maint(request):
    context = {
        'maints' : Maintenance.objects.all()
    }
    return render(request, 'pages/page-list-maint.html', context)

def page_delete_maint(request, id):
    maint_delete = get_object_or_404(Maintenance, id=id)
    if request.method == 'POST':
        maint_delete.delete()
        product_name = maint_delete.product_id
        parent = Product.objects.get(product_id=product_name).product_name
        inventory = Inventory.objects.get(product_name=parent)
        inventory.real_quantity += 1
        inventory.save()
        return redirect('/page-list-maint')
    return render(request, 'pages/page-delete-maint.html')



# ======================================= Reports Functions ==================================================

def page_product_report(request):
    context = {
        'productsreport' : Product.objects.all()
    }
    return render(request, 'pages/page-product-report.html', context)

def page_inventory_report(request):
    context = {
        'inventoryreport' : Inventory.objects.all()
    }
    return render(request, 'pages/page-inventory-report.html', context)

def page_parties_report(request):
    context = {
        'partiesreport' : Party.objects.all()
    }
    return render(request, 'pages/page-Parties-report.html', context)

def search_for_device(request, id):
    product_id = Product.objects.get(id=id)
    product_name = product_id.product_id
    filtered_result = Order.objects.filter(product_id=product_name).last()
    maint_devices = [product.product_id for product in Maintenance.objects.all()]

    if product_name in maint_devices:
        place = "This Device In Maintenance"

    elif filtered_result is None:
        place = f"This Device In Inventory"

    elif filtered_result.state == "add":
        place = f"This Device In Party Has Code: {filtered_result.party_code}"
    else:
        place = "This Device In Inventory"

    context = {
        'place' : place,
        'product_name' : product_name
    }
    return render(request, 'pages/search-for-device.html', context)

# ======================================= Users Functions ==================================================

def page_list_users(request):
    context = {
        'form' : User.objects.all()
    }
    return render(request, 'pages/page-list-users.html', context)

# ======================================= Package Functions ==================================================

def page_add_package(request):
    if request.method == 'POST':
        add_package = PackageForm(request.POST, request.FILES)
        if add_package.is_valid():
            add_package.save()
            return redirect('/page-add-package')


    context = {
        'packageform' : PackageForm()
    }
    return render(request, 'pages/page-add-package.html', context)

def page_list_package(request):
    context = {
        'packageform' : Package.objects.all()
    }
    return render(request, 'pages/page-list-package.html', context)


def page_update_package(request, id):
    pack_id = Package.objects.get(id=id)
    if request.method == 'POST':
        pack_save = PackageForm(request.POST, instance=pack_id)
        if pack_save.is_valid():
            pack_save.save()
            return redirect('/page-list-package')
    else:
        pack_save = PackageForm(instance=pack_id)

    context = {
        'packform' : pack_save,
    }
    return render(request, 'pages/page-update-package.html', context)

def delete_package(request, id):
    try:
        pack_delete = get_object_or_404(Package, id=id)
        if request.method == 'POST':
            pack_delete.delete()
            return redirect('/page-list-package')
    except ProtectedError:
        messages.warning(request, "Delete Orders Inside Party First")
    return render(request, 'pages/page-delete-package.html')
