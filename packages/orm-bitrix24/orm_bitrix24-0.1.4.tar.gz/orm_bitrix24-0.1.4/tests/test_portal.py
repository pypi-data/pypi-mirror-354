

import os
import time
import pytest
import asyncio
from dotenv import load_dotenv
from fast_bitrix24 import Bitrix
from pprint import pprint
# Импортируем базовый класс _Deal
from orm_bitrix24.entity import Portal

load_dotenv()


# Фикстура для инициализации клиента Bitrix24
@pytest.fixture(scope="session")
def bitrix_client():
    webhook = os.environ.get("WEBHOOK")
    if not webhook:
        pytest.skip("Необходимо установить переменную окружения WEBHOOK")
    
    bitrix = Bitrix(webhook)
    
    return bitrix

@pytest.fixture(scope="session")
def portal(bitrix_client):
    return Portal(bitrix_client)

@pytest.mark.asyncio
async def test_portal_deal_fields(portal):
    """Тест получения полей сделки"""
    
    # Получаем поля сделки
    fields = await portal.deal.fields.get_all()
    # print(f'fields: {fields}')
    title_field=fields[1]
    
    assert title_field.title == "Название"
    assert title_field.name == "TITLE"
    assert title_field.type == "string"
    assert title_field.is_required is False
    
@pytest.mark.asyncio
async def test_portal_contact_fields(portal):
    """Тест получения полей контакта"""
    fields = await portal.contact.fields.get_all()
    # print(f'fields: {fields}')
    title_field=fields[1]
    assert title_field.title == "Обращение"
    assert title_field.name == "HONORIFIC"
    assert title_field.type == "crm_status"
    assert title_field.is_required is False

@pytest.mark.asyncio
async def test_portal_company_fields(portal):
    """Тест получения полей компании"""
    fields = await portal.company.fields.get_all()
    # print(f'fields: {fields}')
    title_field=fields[1]
    assert title_field.title == "Название компании"
    assert title_field.name == "TITLE"
    assert title_field.type == "string"
    assert title_field.is_required is True


@pytest.mark.asyncio
async def test_portal_create_deal_field(portal):
    """Тест создания поля сделки"""
    field = await portal.deal.fields.create(
        field_name="TEST_FIELD",
        field_title="Тестовое поле",
        field_type="string",
        is_required=False
    )
    assert field.name == "UF_CRM_TEST_FIELD"
    assert field.title == "Тестовое поле"
    assert field.type == "string"
    assert field.is_required is False

@pytest.mark.asyncio
async def test_portal_create_contact_field(portal):
    """Тест создания поля контакта"""
    field = await portal.contact.fields.create(
        field_name="TEST_FIELD",
        field_title="Тестовое поле",
        field_type="string",
        is_required=False
    )
    assert field.name == "UF_CRM_TEST_FIELD"
    assert field.title == "Тестовое поле"
    assert field.type == "string"
    assert field.is_required is False

@pytest.mark.asyncio
async def test_portal_get_deal_field(portal):
    """Тест получения поля сделки"""
    field = await portal.deal.fields.get_by_name("UF_CRM_TEST_FIELD")
    assert field.name == "UF_CRM_TEST_FIELD"
    assert field.title == "Тестовое поле"
    assert field.type == "string"   
    assert field.is_required is False

@pytest.mark.asyncio
async def test_portal_delete_deal_field(portal):
    """Тест удаления поля сделки"""
    field = await portal.deal.fields.delete("UF_CRM_TEST_FIELD")
    fields = await portal.deal.fields.get_all()
    for field in fields:
        if field.name == "UF_CRM_TEST_FIELD":
            assert False
    assert True


@pytest.mark.asyncio
async def test_portal_create_contact_field(portal):
    """Тест создания поля контакта"""
    field = await portal.contact.fields.create(
        field_name="CONTACT_TEST_FIELD",
        field_title="Тестовое поле",
        field_type="string",
        is_required=False
    )
    assert field.name == "UF_CRM_CONTACT_TEST_FIELD"
    assert field.title == "Тестовое поле"
    assert field.type == "string"
    assert field.is_required is False

@pytest.mark.asyncio
async def test_portal_delete_contact_field(portal):
    """Тест удаления поля контакта"""
    field = await portal.contact.fields.delete("UF_CRM_CONTACT_TEST_FIELD")
    fields = await portal.contact.fields.get_all()
    for field in fields:
        if field.name == "UF_CRM_CONTACT_TEST_FIELD":
            assert False
    assert True
    
    