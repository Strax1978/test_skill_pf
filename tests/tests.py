from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter='my_pets'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Бим', animal_type='спаниэль',
                                     age='12', pet_photo='images/dog.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Бим", "спаниэль", "12", "images/dog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Бим', animal_type='спаниэль', age=11):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# 10 тестов в рамках выполнения домашнего задания

def test_create_pet_simple_successfully(name="Газета", animal_type="птичка", age="4"):
    '''Тест 1: Метод простого добавления питомца без фото'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo_to_pet_with_valid_data(pet_photo="images/bird.jpeg"):
    '''Тест 2: Метод добавления фото к существующему питомцу с валидными данными'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Бим", "песик", "12")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo'] is not None


def test_get_api_key_for_invalid_user(email="test_email@mail.ru", password="invalid_password"):
    '''Тест 3: Получение apikey незарегистрированного пользователя'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_api_key_for_valid_user_invalid_password(email=valid_email, password="test"):
    '''Тест 4: Получение apikey зарегистрированного пользователя с неверным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_api_key_for_invalid_user_valid_password(email="invalid@mail.com", password=valid_password):
    '''Тест 5: Получение apikey не валидной электронной почты с правильным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result


def test_get_all_pets_with_invalid_key(filter=''):
     '''Тест 6: Получение списка питомцев с несуществующим apikey'''
     _, auth_key = pf.get_api_key(valid_email, valid_password)

     # замена ключа на несуществующий
     auth_key = {"key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae722"}

     status, result = pf.get_list_of_pets(auth_key, filter)
     assert status != 200


def test_get_my_pets_with_valid_key(filter='my_pets'):
    '''Тест 7: Получение списка "my_pets" зарегистрированного пользователя'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) >= 0


def test_create_pet_simple_wrong_age(name="Бим", animal_type="песик", age="много"):
    '''Тест 8: Добавление питомца (без фото) с невалидным полем ,возраст,.
    Тут баг сайт допустил запись питомца у которого возраст не число.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age


def test_post_new_pet_with_invalid_photo(name="qwee", animal_type="qqqq",
                                      age='1111', pet_photo="images/noname.ods"):
    '''Тест 9: Добавления питомца с другим файлом вместо фото.
    Опять баг. нельзя добавлять фото кроме формата JPG, JPEG, PNG.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['pet_photo'] is not None


def test_create_pet_simple_invalid_data(name="", animal_type="", age=""):
    '''Тест 10: Метод простого добавления питомца с пустыми полями.
    Баг пустых строк в создании питомцев быть не должно.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name





