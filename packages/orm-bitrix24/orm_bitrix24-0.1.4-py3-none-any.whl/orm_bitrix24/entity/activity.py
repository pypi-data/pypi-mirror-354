from typing import ClassVar, Optional, List, Dict, Any, Type, Union, TYPE_CHECKING
import datetime
from loguru import logger

from .base import (
    BaseEntity, StringField, IntegerField, DateTimeField, BooleanField,
    RelatedManager, EntityManager
)

if TYPE_CHECKING:
    from .deal import Deal
    from .lead import Lead


class ActivityEntityManager(EntityManager['Activity']):
    """Кастомный менеджер активностей для правильной типизации"""
    
    async def get_by_id(self, activity_id: Union[str, int]) -> Optional['Activity']:
        """Получение активности по ID"""
        result = await self._bitrix.call(
            'crm.activity.get',
            {'id': activity_id}
        )
        if result:
            return self._entity_class(self._bitrix, result)
        return None
    
    async def filter(self, **kwargs) -> List['Activity']:
        """Фильтрация активностей"""
        filter_params = {}
        
        # Преобразуем kwargs в filter для API
        for key, value in kwargs.items():
            if key == 'entity_type':
                filter_params['ENTITY_TYPE'] = value
            elif key == 'entity_id':
                filter_params['ENTITY_ID'] = value
            elif key == 'type_id':
                filter_params['TYPE_ID'] = value
            else:
                filter_params[key.upper()] = value
        
        result = await self._bitrix.get_all(
            'crm.activity.list',
            {'filter': filter_params}
        )
        
        return [self._entity_class(self._bitrix, item) for item in result]


class Activity(BaseEntity):
    """Базовый класс для работы с делами в Bitrix24 CRM"""
    
    ENTITY_NAME: ClassVar[str] = "ACTIVITY"
    ENTITY_METHOD: ClassVar[str] = "crm.activity"
    
    # Основные поля активности
    id = IntegerField("ID")
    subject = StringField("SUBJECT")
    type_id = IntegerField("TYPE_ID")  # 1-звонок, 2-встреча, 4-email
    entity_type = StringField("ENTITY_TYPE")  # DEAL, LEAD, CONTACT, COMPANY
    entity_id = IntegerField("ENTITY_ID")
    start_time = DateTimeField("START_TIME")
    end_time = DateTimeField("END_TIME")
    deadline = DateTimeField("DEADLINE")
    completed = BooleanField("COMPLETED")
    priority = IntegerField("PRIORITY")  # 1-низкий, 2-средний, 3-высокий
    responsible_id = IntegerField("RESPONSIBLE_ID")
    description = StringField("DESCRIPTION")
    direction = IntegerField("DIRECTION")  # 1-входящий, 2-исходящий
    location = StringField("LOCATION")
    created = DateTimeField("CREATED")
    updated = DateTimeField("LAST_UPDATED")
    
    # Объект для подсказок типов IDE
    objects: ClassVar[ActivityEntityManager]
    
    def __init__(self, bitrix, data: Optional[Dict[str, Any]] = None):
        super().__init__(bitrix, data)
        logger.debug(f"Создана активность: {self.subject} (ID: {self.id})")
    
    def __str__(self) -> str:
        return f"Activity: {self.subject} (ID: {self.id}, Type: {self.type_id})"
    
    @classmethod
    def get_manager(cls, bitrix) -> ActivityEntityManager:
        manager = ActivityEntityManager(bitrix, cls)
        cls.objects = manager
        return manager
    
    async def save(self) -> 'Activity':
        """Сохранение активности"""
        logger.info(f"Сохранение активности: {self.subject}")
        return await super().save()
    
    async def delete(self) -> bool:
        """Удаление активности"""
        if not self.id:
            raise ValueError("Невозможно удалить несохраненную активность")
        
        logger.info(f"Удаление активности ID: {self.id}")
        result = await self._bitrix.call(
            'crm.activity.delete',
            {'id': self.id}
        )
        
        return bool(result)
    
    async def complete(self) -> bool:
        """Отметить активность как выполненную"""
        self.completed = True
        await self.save()
        logger.info(f"Активность ID {self.id} отмечена как выполненная")
        return True


class EmailActivity(Activity):
    """Специализированный класс для email-активностей"""
    
    # Коммуникации хранятся в отдельном поле COMMUNICATIONS
    # Используем свойства для удобного доступа к данным
    
    @property
    def to_email(self) -> Optional[str]:
        """Получение email получателя из коммуникаций"""
        communications = self._data.get('COMMUNICATIONS', [])
        for comm in communications:
            if comm.get('TYPE') == 'EMAIL':
                return comm.get('VALUE')
        return None
    
    @property 
    def from_email(self) -> Optional[str]:
        """Email отправителя (пока не используется в COMMUNICATIONS)"""
        return self._data.get('COMM_FROM')  # Для обратной совместимости
    
    def __init__(self, bitrix, data: Optional[Dict[str, Any]] = None):
        super().__init__(bitrix, data)
        # Устанавливаем тип как email (4)
        if not self.type_id:
            self.type_id = 4
        
        logger.debug(f"Создана email-активность: {self.subject}")
    
    @classmethod
    async def create_for_entity(cls, bitrix, entity_type: str, entity_id: int, 
                               subject: str, message: str, to_email: Optional[str] = None,
                               contact_id: Optional[int] = None,
                               from_email: Optional[str] = None) -> 'EmailActivity':
        """
        Создание email-активности для указанной сущности
        
        Args:
            bitrix: Объект клиента Bitrix24
            entity_type: Тип сущности (DEAL, LEAD, CONTACT, COMPANY)
            entity_id: ID сущности
            subject: Тема письма
            message: Текст письма
            to_email: Email получателя (опционально, если указан contact_id)
            contact_id: ID контакта для отправки (приоритет над to_email)
            from_email: Email отправителя (опционально)
        Docs: https://apidocs.bitrix24.ru/tutorials/crm/how-to-add-crm-objects/how-to-send-email.html?tabs=defaultTabsGroup-2w119eqc_php
        """
        logger.info(f"Создание email-активности для {entity_type} ID {entity_id}")
        
        # Определяем тип владельца (OWNER_TYPE_ID)
        owner_type_mapping = {
            'DEAL': 2,      # CCrmOwnerType::Deal
            'LEAD': 1,      # CCrmOwnerType::Lead  
            'CONTACT': 3,   # CCrmOwnerType::Contact
            'COMPANY': 4    # CCrmOwnerType::Company
        }
        
        activity_data = {
            'TYPE_ID': 4,  # Email тип
            'SUBJECT': subject,
            'DESCRIPTION': message,
            'DESCRIPTION_TYPE':3,
            'DIRECTION': 2,  # Исходящий
            'COMPLETED': 'Y',
            # 'PRIORITY': 2,   # Средний приоритет
            'OWNER_ID': entity_id,
            'OWNER_TYPE_ID': owner_type_mapping.get(entity_type, 2),
            # 'OWNER_ID': 5,
            # 'OWNER_TYPE_ID': 3,
            'START_TIME': datetime.datetime.now().isoformat(),
            'END_TIME': (datetime.datetime.now() + datetime.timedelta(minutes=10)).isoformat(),
            # 'RESPONSIBLE_ID': 1,
            'SETTINGS': {'EMAIL_META': {
                '__email': from_email,
                            #  'bcc': '',
                            #  'cc': '',
                
                'from': f'<{from_email}>',
                            #  'replyTo': '',
                             
                             },
                            
                             }
            # 'SETTINGS': {'MESSAGE_FROM': 'Игорь 123 <' + from_email + '>'},
            
        }
        
        # Формируем структуру коммуникаций
        communications = []
        
        if contact_id:
            # Получаем email контакта из Bitrix24
            logger.info(f"Получение данных контакта ID: {contact_id}")
            try:
                contact_data = await bitrix.call('crm.contact.get', {'id': contact_id})
                if contact_data.get('order0000000000'):
                    contact_data = contact_data['order0000000000']
                print(contact_data)
                if contact_data and contact_data.get('EMAIL'):
                    # Берем первый email из массива
                    emails = contact_data['EMAIL']
                    if emails and len(emails) > 0:
                        email_value = emails[0]['VALUE']
                        communications.append({
                            'ENTITY_ID': contact_id,
                            'ENTITY_TYPE_ID': 3,  # Контакт
                            # 'TYPE': 'EMAIL',
                            'VALUE': email_value
                        })
                        activity_data['SETTINGS']['EMAIL_META']['to'] = email_value
                        logger.info(f"Добавлен email контакта: {email_value}")
                    else:
                        logger.warning(f"У контакта {contact_id} нет email адресов")
                        if to_email:
                            logger.info(f"Используем fallback email: {to_email}")
                            communications.append({
                                # 'TYPE': 'EMAIL',
                                'ENTITY_ID': contact_id,
                                'ENTITY_TYPE_ID': 3,  # Контакт
                                'VALUE': to_email
                            })
                else:
                    logger.warning(f"Контакт {contact_id} не найден или нет доступа")
                    if to_email:
                        logger.info(f"Используем fallback email: {to_email}")
                        communications.append({
                            # 'TYPE': 'EMAIL',
                            'ENTITY_ID': contact_id,
                            'ENTITY_TYPE_ID': 3,  # Контакт
                            'VALUE': to_email
                        })
                        
            except Exception as e:
                logger.error(f"Ошибка при получении контакта {contact_id}: {e}")
                if to_email:
                    logger.info(f"Используем fallback email: {to_email}")
                    communications.append({
                        # 'TYPE': 'EMAIL',
                        'ENTITY_ID': contact_id,
                        'ENTITY_TYPE_ID': 3,  # Контакт
                        'VALUE': to_email
                    })
        
        elif to_email:
            # Используем указанный email без привязки к конкретному контакту
            communications.append({
                # # 'TYPE': 'EMAIL',
                # 'ENTITY_ID': contact_id,
                # 'ENTITY_TYPE_ID': 3,  # Контакт
                'VALUE': to_email
            })
            activity_data['SETTINGS']['EMAIL_META']['to'] = to_email
            logger.info(f"Добавлен произвольный email: {to_email}")
        
        # Добавляем коммуникации если есть
        if communications:
            activity_data['COMMUNICATIONS'] = communications
        else:
            raise ValueError("Необходимо указать либо contact_id, либо to_email")

             
        logger.debug(f"Данные активности: {activity_data}")
        


        # Создаем активность через API
        result = await bitrix.call(
            'crm.activity.add',
            {'fields': activity_data}
        )
        
        if result:
            # Получаем созданную активность
            activity_manager = cls.get_manager(bitrix)
            created_activity = await activity_manager.get_by_id(result)
            logger.success(f"Email-активность создана с ID: {result}")
            return created_activity
        
        raise Exception("Не удалось создать email-активность")


class ActivityManager(RelatedManager['Activity']):
    """Менеджер для работы с активностями сущности"""
    
    def __init__(self, bitrix, parent_entity, activity_class: Type[Activity] = Activity):
        super().__init__(bitrix, parent_entity, activity_class)
        self._entity_type = self._get_entity_type()
        self._activity_class = activity_class  # Сохраняем класс активности
        logger.debug(f"Инициализирован ActivityManager для {self._entity_type}")
    
    def _get_entity_type(self) -> str:
        """Определение типа родительской сущности"""
        entity_name = self._parent_entity.__class__.__name__.upper()
        if entity_name == 'DEAL':
            return 'DEAL'
        elif entity_name == 'LEAD':
            return 'LEAD'
        elif entity_name == 'CONTACT':
            return 'CONTACT'
        elif entity_name == 'COMPANY':
            return 'COMPANY'
        else:
            return 'UNKNOWN'
    
    async def get_all(self) -> List[Activity]:
        """Получение всех активностей для родительской сущности"""
        if not self._parent_entity.id:
            return []
        
        logger.debug(f"Получение активностей для {self._entity_type} ID {self._parent_entity.id}")
        owner_type_mapping = {
            'DEAL': 2,      # CCrmOwnerType::Deal
            'LEAD': 1,      # CCrmOwnerType::Lead  
            'CONTACT': 3,   # CCrmOwnerType::Contact
            'COMPANY': 4    # CCrmOwnerType::Company
        }

        result = await self._bitrix.get_all(
            'crm.activity.list',
            {
                'filter': {
                    'OWNER_TYPE_ID': owner_type_mapping[self._entity_type],
                    'OWNER_ID': self._parent_entity.id
                },
                'select':['*','COMMUNICATIONS']
            }
        )
        if isinstance(result, dict):

            if result.get('order0000000000'):
                result = result['order0000000000']
        
        activities = [self._activity_class(self._bitrix, item) for item in result]
        logger.debug(f"Найдено {len(activities)} активностей")

        return activities
    
    async def create_call(self, subject: str, phone: str, description: str = "",
                         direction: int = 2, completed: bool = False) -> Activity:
        """Создание активности-звонка"""
        logger.info(f"Создание звонка для {self._entity_type} ID {self._parent_entity.id}")
        
        activity = self._activity_class(self._bitrix)
        activity.type_id = 1  # Звонок
        activity.entity_type = self._entity_type
        activity.entity_id = self._parent_entity.id
        activity.subject = subject
        activity.description = description
        activity.direction = direction
        activity.completed = completed
        
        await activity.save()
        logger.success(f"Звонок создан с ID: {activity.id}")
        return activity
    
    async def create_meeting(self, subject: str, location: str = "", 
                           start_time: Optional[datetime.datetime] = None,
                           end_time: Optional[datetime.datetime] = None,
                           description: str = "") -> Activity:
        """Создание активности-встречи"""
        logger.info(f"Создание встречи для {self._entity_type} ID {self._parent_entity.id}")
        
        activity = self._activity_class(self._bitrix)
        activity.type_id = 2  # Встреча
        activity.entity_type = self._entity_type
        activity.entity_id = self._parent_entity.id
        activity.subject = subject
        activity.location = location
        activity.description = description
        
        if start_time:
            activity.start_time = start_time
        if end_time:
            activity.end_time = end_time
            
        await activity.save()
        logger.success(f"Встреча создана с ID: {activity.id}")
        return activity
    
    async def mail(self, subject: str, message: str, to_email: Optional[str] = None,
                   contact_id: Optional[int] = None, from_email: Optional[str] = None) -> EmailActivity:
        """
        Создание email-активности для родительской сущности
        
        Args:
            subject: Тема письма
            message: Текст письма  
            to_email: Email получателя (опционально, если указан contact_id)
            contact_id: ID контакта для отправки (приоритет над to_email)
            from_email: Email отправителя (опционально)
        
        Примеры использования:
        # Отправка на email контакта из сделки
        await deal.activity.mail("Предложение", "Текст письма", contact_id=deal.contact_id)
        
        # Отправка на произвольный email  
        await deal.activity.mail("Предложение", "Текст письма", to_email="client@example.com")
        """
        logger.info(f"Создание email для {self._entity_type} ID {self._parent_entity.id}")
        
        # Если не указан contact_id, пытаемся получить из родительской сущности
        if not contact_id and not to_email:
            if hasattr(self._parent_entity, 'contact_id') and self._parent_entity.contact_id:
                contact_id = self._parent_entity.contact_id
                logger.info(f"Используем контакт из {self._entity_type}: {contact_id}")
            else:
                raise ValueError("Необходимо указать либо contact_id, либо to_email")
        
        # Если указан только contact_id без fallback email, используем дефолтный
        if contact_id and not to_email:
            to_email = "default@example.com"  # можно настроить дефолтный email
            logger.debug(f"Установлен fallback email: {to_email}")
        
        email_activity = await EmailActivity.create_for_entity(
            self._bitrix,
            self._entity_type,
            self._parent_entity.id,
            subject,
            message,
            to_email,
            contact_id,
            from_email
        )
        
        return email_activity 