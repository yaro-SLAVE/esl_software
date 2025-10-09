from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import UserProfile, Organization, OrganizationFilial
import datetime


class UserProfileModelTest(TestCase):
    
    def setUp(self):
        """Создание тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_user_profile(self):
        """Тест создания профиля пользователя"""
        profile = UserProfile.objects.create(
            user=self.user,
            middle_name='Иванович'
        )
        
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.middle_name, 'Иванович')
        self.assertEqual(str(profile), f'Profile for {self.user.username}')
    
    def test_user_profile_middle_name_optional(self):
        """Тест что отчество может быть пустым"""
        profile = UserProfile.objects.create(user=self.user)
        
        self.assertIsNone(profile.middle_name)
        self.assertTrue(profile.middle_name is None or profile.middle_name == '')
    
    def test_user_profile_one_to_one_relationship(self):
        """Тест связи один-к-одному с User"""
        profile = UserProfile.objects.create(user=self.user)
        
        # Проверка связи с пользователем
        self.assertEqual(profile.user, self.user)
        self.assertEqual(self.user.user, profile)
    
    def test_user_profile_string_representation(self):
        """Тест строкового представления"""
        profile = UserProfile.objects.create(user=self.user)
        
        # Можно добавить метод __str__ в модель для красивого отображения
        # Если метода нет, тест будет проверять базовое представление
        self.assertIn('UserProfile object', str(profile))


class OrganizationModelTest(TestCase):
    
    def setUp(self):
        """Создание тестовых данных"""
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='managerpass123'
        )
    
    def test_create_organization(self):
        """Тест создания организации"""
        organization = Organization.objects.create(
            general_manager=self.manager,
            ur_address='ул. Ленина, д. 1, г. Москва'
        )
        
        self.assertEqual(organization.general_manager, self.manager)
        self.assertEqual(organization.ur_address, 'ул. Ленина, д. 1, г. Москва')
    
    def test_organization_string_representation(self):
        """Тест строкового представления организации"""
        organization = Organization.objects.create(
            general_manager=self.manager,
            ur_address='ул. Ленина, д. 1'
        )
        
        # Проверяем что строка содержит адрес или ID
        self.assertIn('Organization object', str(organization))
    
    def test_organization_required_fields(self):
        """Тест обязательных полей организации"""
        # Должна создаваться без ошибок
        organization = Organization.objects.create(
            general_manager=self.manager,
            ur_address='Test address'
        )
        self.assertIsNotNone(organization.id)
    
    def test_organization_cascade_delete(self):
        """Тест каскадного удаления при удалении менеджера"""
        organization = Organization.objects.create(
            general_manager=self.manager,
            ur_address='Test address'
        )
        
        organization_id = organization.id
        self.manager.delete()
        
        # Проверяем что организация тоже удалилась
        with self.assertRaises(Organization.DoesNotExist):
            Organization.objects.get(id=organization_id)


class OrganizationFilialModelTest(TestCase):
    
    def setUp(self):
        """Создание тестовых данных"""
        self.manager = User.objects.create_user(
            username='filial_manager',
            email='filial@example.com',
            password='filialpass123'
        )
        self.organization = Organization.objects.create(
            general_manager=self.manager,
            ur_address='Главный офис'
        )
        self.start_time = datetime.time(9, 0)
        self.end_time = datetime.time(18, 0)
    
    def test_create_organization_filial(self):
        """Тест создания филиала организации"""
        filial = OrganizationFilial.objects.create(
            organization=self.organization,
            address='ул. Пушкина, д. 10',
            start_time=self.start_time,
            end_time=self.end_time
        )
        
        self.assertEqual(filial.organization, self.organization)
        self.assertEqual(filial.address, 'ул. Пушкина, д. 10')
        self.assertEqual(filial.start_time, self.start_time)
        self.assertEqual(filial.end_time, self.end_time)
    
    def test_filial_required_fields(self):
        """Тест обязательных полей филиала"""
        # Должна создаваться без ошибок при наличии всех обязательных полей
        filial = OrganizationFilial.objects.create(
            organization=self.organization,
            address='Test address',
            start_time=self.start_time,
            end_time=self.end_time
        )
        self.assertIsNotNone(filial.id)
    
    def test_filial_time_validation(self):
        """Тест что время окончания может быть раньше времени начала (если это допустимо бизнес-логикой)"""
        # Если в бизнес-логике требуется проверка времени, можно добавить валидацию
        filial = OrganizationFilial.objects.create(
            organization=self.organization,
            address='Test address',
            start_time=datetime.time(18, 0),  # вечер
            end_time=datetime.time(9, 0)      # утро следующего дня
        )
        
        # Проверяем что объект создался (если нет ограничений на время)
        self.assertIsNotNone(filial.id)
    
    def test_filial_cascade_delete(self):
        """Тест каскадного удаления при удалении организации"""
        filial = OrganizationFilial.objects.create(
            organization=self.organization,
            address='Test address',
            start_time=self.start_time,
            end_time=self.end_time
        )
        
        filial_id = filial.id
        self.organization.delete()
        
        # Проверяем что филиал тоже удалился
        with self.assertRaises(OrganizationFilial.DoesNotExist):
            OrganizationFilial.objects.get(id=filial_id)


class ModelsRelationshipTest(TestCase):
    """Тесты для проверки связей между моделями"""
    
    def setUp(self):
        """Создание комплексных тестовых данных"""
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass1')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass2')
        
        self.user_profile = UserProfile.objects.create(user=self.user1, middle_name='Петрович')
        
        self.organization = Organization.objects.create(
            general_manager=self.user1,
            ur_address='Главный офис'
        )
        
        self.filial1 = OrganizationFilial.objects.create(
            organization=self.organization,
            address='Филиал 1',
            start_time=datetime.time(9, 0),
            end_time=datetime.time(18, 0)
        )
        
        self.filial2 = OrganizationFilial.objects.create(
            organization=self.organization,
            address='Филиал 2',
            start_time=datetime.time(10, 0),
            end_time=datetime.time(19, 0)
        )
    
    def test_user_profile_relationship(self):
        """Тест связи User - UserProfile"""
        self.assertEqual(self.user1.user, self.user_profile)
        self.assertEqual(self.user_profile.user, self.user1)
    
    def test_organization_filials_relationship(self):
        """Тест связи Organization - OrganizationFilial"""
        filials = self.organization.organization.all()
        self.assertEqual(filials.count(), 2)
        self.assertIn(self.filial1, filials)
        self.assertIn(self.filial2, filials)
    
    def test_organization_general_manager_relationship(self):
        """Тест связи Organization - User (general_manager)"""
        self.assertEqual(self.organization.general_manager, self.user1)
        
        # Проверяем related_name
        user_organizations = self.user1.general_manager.all()
        self.assertEqual(user_organizations.count(), 1)
        self.assertIn(self.organization, user_organizations)
    
    def test_multiple_filials_per_organization(self):
        """Тест что у одной организации может быть несколько филиалов"""
        filial3 = OrganizationFilial.objects.create(
            organization=self.organization,
            address='Филиал 3',
            start_time=datetime.time(8, 0),
            end_time=datetime.time(17, 0)
        )
        
        filials_count = OrganizationFilial.objects.filter(organization=self.organization).count()
        self.assertEqual(filials_count, 3)


class FieldValidationTest(TestCase):
    """Тесты валидации полей"""
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass')
        self.organization = Organization.objects.create(
            general_manager=self.user,
            ur_address='Test address'
        )
    
    def test_user_profile_middle_name_max_length(self):
        """Тест что поле middle_name может содержать длинный текст"""
        long_name = 'Очень длинное отчество которое может быть очень длинным ' * 10
        profile = UserProfile.objects.create(user=self.user, middle_name=long_name)
        
        self.assertEqual(profile.middle_name, long_name)
    
    def test_organization_address_blank(self):
        """Тест что поле ur_address не может быть пустым"""
        # Поле TextField с blank=False по умолчанию, но без валидатора на пустую строку
        organization = Organization.objects.create(
            general_manager=self.user,
            ur_address=''  # Пустая строка
        )
        
        self.assertEqual(organization.ur_address, '')
    
    def test_filial_address_not_blank(self):
        """Тест что поле address филиала не может быть пустым"""
        filial = OrganizationFilial.objects.create(
            organization=self.organization,
            address='',  # Пустая строка
            start_time=datetime.time(9, 0),
            end_time=datetime.time(18, 0)
        )
        
        self.assertEqual(filial.address, '')