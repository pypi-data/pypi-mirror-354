from typing import ClassVar, Optional, List, Dict, Any, Type, cast, Union, AsyncIterator, TYPE_CHECKING
import datetime

from .base import (
    BaseEntity, StringField, IntegerField, FloatField, DateTimeField, BooleanField,
    RelatedEntityField, ListField, RelatedManager, CustomField, EntityManager
)
from .company import Company
from .contact import Contact
from .deal import Deal
from .note import Note
from .activity import ActivityManager


class LeadNote(Note):
    def __init__(self, bitrix, lead: Optional['Lead'] = None, data: Optional[Dict[str, Any]] = None):
        super().__init__(bitrix, lead, data)


class LeadNoteManager(RelatedManager[LeadNote]):
    async def create(self, **kwargs) -> LeadNote:
        return await super().create(**kwargs)


class LeadEntityManager(EntityManager['Lead']):

    async def get_by_id(self, lead_id: Union[str, int]) -> Optional['Lead']:
        return await super().get_by_id(lead_id)


class Lead(BaseEntity):
    ENTITY_NAME: ClassVar[str] = "LEAD"
    ENTITY_METHOD: ClassVar[str] = "crm.lead"

    id: Optional[int]
    title: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    closed: Optional[bool]
    comments: Optional[str]

    company_id: Optional[int]
    contact_id: Optional[int]
    assigned_by_id: Optional[int]
    
    company: Optional[Company]
    contact: Optional[Contact]

    id = IntegerField("ID")
    title = StringField("TITLE")
    opportunity = FloatField("OPPORTUNITY")
    currency_id = StringField("CURRENCY_ID")
    stage_id = StringField("STAGE_ID")
    probability = FloatField("PROBABILITY")
    created_at = DateTimeField("DATE_CREATE")
    updated_at = DateTimeField("DATE_MODIFY")
    closed = BooleanField("CLOSED")
    comments = StringField("COMMENTS")
    type_id = StringField("TYPE_ID")
    
    # Связанные сущности
    company_id = IntegerField("COMPANY_ID")
    contact_id = IntegerField("CONTACT_ID")
    assigned_by_id = IntegerField("ASSIGNED_BY_ID")
    
    # Связанные объекты (lazy loading)
    company = RelatedEntityField("COMPANY_ID", Company)
    contact = RelatedEntityField("CONTACT_ID", Contact)

    objects: ClassVar[LeadEntityManager]
    activity: ActivityManager

    @property
    def tags(self) -> List[str]:
        return self._tags
    
    def __init__(self, bitrix, data: Optional[Dict[str, Any]] = None):
        super().__init__(bitrix, data)
        # Инициализация менеджера примечаний
        self.notes = LeadNoteManager(bitrix, self, LeadNote)
        # Инициализация менеджера активностей
        self.activity = ActivityManager(bitrix, self)

    def __str__(self) -> str:
        return f"Lead: {self.title} (ID: {self.id})"
    
    @classmethod
    def get_manager(cls, bitrix) -> LeadEntityManager:
        manager = LeadEntityManager(bitrix, cls)
        cls.objects = manager
        return manager
    
    async def save(self) -> 'Lead':
        """Сохранение лида и связанных данных"""
        # Сначала сохраняем основные данные лида
        await super().save()
        
        # Затем сохраняем товары, если они были изменены
        # await self.products.save()
        
        return self
    
    async def delete(self) -> bool:
        """Удаление лида"""
        if not self.id:
            raise ValueError("Невозможно удалить несохраненный лид")
        
        try:
            await self.bitrix.call(
                method="crm.lead.delete",
                params={"ID": self.id}
            )
            return True
        except Exception as e:
            print(f"Ошибка при удалении лида: {e}")
            return False
        
    async def get_by_id(self, lead_id: Union[str, int]) -> Optional['Lead']:
        return await super().get_by_id(lead_id)
    
    async def get_all(self) -> List['Lead']:
        return await super().get_all()
    
    async def filter(self, **kwargs) -> List['Lead']:
        return await super().filter(**kwargs)
    
    async def create(self, **kwargs) -> 'Lead':
        return await super().create(**kwargs)
    
    async def update(self, **kwargs) -> 'Lead':
        return await super().update(**kwargs)
    
    async def get_by_id(self, lead_id: Union[str, int]) -> Optional['Lead']:
        return await super().get_by_id(lead_id)
    
    async def get_all(self) -> List['Lead']:
        return await super().get_all()
    
    async def filter(self, **kwargs) -> List['Lead']:
        return await super().filter(**kwargs)
    
    async def move_to_deal(self) -> 'Deal':
        """Перемещает лид в сделку и создает компанию и контакт, если они не существуют"""
        deal = Deal(self._bitrix)
        
        if self.company_id:    
            deal.company_id = self.company_id
        
        if self.contact_id:
            deal.contact_id = self.contact_id
        
        deal.title = f'Сделка на основе лида {self.title}'
        deal.lead_id = self.id
        
        await deal.save()
        return deal