from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from PracticePetstragram.accounts.models import Profile
from PracticePetstragram.web.models import Pet, PetPhoto

UserModel = get_user_model()

class ProfileDetailsViewTest(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '12345',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'picture': 'http://testuser/url.png',
        'date_of_birth': date(2002, 5, 14),
    }

    VALID_PET_INPUTS = {
        'name': "Test pet",
        'type': Pet.CAT,
    }

    VALID_PET_PHOTO_INPUTS = {
        'photo': 'somephoto.jpg',
        'publication_date': date.today(),
    }

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_pet_and_pet_photo(self, user):
        pet = Pet.objects.create(
            **self.VALID_PET_INPUTS,
            user=user,
        )

        pet_photo = PetPhoto.objects.create(
            **self.VALID_PET_PHOTO_INPUTS,
            user=user,
        )

        pet_photo.tagged_pets.add(pet)
        pet_photo.save()
        return (pet, pet_photo)

    def test_when_profile_does_not_exist_expect_404(self):
        response = self.client.get(reverse('profile details', kwargs={
            'pk': 1,
        }))
        self.assertEqual(404, response.status_code)

    def test_expect_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))
        self.assertTemplateUsed('profile_details.html')

    def test_if_owner_is_owner_expect_is_owner_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS) # How to login for a test

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertTrue(response.context['is_owner'])

    def test_if_owner_is_not_owner_expect_is_owner_false(self):
        _, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'Fakeuser',
            'password': 'fakepassword',
        }

        user = self.__create_user(**credentials)

        self.client.login(**credentials) # How to login for a test

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

        self.assertFalse(response.context['is_owner'])

    def test_if_photo_has_no_likes_expect_total_likes_count_0(self):
        user, profile = self.__create_valid_user_and_profile()

        self.__create_pet_and_pet_photo(user)

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))

        self.assertEqual(0, response.context['total_likes_count'])

    def test_if_photo_has_likes_expect_correct_likes_count(self):
        likes = 5
        user, profile = self.__create_valid_user_and_profile()

        _, pet_photo = self.__create_pet_and_pet_photo(user)

        pet_photo.likes = likes
        pet_photo.save()

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))

        self.assertEqual(5, response.context['total_likes_count'])

    def test_user_has_photos_expect_correct_photos_count(self):
        user, profile = self.__create_valid_user_and_profile()

        pet = Pet.objects.create(
            **self.VALID_PET_INPUTS,
            user=user,
        )

        pet_photo = PetPhoto.objects.create(
            **self.VALID_PET_PHOTO_INPUTS,
            user=user,
        )

        pet_photo.tagged_pets.add(pet)
        pet_photo.save()

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))

        self.assertEqual(1, response.context['total_pet_photos_count'])

    def test_when_no_photos_expect_photos_count_zero(self):
        user, profile = self.__create_valid_user_and_profile()

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))
        self.assertEqual(0, response.context['total_pet_photos_count'])



    def test_when_user_has_pets_expect_return_only_users_pets(self):
        user, profile = self.__create_valid_user_and_profile()
        credentials = {
            'username': 'Test1',
            'password': 'pass1',
        }
        (pet, _) = self.__create_pet_and_pet_photo(user)

        user2 = self.__create_user(**credentials)

        self.__create_pet_and_pet_photo(user2)

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))
        self.assertListEqual(
            [pet],
            response.context['pets'],
        )

    def test_when_user_has_no_pets_expect_pets_to_be_empty(self):
        _, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))
        self.assertListEqual([], response.context['pets'])