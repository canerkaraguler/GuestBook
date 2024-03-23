from django.urls import path
from .views import create_entry,get_entries,get_users_data

urlpatterns = [
    path('create-entry/', create_entry, name='create_entry'),
    path('get-entries/', get_entries, name='get_entries'),
    path('get-users-data/', get_users_data, name='get_users_data'),

]
