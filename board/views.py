from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Board, BoardParticipant, Stroke
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboards(request):
    my_boards = Board.objects.filter(owner=request.user)
    participating = Board.objects.filter(participants__user=request.user)

    boards = (my_boards | participating).distinct()
    return render(request, 'dashboard.html', {'boards': boards})


@login_required
def create_board(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        new_board = Board.objects.create(
            title=title,
            owner=request.user,
        )
        BoardParticipant.objects.create(
            board=new_board,
            user=request.user,
            role='admin'
        )
        return redirect('whiteboard_detail', slug=new_board.slug)
    return render(request, 'create.html')


@login_required
def whiteboard_detail(request, slug):
    board = get_object_or_404(Board, slug=slug)
    existing_strokes = Stroke.objects.filter(board=board)

    return render(request, 'whiteboard.html', {
        'board': board,
        'strokes': existing_strokes
    })

from django.shortcuts import get_object_or_404

@login_required
def board_detail(request, slug):
    board = get_object_or_404(Board, slug=slug)
    return render(request, 'board_detail.html', {'board': board})

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request,'base.html')
