from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Book, Member, IssueRecord


class BootstrapModelForm(forms.ModelForm):
    """Adds Bootstrap's 'form-control' class to every field automatically,
    so we don't have to repeat it on every single field."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            if isinstance(field.widget, (forms.CheckboxInput,)):
                field.widget.attrs['class'] = (existing + ' form-check-input').strip()
            else:
                field.widget.attrs['class'] = (existing + ' form-control').strip()


class BookForm(BootstrapModelForm):
    class Meta:
        model = Book
        fields = [
            'isbn', 'title', 'author', 'category', 'publisher',
            'publication_year', 'quantity', 'available_quantity',
            'shelf_number', 'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        available_quantity = cleaned_data.get('available_quantity')
        if quantity is not None and available_quantity is not None:
            if available_quantity > quantity:
                raise forms.ValidationError(
                    'Available quantity cannot be greater than total quantity.'
                )
        return cleaned_data


class MemberForm(BootstrapModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone', 'address', 'course', 'semester']


class IssueBookForm(BootstrapModelForm):
    class Meta:
        model = IssueRecord
        fields = ['member', 'book', 'issue_date', 'due_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show books that currently have at least one available copy.
        self.fields['book'].queryset = Book.objects.filter(available_quantity__gt=0)
        if not self.instance.pk:
            today = timezone.localdate()
            self.fields['issue_date'].initial = today
            self.fields['due_date'].initial = today + timedelta(days=14)

    def clean_book(self):
        book = self.cleaned_data['book']
        if book.available_quantity <= 0:
            raise forms.ValidationError('This book has no available copies to issue.')
        return book

    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        due_date = cleaned_data.get('due_date')
        if issue_date and due_date and due_date < issue_date:
            raise forms.ValidationError('Due date cannot be before the issue date.')
        return cleaned_data
