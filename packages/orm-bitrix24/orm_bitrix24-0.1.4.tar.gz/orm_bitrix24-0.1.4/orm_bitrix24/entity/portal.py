from pprint import pprint
import traceback
from typing import Dict, List, Any, Optional, ClassVar, Union
from loguru import logger


class EnumValue:
    """Класс для представления значения поля enumeration"""
    
    def __init__(self, data: Dict[str, Any]):
        self._data = data
    
    @property
    def id(self) -> str:
        """ID значения"""
        return self._data.get('ID', '')
    
    @property
    def value(self) -> str:
        """Значение для отображения"""
        return self._data.get('VALUE', '')
    
    def __str__(self) -> str:
        return f"{self.value} ({self.id})"
    
    def __repr__(self) -> str:
        return f"EnumValue(id='{self.id}', value='{self.value}')"


class FieldInfo:
    """Класс для представления информации о поле сущности"""
    
    def __init__(self, data: Dict[str, Any]):
        self._data = data
    
    @property
    def name(self) -> str:
        """Имя поля"""
        return self._data.get('NAME', '')
    
    @property
    def title(self) -> str:
        """Отображаемое название поля"""
        # Для пользовательских полей проверяем специальные поля названий
        if self.is_custom:
            # Приоритет: formLabel -> listLabel -> filterLabel -> title
            return (self._data.get('formLabel') or 
                   self._data.get('listLabel') or 
                   self._data.get('filterLabel') or 
                   self._data.get('title', ''))
        else:
            # Для стандартных полей используем обычное поле title
            return self._data.get('title', '')
    
    @property
    def type(self) -> str:
        """Тип поля"""
        return self._data.get('type', '')
    
    @property
    def is_required(self) -> bool:
        """Обязательное ли поле"""
        return self._data.get('isRequired', False)
    
    @property
    def is_readonly(self) -> bool:
        """Только для чтения"""
        return self._data.get('isReadOnly', False)
    
    @property
    def is_multiple(self) -> bool:
        """Множественное ли поле"""
        return self._data.get('isMultiple', False)
    
    @property
    def is_custom(self) -> bool:
        """Пользовательское ли поле"""
        return self.name.startswith('UF_')
    
    @property
    def settings(self) -> Dict[str, Any]:
        """Настройки поля"""
        return self._data.get('settings', {})
    
    @property
    def values(self) -> List[EnumValue]:
        """Значения для полей типа enumeration"""
        if self.type == 'enumeration':
            items = self._data.get('items', [])
            return [EnumValue(item) for item in items]
        return []
    
    def __str__(self) -> str:
        return f"Field: {self.name} ({self.title}) - {self.type}"
    
    def __repr__(self) -> str:
        return f"FieldInfo(name='{self.name}', type='{self.type}', title='{self.title}')"


class FieldsManager:
    """Базовый менеджер для работы с полями сущности"""
    
    def __init__(self, bitrix, entity_type: str, api_method_prefix: str):
        self._bitrix = bitrix
        self.entity_type = entity_type
        self.api_method_prefix = api_method_prefix
        logger.info(f"Инициализирован FieldsManager для {entity_type}")
    
    async def get_all(self) -> List[FieldInfo]:
        """Получение всех полей сущности (включая пользовательские)"""
        try:
            logger.info(f"Получение всех полей для {self.entity_type}")
            # Метод .fields не требует параметров, используем get_all
            result = await self._bitrix.get_all(f'{self.api_method_prefix}.fields')
            
            if not result:
                logger.warning(f"Не получены поля для {self.entity_type}")
                return []
            
            # result приходит в виде списка словарей, а не словаря словарей
            if isinstance(result, dict):
                # Если результат - словарь полей (ключ = имя поля, значение = данные поля)
                fields = []
                for field_name, field_data in result.items():
                    if isinstance(field_data, dict):
                        # Добавляем имя поля в данные, если его там нет
                        if 'NAME' not in field_data:
                            field_data['NAME'] = field_name

                        fields.append(FieldInfo(field_data))
            else:
                # Если результат - список полей
                fields = [FieldInfo(field_data) for field_data in result]
            
            
            
            logger.info(f"Получено {len(fields)} полей для {self.entity_type}")
            return fields
            
        except Exception as e:
            logger.error(f"Ошибка при получении полей {self.entity_type}: {e}")
            raise
    
    async def get_by_name(self, field_name: str) -> Optional[FieldInfo]:
        """Получение информации о конкретном поле по имени"""
        try:
            logger.info(f"Получение поля {field_name} для {self.entity_type}")
            fields = await self.get_all()
            
            for field in fields:
                if field.name == field_name:
                    logger.info(f"Найдено поле {field_name}")
                    return field
            
            logger.warning(f"Поле {field_name} не найдено для {self.entity_type}")
            return None
            
        except Exception as e:
            logger.error(f"Ошибка при получении поля {field_name} для {self.entity_type}: {e}")
            raise
    
    async def get_custom_fields(self) -> List[FieldInfo]:
        """Получение только пользовательских полей"""
        try:
            logger.info(f"Получение пользовательских полей для {self.entity_type}")
            all_fields = await self.get_all()
            custom_fields = [field for field in all_fields if field.is_custom]
            logger.info(f"Найдено {len(custom_fields)} пользовательских полей для {self.entity_type}")
            return custom_fields
            
        except Exception as e:
            logger.error(f"Ошибка при получении пользовательских полей {self.entity_type}: {e}")
            raise
    
    async def create(self, 
                    field_name: str, 
                    field_title: str, 
                    field_type: str = 'string',
                    is_required: bool = False,
                    is_multiple: bool = False,
                    settings: Optional[Dict[str, Any]] = None) -> FieldInfo:
        """
        Создание пользовательского поля
        
        Args:
            field_name: Имя поля (будет добавлен префикс UF_ если его нет)
            field_title: Отображаемое название поля
            field_type: Тип поля (string, integer, double, boolean, datetime, enumeration и др.)
            is_required: Обязательное ли поле
            is_multiple: Множественное ли поле
            settings: Дополнительные настройки поля
        """
        try:
            # Добавляем префикс UF_ если его нет
            if not field_name.startswith('UF_'):
                field_name = f'UF_CRM_{field_name.upper()}'
            
            logger.info(f"Создание пользовательского поля {field_name} для {self.entity_type}")
            
            field_data = {
                'FIELD_NAME': field_name,
                'EDIT_FORM_LABEL': field_title,
                'LIST_COLUMN_LABEL': field_title,
                'LIST_FILTER_LABEL': field_title,
                'USER_TYPE_ID': field_type,
                'MANDATORY': 'Y' if is_required else 'N',
                'MULTIPLE': 'Y' if is_multiple else 'N'
            }
            
            if settings:
                field_data['SETTINGS'] = settings
            
            result = await self._bitrix.call(
                f'{self.api_method_prefix}.userfield.add',
                {
                    'fields': {
                        'ENTITY_ID': f'CRM_{self.entity_type}',
                        **field_data
                    }
                }
            )
            pprint(result)
            if result:
                logger.info(f"Пользовательское поле {field_name} создано с ID: {result}")
                # Получаем созданное поле для возврата
                created_field = await self.get_by_name(field_name)
                if created_field:
                    return created_field
         
            # raise Exception(f"Ошибка при создании поля {field_name}")
            
        except Exception as e:
            logger.error(f"Ошибка при создании поля {field_name} для {self.entity_type}: {e}")
            raise
    
    async def delete(self, field_name: str) -> bool:
        """Удаление пользовательского поля"""
        try:
            logger.info(f"Удаление пользовательского поля {field_name} для {self.entity_type}")
            
            # Сначала получаем ID поля
            field = await self.get_by_name(field_name)
            if not field or not field.is_custom:
                logger.warning(f"Пользовательское поле {field_name} не найдено")
                return False
            
            # Получаем список всех пользовательских полей с их ID
            userfields_result = await self._bitrix.call(
                f'{self.api_method_prefix}.userfield.list',
                {
                    'filter': {
                        'ENTITY_ID': f'CRM_{self.entity_type}',
                        'FIELD_NAME': field_name
                    }
                }
            )
            
            if not userfields_result:
                logger.warning(f"Не найден ID для поля {field_name}")
                return False
            
            
            field_id = userfields_result['ID']
            
            result = await self._bitrix.call(
                f'{self.api_method_prefix}.userfield.delete',
                {'id': field_id}
            )
            
            if result:
                logger.info(f"Пользовательское поле {field_name} удалено")
                return True
            
            return False
            
        except Exception as e:
            
            logger.error(f"Ошибка при удалении поля {field_name} для {self.entity_type}: {traceback.print_exc()}")
            raise


class DealFieldsManager(FieldsManager):
    """Менеджер полей для сделок"""
    
    def __init__(self, bitrix):
        super().__init__(bitrix, 'DEAL', 'crm.deal')


class ContactFieldsManager(FieldsManager):
    """Менеджер полей для контактов"""
    
    def __init__(self, bitrix):
        super().__init__(bitrix, 'CONTACT', 'crm.contact')


class CompanyFieldsManager(FieldsManager):
    """Менеджер полей для компаний"""
    
    def __init__(self, bitrix):
        super().__init__(bitrix, 'COMPANY', 'crm.company')


class LeadFieldsManager(FieldsManager):
    """Менеджер полей для лидов"""
    
    def __init__(self, bitrix):
        super().__init__(bitrix, 'LEAD', 'crm.lead')


class EntityFieldsContainer:
    """Контейнер для менеджеров полей конкретной сущности"""
    
    def __init__(self, fields_manager: FieldsManager):
        self.fields = fields_manager


class Portal:
    """
    Главный класс для работы с порталом Bitrix24
    Предоставляет доступ к управлению полями всех сущностей
    """
    
    def __init__(self, bitrix):
        self._bitrix = bitrix
        logger.info("Инициализация Portal для работы с полями сущностей")
        
        # Инициализация менеджеров полей для каждой сущности
        self.deal = EntityFieldsContainer(DealFieldsManager(bitrix))
        self.contact = EntityFieldsContainer(ContactFieldsManager(bitrix))
        self.company = EntityFieldsContainer(CompanyFieldsManager(bitrix))
        self.lead = EntityFieldsContainer(LeadFieldsManager(bitrix))
    
    async def get_all_entities_fields(self) -> Dict[str, List[FieldInfo]]:
        """Получение полей всех сущностей"""
        try:
            logger.info("Получение полей всех сущностей")
            result = {}
            
            result['deal'] = await self.deal.fields.get_all()
            result['contact'] = await self.contact.fields.get_all()
            result['company'] = await self.company.fields.get_all()
            result['lead'] = await self.lead.fields.get_all()
            
            total_fields = sum(len(fields) for fields in result.values())
            logger.info(f"Получено {total_fields} полей для всех сущностей")
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при получении полей всех сущностей: {e}")
            raise
    
    def __str__(self) -> str:
        return "Portal: Менеджер полей для сущностей Bitrix24"
