from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Entry


class CreateEntryAPITestCase(APITestCase):
    def setUp(self):
        self.user_name = "Test User"
        self.user = User.objects.create(name=self.user_name)
        self.entry_data_new_user = {
            "name": "Test User 2",
            "subject": "Test Subject 2",
            "message": "Test Message 2"
        }
        self.entry_data_existing_user = {
            "name": "Test User",
            "subject": "Test Subject 3",
            "message": "Test Message 3"
        }

    def test_create_entry_new_user(self):
        
        url = reverse('api:create_entry')
        response = self.client.post(url, self.entry_data_new_user, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entry.objects.count(), 1)  

        expected_user = User.objects.filter(name=self.entry_data_new_user['name']).first()
        self.assertIsNotNone(expected_user)
    
    def test_create_entry_existing_user(self):
        initial_user_count = User.objects.count()
        url = reverse('api:create_entry')
        response = self.client.post(url, self.entry_data_existing_user, format='json')     
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entry.objects.count(), 1)  
        new_user_count = User.objects.count()
        self.assertEqual(initial_user_count,new_user_count )  


class GetEntriesAPITestCase(APITestCase):
    def setUp(self):
        for i in range(10):  
            Entry.objects.create(user=User.objects.create(name=f"Demo User{i}"), subject=f"Demo {i}", message="Demo Message")

    def test_get_entries(self):

        url = reverse('api:get_entries')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_keys = ['count', 'page_size', 'total_pages', 'current_page_number', 'links', 'entries']
        self.assertEqual(set(response.data.keys()), set(expected_keys))

        self.assertEqual(response.data['count'], 10) 
        self.assertEqual(response.data['page_size'], 3)  
        self.assertEqual(response.data['total_pages'], 4)  
        self.assertEqual(response.data['current_page_number'], 1)  

        self.assertIsInstance(response.data['entries'], list)
        self.assertEqual(len(response.data['entries']), 3)  

        self.assertIn('next', response.data['links'])
        self.assertIsNotNone(response.data['links']['next'])

        self.assertIn('previous', response.data['links'])
        self.assertIsNone(response.data['links']['previous'])

        self.assertEqual(response.data['entries'][0]['subject'], "Demo 9")
        self.assertEqual(response.data['entries'][1]['subject'], "Demo 8")
        self.assertEqual(response.data['entries'][2]['subject'], "Demo 7")

        
        next_page_url = response.data['links']['next']
        response = self.client.get(next_page_url)

       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data.keys()), set(expected_keys))

        self.assertEqual(response.data['count'], 10)  
        self.assertEqual(response.data['page_size'], 3)  
        self.assertEqual(response.data['total_pages'], 4)  
        self.assertEqual(response.data['current_page_number'], 2)  
       
        self.assertIsInstance(response.data['entries'], list)
        self.assertEqual(len(response.data['entries']), 3) 

        self.assertEqual(response.data['entries'][0]['subject'], "Demo 6")
        self.assertEqual(response.data['entries'][1]['subject'], "Demo 5")
        self.assertEqual(response.data['entries'][2]['subject'], "Demo 4")



class GetUsersDataAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(name='User1')
        self.user2 = User.objects.create(name='User2')

        Entry.objects.create(user=self.user1, subject='Subject 1', message='Message 1')
        Entry.objects.create(user=self.user1, subject='Subject 2', message='Message 2')
        Entry.objects.create(user=self.user2, subject='Subject 3', message='Message 3')

    def test_get_users_data(self):
        url = reverse('api:get_users_data')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('users', response.data)
        users_data = response.data['users']

        self.assertEqual(len(users_data), 2)

        user1_data = users_data[0]
        user2_data = users_data[1]

        self.assertEqual(user1_data['username'], 'User1')
        self.assertEqual(user1_data['total_messages'], 2)
        self.assertEqual(user1_data['last_entry'], 'Subject 2 | Message 2')

        self.assertEqual(user2_data['username'], 'User2')
        self.assertEqual(user2_data['total_messages'], 1)
        self.assertEqual(user2_data['last_entry'], 'Subject 3 | Message 3')