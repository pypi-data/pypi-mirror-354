import os
import time
import pytest
import asyncio
from dotenv import load_dotenv
from fast_bitrix24 import Bitrix
from pprint import pprint
# Импортируем базовый класс _Deal
from orm_bitrix24.entity import _Deal, CustomField, TextCustomField

# Расширяем класс для тестирования
class Deal(_Deal):
    new_string_user = TextCustomField("UF_CRM_1748463696180")
    # delivery_address = TextCustomField("UF_CRM_DELIVERY_ADDRESS")
    # test_field = TextCustomField("UF_CRM_TEST_FIELD")
    # pass

# Загружаем переменные окружения
load_dotenv()

# Фикстура для инициализации клиента Bitrix24
@pytest.fixture(scope="session")
def bitrix_client():
    webhook = os.environ.get("WEBHOOK")
    if not webhook:
        pytest.skip("Необходимо установить переменную окружения WEBHOOK")
    
    bitrix = Bitrix(webhook)
    
    return bitrix

# Фикстура для создания тестовой сделки
@pytest.fixture(scope="session")
def test_deal(bitrix_client):
    # Создаем тестовую сделку
    Deal.get_manager(bitrix_client)
    deal = asyncio.run(Deal.objects.create(
        title="Тестовая сделка для pytest",
        opportunity=5000,
        currency_id="RUB",
        stage_id="NEW",
        test_field="Тестовое значение"

    ))
    print(f"Создана новая сделка: {deal.title} (ID: {deal.id})")
    # print(deal)
    # 1/0
    # yield deal
    return  deal
    
    # Удаляем тестовую сделку после завершения теста
    # try:
    #     await DealTest.objects.delete(deal.id)
    # except Exception as e:
    #     print(f"Ошибка при удалении тестовой сделки: {e}")


@pytest.mark.asyncio
async def test_deal_get(test_deal):
    """Тест получения сделки по ID"""
    # Получаем сделку по ID
    pprint(test_deal)
    deal_id = test_deal.id
    # pytest.skip("Необходимо установить переменную окружения WEBHOOK")
    # retrieved_deal = asyncio.run(DealTest.objects.get_by_id(deal_id))
    retrieved_deal = await Deal.objects.get_by_id(deal_id)
    
    # Проверяем полученную сделку
    assert retrieved_deal is not None
    assert retrieved_deal.id == deal_id
    assert retrieved_deal.title == test_deal.title
    assert retrieved_deal.opportunity == test_deal.opportunity


@pytest.mark.asyncio
async def test_deal_update(test_deal):
    """Тест обновления сделки"""
    # Изменяем поля сделки
    new_title = "Обновленная тестовая сделка"
    new_opportunity = 7500
    new_address = "ул. Новая, д. 42"
    
    test_deal.title = new_title
    test_deal.opportunity = new_opportunity
    # test_deal.delivery_address = new_address
    print(f'test_deal: {test_deal}')
    # 1/0
    # Сохраняем изменения
    await test_deal.save()
    # asyncio.run(test_deal.save())
    # 1/0
    # Получаем обновленную сделку из API
    # updated_deal = asyncio.run(DealTest.objects.get_by_id(test_deal.id))
    updated_deal = await Deal.objects.get_by_id(test_deal.id)
    
    # Проверяем обновленные поля
    assert updated_deal.title == new_title
    assert updated_deal.opportunity == new_opportunity
    
    # assert updated_deal.delivery_address == new_address



@pytest.mark.asyncio
async def test_deal_create_activity(test_deal):
    """Тест создания активности"""
    # Создаем активность
    email_activity = await test_deal.activity.mail(
                subject="Коммерческое предложение из ORM просто ответьте",
                message="Добрый день! Высылаем коммерческое предложение через новую ORM-систему.",
                contact_id=1,
                from_email="darkclaw921@yandex.ru"             
            )
    print(f'email_activity: {email_activity}')
    assert email_activity.subject == "Коммерческое предложение из ORM просто ответьте"


@pytest.mark.asyncio
async def test_deal_get_activity(test_deal):
    """Тест получения активности"""
    # Получаем активность
    activities = await test_deal.activity.get_all()
    print(f'activities: {activities}')
    assert activities[0].subject == "Коммерческое предложение из ORM просто ответьте"

# @pytest.mark.asyncio
# async def test_deal_activity(test_deal):
#     """Тест работы с активностями"""
#     # Получаем активнсоти сделки
#     activities = await test_deal.activity.get_all()
#     print(f'activities: {activities}')

# @pytest.mark.asyncio
# async def test_deal_timeline(test_deal):
#     """Тест работы с таймлайном"""
#     # Получаем таймлайн сделки
#     timeline = await test_deal.timeline.comments.get_all()
#     print(f'timeline: {timeline}')

@pytest.mark.asyncio
async def test_deal_create_timeline_comment(bitrix_client, test_deal):
    """Тест создания комментария в таймлайне"""
    # Создаем комментарий в таймлайне
    Deal.get_manager(bitrix_client)
    retrieved_deal = await Deal.objects.get_by_id(test_deal.id)

    comment = await retrieved_deal.timeline.comments.create(comment="Тестовый комментарий")
    print(f'comment: {comment.comment}')
    assert comment.comment == "Тестовый комментарий"
    # pytest.skip("Необходимо установить переменную окружения WEBHOOK") 

@pytest.mark.asyncio
async def test_deal_get_timeline_comment(test_deal):
    """Тест получения комментария в таймлайне"""
    # Получаем комментарий в таймлайне
    comments = await test_deal.timeline.comments.get_all()
    print(f'comments: {comments}')
    assert comments[0].comment == "Тестовый комментарий"




@pytest.mark.asyncio
async def test_deal_filter(test_deal):
    """Тест фильтрации сделок"""
    # Фильтруем сделки по заголовку
    # deals = asyncio.run(DealTest.objects.filter(title=test_deal.title))
    deals = await Deal.objects.filter(title=test_deal.title)
    
    # Проверяем результаты фильтрации
    assert len(deals) > 0
    assert any(deal.id == test_deal.id for deal in deals)


@pytest.mark.asyncio
async def test_deal_delete(test_deal):
    """Тест удаления сделки"""
    # Создаем сделку для удаления
    deal = await Deal.objects.create(
        title="Сделка для удаления",
        opportunity=100,
        currency_id="RUB",
        stage_id="NEW"
    )
    
    deal_id = deal.id
    time.sleep(1)
    # Удаляем сделку
    # result = asyncio.run(DealTest.objects.delete(deal_id))
    result = await deal.delete()
    
    # Проверяем результат удаления
    assert result is True
    
    # Пробуем получить удаленную сделку
    try:
        # deleted_deal = asyncio.run(DealTest.objects.get_by_id(deal_id))
        deleted_deal = await Deal.objects.get_by_id(deal_id)
        assert deleted_deal is None, "Сделка должна быть удалена"
    except Exception:
        # Ожидаем ошибку при попытке получить удаленную сделку
        pass


@pytest.mark.asyncio
async def test_custom_fields(test_deal):
    """Тест работы с пользовательскими полями"""
    # Устанавливаем значения пользовательских полей 
    test_deal.new_string_user = "test_source"
    # test_deal.test_field = "Тестовое значение поля"
    
    # Сохраняем изменения
    await test_deal.save()
    
    # Получаем обновленную сделку
    updated_deal = await Deal.objects.get_by_id(test_deal.id)
    
    # Проверяем значения пользовательских полей
    assert updated_deal.new_string_user == "test_source"
    # assert updated_deal.test_field == "Тестовое значение поля" 