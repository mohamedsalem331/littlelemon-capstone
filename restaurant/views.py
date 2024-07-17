from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Menu, Booking
from .serializers import BookingSerializer, MenuSerializer
from rest_framework.permissions import IsAuthenticated
from .forms import BookingForm

def home(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html')

def menu(request):
    menu_data = Menu.objects.all()
    menu_data = menu_data.order_by('price')
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})

def single_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = Menu.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = MenuSerializer

# class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Menu.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = MenuSerializer

# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = BookingSerializer