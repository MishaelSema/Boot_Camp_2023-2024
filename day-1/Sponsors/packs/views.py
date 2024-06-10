from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pack, Subscription, Item
from .forms import SubscriptionForm, ItemSelectionForm

def pack_list(request):
    packs = Pack.objects.all()
    items = Item.objects.all()
    return render(request, 'packs/pack_list.html', {'packs': packs, 'items': items})

def subscribe(request, pack_id):
    pack = Pack.objects.get(id=pack_id)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.pack = pack
            subscription.save()  # Save without passing items
            subscription.items.set(pack.description.all())  # Set the items after saving the instance
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('thank_you')
    else:
        form = SubscriptionForm()
    return render(request, 'packs/subscribe.html', {'form': form, 'pack': pack})

def thank_you(request):
    return render(request, 'packs/thank_you.html')

def create_custom_plan(request):
    items = Item.objects.all()
    if request.method == 'POST':
        item_form = ItemSelectionForm(request.POST)
        if item_form.is_valid():
            selected_items = item_form.cleaned_data['items']
            request.session['selected_items'] = [item.id for item in selected_items]
            return redirect('create_subscription')
    else:
        item_form = ItemSelectionForm()
    return render(request, 'packs/create_custom_plan.html', {'item_form': item_form, 'items': items})

def create_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            selected_item_ids = request.session.get('selected_items', [])
            form.instance.selected_items = selected_item_ids  # Set the selected items
            subscription = form.save(commit=False)
            subscription.pack_id = None  # Set pack_id to None for custom plan
            subscription.save()  # Save the subscription instance to generate its ID
            selected_items = Item.objects.filter(id__in=selected_item_ids)
            subscription.items.set(selected_items)  # Set the selected items for custom plan
            subscription.amount_per_month = subscription.calculate_price()  # Calculate and save amount per month
            subscription.save()  # Save the subscription instance with the calculated amount per month
            return redirect('thank_you')
    else:
        form = SubscriptionForm()
    return render(request, 'packs/subscribe.html', {'form': form, 'custom_plan': True})
