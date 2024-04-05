import pytest
from unittest.mock import patch, MagicMock
from main import user_interaction, get_value


@pytest.fixture
def sample_vacancy_data():
    return {
        'items': [
            {
                'name': 'Инженер-программист',
                'area': {'name': 'Москва'},
                'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
                'snippet': {'requirement': 'Python, Django, SQL'},
                'alternate_url': 'https://example.com/vacancy/1'
            },
            {
                'name': 'Аналитик данных',
                'area': {'name': 'Санкт-Петербург'},
                'salary': {'from': 120000, 'to': 180000, 'currency': 'USD'},
                'snippet': {'requirement': 'Python, Machine Learning'},
                'alternate_url': 'https://example.com/vacancy/2'
            }
        ]
    }


def test_get_value():
    dictionary = {'a': {'b': {'c': 1}}}
    assert get_value(dictionary, 'a', 'b', 'c') == 1

    dictionary = {'a': {'b': {'c': 1}}}
    assert get_value(dictionary, 'a', 'b') == {'c': 1}

    dictionary = {'a': {'b': {'c': 1}}}
    assert get_value(dictionary, 'a', 'x') is None


@pytest.fixture
def JsonMagicMock():
    return MagicMock()


@pytest.fixture
def HHMagicMock():
    return MagicMock()


def test_user_interaction(JsonMagicMock, HHMagicMock, sample_vacancy_data):
    with patch('main.SaveJson', JsonMagicMock), \
         patch('main.HeadHunterRuAPI', HHMagicMock):
        with patch('builtins.input', side_effect=['Инженер-программист', 'Python']):
            user_interaction()


def test_user_interaction_no_vacancies(JsonMagicMock, HHMagicMock):
    with patch('main.SaveJson', JsonMagicMock) as mock_save_instance, \
         patch('main.HeadHunterRuAPI', HHMagicMock) as mock_api_instance:
        with patch('builtins.input', side_effect=['Несуществующая профессия', '']):
            user_interaction()
        assert mock_api_instance.return_value.getting_vacancies.call_count == 1
        assert mock_save_instance.return_value.add_vacancy.call_count == 0
        assert mock_save_instance.return_value.save.call_count == 0
        assert JsonMagicMock.call_count == 0


def test_user_interaction_less_vacancies(JsonMagicMock, HHMagicMock, sample_vacancy_data):
    with patch('main.SaveJson', JsonMagicMock) as mock_save_instance, \
         patch('main.HeadHunterRuAPI', HHMagicMock) as mock_api_instance:
        mock_api_instance.return_value.getting_vacancies.return_value = sample_vacancy_data
        with patch('builtins.input', side_effect=['Инженер-программист', '']):
            user_interaction()
        assert mock_api_instance.return_value.getting_vacancies.call_count == 1
        assert mock_save_instance.return_value.add_vacancy.call_count == 1
        assert mock_save_instance.return_value.save.call_count == 1
        assert JsonMagicMock.call_count == 1


def test_user_interaction_error(JsonMagicMock, HHMagicMock, sample_vacancy_data):
    with patch('main.SaveJson', JsonMagicMock) as mock_save_instance, \
         patch('main.HeadHunterRuAPI', HHMagicMock) as mock_api_instance:
        mock_api_instance.return_value.getting_vacancies.return_value = sample_vacancy_data
        mock_save_instance.return_value.add_vacancy.side_effect = Exception('Test error')
        with patch('builtins.input', side_effect=['Software Engineer', '']):
            try:
                user_interaction()
            except Exception as e:
                assert str(e) == 'Test error'

