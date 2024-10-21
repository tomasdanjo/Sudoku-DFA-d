from django.contrib import admin
from django.urls import path, include
from .views import sudoku_game, landing_page, success_page

urlpatterns = [
   path('',landing_page,name='landing_page'),
   path('game/<int:id>/', sudoku_game, name='sudoku_game'),
   path('success/',success_page,name='success_page')
   # path('')
]