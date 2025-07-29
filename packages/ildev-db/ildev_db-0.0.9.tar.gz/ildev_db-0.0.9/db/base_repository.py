from typing import Type, TypeVar, Generic, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy import asc, desc
from db.base_model import Base
from db.exception import handle_db_exceptions
from db.base_query_params import BaseQueryParams

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    @handle_db_exceptions(allow_return=True)
    async def get_one(self, db: AsyncSession, options: Optional[List[Any]] = None, **filters) -> Optional[ModelType]:
        """Fetch one record, with optional eager loading."""
        stmt = select(self.model)

        if filters:
            stmt = stmt.filter_by(**filters)

        if options:
            stmt = stmt.options(*options)

        result = await db.execute(stmt)
        return result.scalars().first()

    @handle_db_exceptions(allow_return=True, return_data=[])
    async def get_all(
        self,
        db: AsyncSession,
        query_params: Optional[BaseQueryParams] = BaseQueryParams(),
    ) -> List[ModelType]:
        """
        Fetch multiple records based on query parameters.

        Args:
            db (AsyncSession): The database session.
            query_params (QueryParams): optional structured query parameters.

        Returns:
            List[ModelType]: A list of matching records.
        """
        stmt = select(self.model)

        if query_params.filters:
            stmt = stmt.filter_by(**query_params.filters)

        if query_params.order_by:
            column = getattr(self.model, query_params.order_by, None)
            if column:
                stmt = stmt.order_by(asc(column) if query_params.sort.lower() == "asc" else desc(column))

        if query_params.limit is not None:
            stmt = stmt.offset(query_params.offset).limit(query_params.limit)

        result = await db.execute(stmt)
        return result.scalars().all()


    @handle_db_exceptions()
    async def create(self, db: AsyncSession, obj_data: dict) -> ModelType:
        # First: Check top-level model uniqueness
        unique_fields = getattr(self.model, "__unique_fields__", [])
        filters = {
            field: obj_data.get(field)
            for field in unique_fields
            if obj_data.get(field) is not None
        }

        if filters:
            stmt = select(self.model).filter_by(**filters)
            result = await db.execute(stmt)
            existing_obj = result.scalars().first()
            if existing_obj:
                return existing_obj  # Don't try to re-insert

        related_fields = {}
        related_cache = {}  # Add this

        for key, value in obj_data.items():
            if hasattr(self.model, key):
                relation = getattr(self.model, key)
                if hasattr(relation, "property") and hasattr(relation.property, "mapper"):
                    related_model = relation.property.mapper.class_

                    if isinstance(value, list):
                        related_objs = []

                        for v in value:
                            key_tuple = (related_model.__name__, tuple(sorted(v.items()))) if isinstance(v, dict) else (related_model.__name__, v)

                            if key_tuple in related_cache:
                                related_objs.append(related_cache[key_tuple])
                                continue
                            
                            existing_obj = None

                            if isinstance(v, dict):
                                unique_fields = getattr(related_model, "__unique_fields__", [])
                                filters = {
                                    field: v[field]
                                    for field in unique_fields
                                    if field in v and v[field] is not None
                                }

                                if filters:
                                    stmt = select(related_model).filter_by(**filters)
                                    result = await db.execute(stmt)
                                    existing_obj = result.scalars().first()

                                if existing_obj:
                                    related_cache[key_tuple] = existing_obj
                                    related_objs.append(existing_obj)
                                else:
                                    new_obj = related_model(**v)
                                    db.add(new_obj)
                                    await db.flush()
                                    related_cache[key_tuple] = new_obj
                                    related_objs.append(new_obj)

                            elif isinstance(v, int):
                                obj = await db.get(related_model, v)
                                if obj:
                                    related_cache[key_tuple] = obj
                                    related_objs.append(obj)

                        # ✅ Deduplicate here
                        seen_ids = set()
                        deduped_related_objs = []
                        for obj in related_objs:
                            obj_id = getattr(obj, "id", None)
                            if obj_id and obj_id not in seen_ids:
                                seen_ids.add(obj_id)
                                deduped_related_objs.append(obj)

                        related_fields[key] = deduped_related_objs

                    elif isinstance(value, dict):
                        unique_fields = getattr(related_model, "__unique_fields__", [])
                        filters = {
                            field: value[field]
                            for field in unique_fields
                            if field in value and value[field] is not None
                        }

                        existing_obj = None
                        if filters:
                            stmt = select(related_model).filter_by(**filters)
                            result = await db.execute(stmt)
                            existing_obj = result.scalars().first()

                        if existing_obj:
                            related_fields[key] = existing_obj
                        else:
                            new_obj = related_model(**value)
                            db.add(new_obj)
                            await db.flush()
                            related_fields[key] = new_obj

        obj_data = {**obj_data, **related_fields}
        obj = self.model(**obj_data)
        db.add(obj)
        await db.flush()
        await db.refresh(obj)
        return obj


    @handle_db_exceptions()
    async def update(self, db: AsyncSession, id: int, obj_data: dict) -> ModelType:
        """Update a record."""
        obj = await self.get_one(db, id=id)
        if obj is None:
            error_text = f"{self.model.__name__} with ID {id} not found"
            raise NoResultFound(error_text)  # Custom error handling
        for key, value in obj_data.items():
            setattr(obj, key, value)
        await db.flush()
        await db.refresh(obj)
        return obj       

    @handle_db_exceptions()
    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Delete a record."""
        obj = await self.get_one(db, id=id)
        if obj:            
            await db.delete(obj)
            await db.flush()
            return True

        return False