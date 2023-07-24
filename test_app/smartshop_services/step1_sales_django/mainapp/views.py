from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView
from .models import Phone
import requests


class PhoneListView(ListView):
    paginate_by = 10
    model = Phone


def sale_view(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    data = {"phone": f"{phone.brand.name} {phone.name}", "price": phone.sale_cost}
    requests.post("http://10.5.0.6:5000/sale/", data=data)
    return HttpResponseRedirect("/")


def repair_view(request, pk):
    phone = get_object_or_404(Phone, pk=pk)
    data = {"phone": f"{phone.brand.name} {phone.name}", "price": phone.repair_cost}
    requests.post("http://10.5.0.6:5000/repair/", data=data)
    return HttpResponseRedirect("/")
