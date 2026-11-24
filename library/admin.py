from django.contrib import admin
from .models import Book, Member, IssueRecord


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'quantity', 'available_quantity', 'shelf_number')
    list_filter = ('category', 'publication_year')
    search_fields = ('title', 'author', 'isbn', 'category')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'course', 'semester', 'registration_date')
    list_filter = ('course', 'semester')
    search_fields = ('name', 'email', 'phone')


@admin.register(IssueRecord)
class IssueRecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'issue_date', 'due_date', 'return_date', 'status')
    list_filter = ('status', 'issue_date')
    search_fields = ('book__title', 'member__name')
