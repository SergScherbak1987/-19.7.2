from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Тест для запроса ключа API по почте и паролю"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter_=''):
    """Тест получения списка всех питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter_)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='der', animal_type='cat',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Тест добавления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['name'] == name

def test_delete_first_pet_with_valid_key():
    """Тест удаления первого питомца пользователя"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Loom", "cat", "10", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_get_api_key_for_not_valid_email(email=not_valid_email, password=valid_password):
    """Тест запроса ключа API с неправильным логином"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result

def test_get_api_key_for_not_valid_password(email=valid_email, password=not_valid_password):
    """Тест запроса ключа API с неправильным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result

def test_get_all_pets_with_not_valid_key(filter_=''):
    """Тест запроса списка питомцев с неправильным ключем API"""
    auth_key = {'key': '1'}
    status, result = pf.get_list_of_pets(auth_key, filter_)
    assert status == 403
    assert 'Forbidden' in result

def test_add_new_pet_with_not_valid_key(name='der', animal_type='cat',
                                     age='4', pet_photo='images/cat1.jpg'):

    """Тест запроса простого добавления питоца с неправильным ключем API"""
    auth_key = {'key': '1'}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403
    assert 'Forbidden' in result

def test_add_new_pet_with_negative_age(name='der', animal_type='cat',
                                     age='-4', pet_photo='images/cat1.jpg'):
    """Тест добавления питомца с отрицательным возрастом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,  pet_photo)
    assert status == 200
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['name'] == name

def test_add_new_pet_with_long_name(name='многобукв'+'o'*10000+'т', animal_type='cat',
                                     age='-4', pet_photo='images/cat1.jpg'):
    """Тест добавления питомца с очень длинным именем"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,  pet_photo)
    assert status == 200
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['name'] == name

def test_set_photo_to_pet_wrong_format(name='der', animal_type='cat',
                                     age='-4', pet_photo='images/foto.txt'):
    """Тест добавления фото питомца не в формте изображения"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Loom', 'dog', 10, pet_photo='images/foto.txt')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,  pet_photo)
    assert status == 200

def test_post_new_pet_with_no_photo(name='www', animal_type='cot', age=2):
    """Тест добавления питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    assert status == 400

def test_create_pet_simple_with_no_name(animal_type='cot', age=10):
    """Тест простого добавления питомца без имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple_no_name(auth_key, animal_type, age)
    assert status == 400

def test_update_first_pet_with_wrong_pet_id(name='www', age=2):
    """Тест изменения данных питомца по неправильному ID"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Loom', 'dog', 10, 'images/cat1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = '1'
    status, result = pf.update_pet_info_wrong_id(auth_key, pet_id, name, age)
    assert status == 400
