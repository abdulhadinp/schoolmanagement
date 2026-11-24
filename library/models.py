
from django.db import models
from django.urls import reverse
from datetime import date


class Book(models.Model):
    """A single book title held by the library."""

    isbn = models.CharField('ISBN', max_length=20, unique=True)
    title = models.CharField('Book Title', max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    publisher = models.CharField(max_length=255, blank=True)
    publication_year = models.PositiveIntegerField('Publication Year')
    quantity = models.PositiveIntegerField(default=1, help_text='Total copies owned by the library')
    available_quantity = models.PositiveIntegerField(default=1, help_text='Copies currently available to issue')
    shelf_number = models.CharField('Shelf/Rack Number', max_length=50, blank=True)
    description = models.TextField('Book Description', blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.pk])

    @property
    def is_available(self):
        return self.available_quantity > 0


class Member(models.Model):
    """A student / member registered with the library."""

    name = models.CharField('Student Name', max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True)
    course = models.CharField('Course/Faculty', max_length=150)
    semester = models.CharField(max_length=20, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('member_detail', args=[self.pk])


class IssueRecord(models.Model):
    """A record of a book being issued to a member, and (later) returned."""

    STATUS_ISSUED = 'Issued'
    STATUS_RETURNED = 'Returned'
    STATUS_CHOICES = [
        (STATUS_ISSUED, 'Issued'),
        (STATUS_RETURNED, 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issue_records')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='issue_records')
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ISSUED)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f'{self.book.title} -> {self.member.name} ({self.status})'

    @property
    def is_overdue(self):
        if self.status == self.STATUS_RETURNED:
            return False
        return date.today() > self.due_date

    @property
    def overdue_days(self):
        if not self.is_overdue:
            return 0
        return (date.today() - self.due_date).days
        
