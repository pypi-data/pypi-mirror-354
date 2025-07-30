import datetime as dt
from typing import Any, List, Union

from pydantic import BaseModel


class Property(BaseModel):
    name: str
    value: Any = None
    json_value: Union[str, List[str], None] = None


class EntityMeta(BaseModel):
    pv: Union[int, None] = None
    origin_id: Union[str, None] = None
    md5: Union[str, None] = None
    edit_user: Union[str, None] = None
    audit_user: Union[str, None] = None
    domain: Union[str, List[str], None] = None
    operation_domain: Union[str, List[str], None] = None


class Entity(BaseModel):
    id: Union[str, None] = None
    entity_name: str
    entity_type: Union[str, None] = None
    entity_tags: Union[str, List[str], None] = None
    entity_title: Union[str, None] = None
    properties: Union[List[Property], None] = None
    create_time: Union[dt.datetime, None] = None
    meta: Union[EntityMeta, None] = None
    version: Union[str, None] = None


class PartialEntity(Entity):
    entity_name: Union[str, None] = None


class Relation(BaseModel):
    start_entity_id: Union[str, None] = None
    end_entity_id: Union[str, None] = None
    relation_type: str


class Neighbor(BaseModel):
    entity: Entity
    relation_type: str
