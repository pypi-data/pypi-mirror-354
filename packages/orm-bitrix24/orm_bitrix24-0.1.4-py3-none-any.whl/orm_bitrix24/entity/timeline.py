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
    from .contact import Contact
    from .company import Company


class TimelineCommentEntityManager(EntityManager['TimelineComment']):
    """Кастомный менеджер комментариев таймлайна для правильной типизации"""
    
    async def get_by_id(self, comment_id: Union[str, int]) -> Optional['TimelineComment']:
        """Получение комментария по ID"""
        result = await self._bitrix.call(
            'crm.timeline.comment.get',
            {'id': comment_id}
        )
        if result:
            return self._entity_class(self._bitrix, result)
        return None
    
    async def filter(self, **kwargs) -> List['TimelineComment']:
        """Фильтрация комментариев"""
        filter_params = {}
        
        # Преобразуем kwargs в filter для API
        for key, value in kwargs.items():
            filter_params[key.upper()] = value
        
        result = await self._bitrix.get_all(
            'crm.timeline.comment.list',
            {'filter': filter_params}
        )
        
        return [self._entity_class(self._bitrix, item) for item in result]


class TimelineComment(BaseEntity):
    """Класс для работы с комментариями таймлайна в Bitrix24 CRM"""
    
    ENTITY_NAME: ClassVar[str] = "TIMELINECOMMENT"
    ENTITY_METHOD: ClassVar[str] = "crm.timeline.comment"
    
    # Основные поля комментария таймлайна
    id = IntegerField("ID")
    entity_id = IntegerField("ENTITY_ID")
    entity_type = IntegerField("ENTITY_TYPE_ID")
    author_id = IntegerField("AUTHOR_ID")
    comment = StringField("COMMENT")
    created = DateTimeField("CREATED")
    files = StringField("FILES")
    
    # Объект для подсказок типов IDE
    objects: ClassVar[TimelineCommentEntityManager]
    
    def __init__(self, bitrix, data: Optional[Dict[str, Any]] = None):
        super().__init__(bitrix, data)
        logger.debug(f"Создан комментарий таймлайна ID: {self.id}")
    
    def __str__(self) -> str:
        return f"TimelineComment: ID {self.id} для сущности {self.entity_type} {self.entity_id}"
    
    @classmethod
    def get_manager(cls, bitrix) -> TimelineCommentEntityManager:
        manager = TimelineCommentEntityManager(bitrix, cls)
        cls.objects = manager
        return manager
    
    async def save(self) -> 'TimelineComment':
        """Сохранение комментария таймлайна"""
        logger.info(f"Сохранение комментария таймлайна ID: {self.id}")
        if self.id:
            # Обновление существующего комментария
            fields = {k: v for k, v in self._data.items() if k in self._dirty_fields}
            result = await self._bitrix.call(
                'crm.timeline.comment.update',
                {'id': self.id, 'fields': fields}
            )
            if result:
                # Обновляем данные после сохранения
                self._dirty_fields.clear()
                return self
        else:
            # Создание нового комментария
            result = await self._bitrix.call(
                'crm.timeline.comment.add',
                {'fields': self._data}
            )
            if result:
                # Получаем созданный комментарий
                comment = await self.__class__.objects.get_by_id(result)
                return comment
        
        raise Exception("Не удалось сохранить комментарий таймлайна")
    
    async def delete(self) -> bool:
        """Удаление комментария таймлайна"""
        if not self.id:
            raise ValueError("Невозможно удалить несохраненный комментарий")
        
        logger.info(f"Удаление комментария таймлайна ID: {self.id}")
        result = await self._bitrix.call(
            'crm.timeline.comment.delete',
            {'id': self.id}
        )
        
        return bool(result)


class TimelineCommentManager(RelatedManager['TimelineComment']):
    """Менеджер для работы с комментариями таймлайна"""
    
    def __init__(self, bitrix, timeline_manager):
        self._bitrix = bitrix
        self._timeline_manager = timeline_manager
        self._parent_entity = timeline_manager._parent_entity
        self._comment_class = TimelineComment
        TimelineComment.get_manager(bitrix)
        logger.debug(f"Инициализирован TimelineCommentManager")
    
    async def get_all(self) -> List[TimelineComment]:
        """Получение всех комментариев для родительской сущности"""
        if not self._parent_entity.id:
            return []

        # Определяем тип сущности для API
        entity_type_id = self._timeline_manager._get_entity_type_id()
        entity_type_mapping = {
            2: "DEAL",      # CCrmOwnerType::Deal
            1: "LEAD",      # CCrmOwnerType::Lead  
            3: "CONTACT",   # CCrmOwnerType::Contact
            4: "COMPANY"    # CCrmOwnerType::Company
        }
        logger.debug(f"Получение комментариев таймлайна для сущности ID {self._parent_entity.id}")
        print(f'ENTITY_ID: {self._parent_entity.id}, ENTITY_TYPE_ID: {entity_type_mapping[entity_type_id]}') 
        result = await self._bitrix.get_all(
            'crm.timeline.comment.list',
            {
                'filter': {
                    'ENTITY_ID': self._parent_entity.id,
                    'ENTITY_TYPE': entity_type_mapping[entity_type_id]
                }
            }
        )
        
        comments = [self._comment_class(self._bitrix, item) for item in result]
        logger.debug(f"Найдено {len(comments)} комментариев таймлайна")

        return comments
    
    async def create(self, comment: str, files: Optional[List[int]] = None) -> TimelineComment:
        """Создание комментария в таймлайне"""
        
        
        # Определяем тип сущности для API
        entity_type_id = self._timeline_manager._get_entity_type_id()
        logger.info(f"Создание комментария в таймлайне для сущности ID {self._parent_entity.id} {entity_type_id}")
        entity_type_mapping = {
            2: "DEAL",      # CCrmOwnerType::Deal
            1: "LEAD",      # CCrmOwnerType::Lead  
            3: "CONTACT",   # CCrmOwnerType::Contact
            4: "COMPANY"    # CCrmOwnerType::Company
        }
        fields = {
            'ENTITY_ID': self._parent_entity.id,
            'ENTITY_TYPE': entity_type_mapping[entity_type_id],
            'COMMENT': comment
        }
        
        if files:
            fields['FILES'] = files
        
        result = await self._bitrix.call(
            'crm.timeline.comment.add',
            {'fields': fields}
        )
        
        if result:
            # Получаем созданный комментарий
            created_comment = await self._comment_class.objects.get_by_id(result)
            logger.success(f"Комментарий в таймлайне создан с ID: {result}")
            return created_comment
        
        raise Exception("Не удалось создать комментарий в таймлайне")


class TimelineManager:
    """Менеджер для работы с таймлайном сущности"""
    
    def __init__(self, bitrix, parent_entity):
        self._bitrix = bitrix
        self._parent_entity = parent_entity
        self._entity_type = self._get_entity_type()
        self._comments = TimelineCommentManager(bitrix, self)
        logger.debug(f"Инициализирован TimelineManager для {self._entity_type}")
    
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
            return entity_name
        # return entity_name
    
    def _get_entity_type_id(self) -> int:
        """Получение типа сущности в виде ID для API"""
        entity_type_mapping = {
            'DEAL': 2,      # CCrmOwnerType::Deal
            'LEAD': 1,      # CCrmOwnerType::Lead  
            'CONTACT': 3,   # CCrmOwnerType::Contact
            'COMPANY': 4    # CCrmOwnerType::Company
        }
        return entity_type_mapping.get(self._entity_type, 0)
    
    @property
    def comments(self) -> TimelineCommentManager:
        """Доступ к менеджеру комментариев таймлайна"""
        return self._comments
    
    async def add_log_message(self, title: str, text: str, icon_code: Optional[str] = None) -> dict:
        """
        Добавление лог-записи в таймлайн
        
        Args:
            title: Заголовок лог-записи
            text: Текст лог-записи
            icon_code: Код иконки записи (опционально)
        """
        logger.info(f"Добавление лог-записи в таймлайн для {self._entity_type} ID {self._parent_entity.id}")
        
        # Определяем тип сущности для API
        entity_type_id = self._get_entity_type_id()
        
        fields = {
            'ENTITY_ID': self._parent_entity.id,
            'ENTITY_TYPE_ID': entity_type_id,
            'TITLE': title,
            'TEXT': text
        }
        
        if icon_code:
            fields['ICON_CODE'] = icon_code
        
        result = await self._bitrix.call(
            'crm.timeline.logmessage.add',
            {'fields': fields}
        )
        
        if result:
            logger.success(f"Лог-запись в таймлайне создана с ID: {result}")
            return {'id': result}
        
        raise Exception("Не удалось создать лог-запись в таймлайне") 