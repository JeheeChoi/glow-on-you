from django.urls import path
from .views.mango_views import Mangos, MangoDetail
from .views.board_views import Boards, BoardDetail
from .views.glow_views import Glows, GlowDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('mangos/', Mangos.as_view(), name='mangos'),
    path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    # Board
    path('boards/', Boards.as_view(), name='boards'),
    # Board with glowIndex
    path('boards/<int:pk>/', BoardDetail.as_view(), name='board_detail'),
    # Glow - create
    path('boards/<int:board_id>/glows/', Glows.as_view(), name='glows'),
    # Glow - show/delete/update
    path('glows/<int:pk>/', GlowDetail.as_view(), name='glow_detail'),

    # path('boards/<int:pk>/glows/<int:pk>/', GlowDetail.as_view(), name='glows')
    # path('glows/<int:pk>/', GlowDetail.as_view(), name='glow_detail'),
]
