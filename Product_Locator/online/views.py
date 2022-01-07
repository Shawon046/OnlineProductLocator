from django.shortcuts import render, redirect
from shopDB.models import Discount
from django.contrib import messages

# Create your views here.
def add_Disc(request):
    if request.method == 'POST':
        print('YES')
        percen = request.POST.get('percentage')
        max_amount = request.POST.get('mx_amnt')
        diamount = request.POST.get('disc_amnt')

        if percen == "":
            perc = None
        else :
            perc = float(percen)

        if max_amount == "":
            max_amnt = None
        else :
            max_amnt = int(max_amount)

        if diamount == "":
            diamnt = None
        else :
            diamnt = float(diamount)

        new_disc = Discount(Percentage=perc, DiscountAmount=diamnt, MaxAmount=max_amnt)
        new_disc.save()
        messages.success(request, "Discount Added", )
        return render(request, 'Discount_add_pop.html')

    return render(request, 'Discount_add_pop.html')