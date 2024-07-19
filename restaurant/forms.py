from datetime import timezone
from django import forms
from django.forms import ModelForm
from .models import Booking


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get("booking_date")
        if booking_date <= timezone.now():
            raise forms.ValidationError("Booking date must be in the future.")
        return booking_date

    def clean(self):
        cleaned_data = super().clean()  # Get the cleaned data from the parent form
        return cleaned_data
