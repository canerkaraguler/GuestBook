""" 
[NOTE]: Function based views is preferred instead of 
class based views for the simplicty.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User,Entry
from .serializers import EntrySerializer
from rest_framework.pagination import PageNumberPagination
import pdb



@api_view(['POST'])
def create_entry(request):
    """
        Description:
        -This function creates a new entry wrt incoming form submit.

        Parameters:
        - request: HTTP POST request.

        Returns:
        - HTTP response with status code

        Example Usage:
            POST /api/create-entry/
            {
                "name": "Caner Karagüler",
                "subject": "Demo",
                "message": "Demo Message"
            }
    """
    if request.method == 'POST':
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            user_name = request.data.get('name')
            user, _ = User.objects.get_or_create(name=user_name)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET'])
def get_entries(request):
    """
    Description:
    -Returns paginated sorted entries from the database.
    
    Parameters:
    - request: HTTP GET request.
    
    Returns:
    - HTTP response containing paginated entries along with pagination metadata.
    
    Example Usage:
        GET /api/get-entries/
    
    """
    entries = Entry.objects.order_by('-created_date')
    
    paginator = PageNumberPagination()
    paginator.page_size = 3
    paginated_entries = paginator.paginate_queryset(entries, request)
    
    modified_entry_data = []
    for item in paginated_entries:
        username = item.user.name
        modified_entry_data.append({
            "user":username,
            "subject":item.subject,
            "message":item.message
        })
    response_data = {
        'count': paginator.page.paginator.count,
        'page_size': paginator.page_size,
        'total_pages': paginator.page.paginator.num_pages,
        'current_page_number': paginator.page.number,
        'links':{
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link()
        },
        'entries': modified_entry_data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_users_data(request):
    """
    Description:
    -Retrieves data for each user with their last entry.
    
    Parameters:
    - request: HTTP GET request.
    
    Returns:
    - HTTP response containing data for each user including the total count of messages and details of their last entry.
    
    Example Usage:
        GET /api/get-users-data/
    """
    users = User.objects.all()
    users_data = []
    
    for user in users:
        total_messages = Entry.objects.filter(user=user).count()     
        last_entry = Entry.objects.filter(user=user).order_by('-created_date').first()
        if last_entry:
            last_entry_details = f"{last_entry.subject} | {last_entry.message}"
        else:
            last_entry_details = "No entries"
        user_data = {
            'username': user.name,
            'total_messages': total_messages,
            'last_entry': last_entry_details
        }
        
        users_data.append(user_data)

    response_data = {
        "users":users_data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


