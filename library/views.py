from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import Book, Member, IssueRecord
from .forms import BookForm, MemberForm, IssueBookForm


@login_required
def dashboard(request):
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    total_issued = IssueRecord.objects.filter(status=IssueRecord.STATUS_ISSUED).count()
    total_available = sum(b.available_quantity for b in Book.objects.all())
    overdue_qs = [r for r in IssueRecord.objects.filter(status=IssueRecord.STATUS_ISSUED) if r.is_overdue]

    context = {
        'total_books': total_books,
        'total_members': total_members,
        'total_issued': total_issued,
        'total_available': total_available,
        'overdue_count': len(overdue_qs),
        'recent_issues': IssueRecord.objects.order_by('-issue_date')[:5],
        'recent_returns': IssueRecord.objects.filter(
            status=IssueRecord.STATUS_RETURNED
        ).order_by('-return_date')[:5],
    }
    return render(request, 'library/dashboard.html', context)


# Books 

@login_required
def book_list(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query) |
            Q(category__icontains=query)
        )
    return render(request, 'library/book_list.html', {'books': books, 'query': query})


@login_required
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully.')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Add Book'})


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form, 'title': 'Edit Book'})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('book_list')
    return render(request, 'library/confirm_delete.html', {'object': book, 'type': 'book'})


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    history = book.issue_records.all()[:20]
    return render(request, 'library/book_detail.html', {'book': book, 'history': history})


# ---------- Members ----------

@login_required
def member_list(request):
    query = request.GET.get('q', '').strip()
    members = Member.objects.all()
    if query:
        members = members.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    return render(request, 'library/member_list.html', {'members': members, 'query': query})


@login_required
def member_add(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully.')
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'library/member_form.html', {'form': form, 'title': 'Add Member'})


@login_required
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member updated successfully.')
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm(instance=member)
    return render(request, 'library/member_form.html', {'form': form, 'title': 'Edit Member'})


@login_required
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Member deleted successfully.')
        return redirect('member_list')
    return render(request, 'library/confirm_delete.html', {'object': member, 'type': 'member'})


@login_required
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    history = member.issue_records.all()[:20]
    return render(request, 'library/member_detail.html', {'member': member, 'history': history})


# ---------- Issue / Return ----------

@login_required
def issue_book(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            book = issue.book
            if book.available_quantity <= 0:
                messages.error(request, 'This book is not available right now.')
            else:
                book.available_quantity -= 1
                book.save()
                issue.status = IssueRecord.STATUS_ISSUED
                issue.save()
                messages.success(request, f'"{book.title}" issued to {issue.member.name}.')
                return redirect('issued_books')
    else:
        form = IssueBookForm()
    return render(request, 'library/issue_form.html', {'form': form})


@login_required
def issued_books(request):
    query = request.GET.get('q', '').strip()
    records = IssueRecord.objects.filter(status=IssueRecord.STATUS_ISSUED)
    if query:
        records = records.filter(
            Q(member__name__icontains=query) | Q(book__title__icontains=query)
        )
    return render(request, 'library/issued_list.html', {'records': records, 'query': query})


@login_required
def returned_books(request):
    query = request.GET.get('q', '').strip()
    records = IssueRecord.objects.filter(status=IssueRecord.STATUS_RETURNED)
    if query:
        records = records.filter(
            Q(member__name__icontains=query) | Q(book__title__icontains=query)
        )
    return render(request, 'library/returned_list.html', {'records': records, 'query': query})


@login_required
def return_book(request, pk):
    record = get_object_or_404(IssueRecord, pk=pk, status=IssueRecord.STATUS_ISSUED)
    if request.method == 'POST':
        record.return_date = timezone.localdate()
        record.status = IssueRecord.STATUS_RETURNED
        record.save()

        book = record.book
        book.available_quantity += 1
        book.save()

        messages.success(request, f'"{book.title}" marked as returned.')
        return redirect('issued_books')
    return render(request, 'library/confirm_return.html', {'record': record})


@login_required
def overdue_books(request):
    query = request.GET.get('q', '').strip()
    records = IssueRecord.objects.filter(status=IssueRecord.STATUS_ISSUED)
    if query:
        records = records.filter(
            Q(member__name__icontains=query) | Q(book__title__icontains=query)
        )
    overdue = [r for r in records if r.is_overdue]
    return render(request, 'library/overdue_list.html', {'records': overdue, 'query': query})


@login_required
def returned_books(request):
    query = request.GET.get('q', '').strip()
    records = IssueRecord.objects.filter(status=IssueRecord.STATUS_RETURNED)
    if query:
        records = records.filter(
            Q(member__name__icontains=query) | Q(book__title__icontains=query)
        )
    return render(request, 'library/returned_list.html', {'records': records, 'query': query})
