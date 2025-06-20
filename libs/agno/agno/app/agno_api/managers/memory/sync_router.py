from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, Path, Query
from fastapi.routing import APIRouter

from agno.app.agno_api.managers.memory.schemas import UserMemoryCreateSchema, UserMemorySchema
from agno.app.agno_api.managers.utils import SortOrder
from agno.memory import Memory
from agno.memory.db.schemas.memory import MemoryRow



def attach_sync_routes(router: APIRouter, memory: Memory) -> APIRouter:
    @router.get("/memories", response_model=List[UserMemorySchema], status_code=200)
    def get_memories(
        user_id: Optional[str] = Query(default=None, description="Filter memories by user ID"),
        agent_id: Optional[str] = Query(default=None, description="Filter memories by agent ID"),
        team_id: Optional[str] = Query(default=None, description="Filter memories by team ID"),
        workflow_id: Optional[str] = Query(default=None, description="Filter memories by workflow ID"),
        limit: Optional[int] = Query(default=20, description="Number of memories to return"),
        offset: Optional[int] = Query(default=0, description="Number of memories to skip"),
        sort_by: Optional[str] = Query(default=None, description="Field to sort by"),
        sort_order: Optional[SortOrder] = Query(default=None, description="Sort order (asc or desc)"),
    ) -> List[UserMemorySchema]:
        if memory.db is None:
            raise HTTPException(status_code=500, detail="Database not initialized")

        user_memories = memory.db.get_user_memories_raw(
            limit=limit,
            offset=offset,
            user_id=user_id,
            agent_id=agent_id,
            team_id=team_id,
            workflow_id=workflow_id,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return [UserMemorySchema.from_dict(user_memory) for user_memory in user_memories]

    @router.get("/memories/{memory_id}", response_model=UserMemorySchema, status_code=200)
    def get_memory(memory_id: str = Path()) -> UserMemorySchema:
        if memory.db is None:
            raise HTTPException(status_code=500, detail="Database not initialized")

        user_memory = memory.db.get_user_memory_raw(memory_id=memory_id)
        if not user_memory:
            raise HTTPException(status_code=404, detail=f"Memory with ID {memory_id} not found")

        return UserMemorySchema.from_dict(user_memory)

    @router.post("/memories", response_model=UserMemorySchema, status_code=200)
    def create_memory(payload: UserMemoryCreateSchema) -> UserMemorySchema:
        if memory.db is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        user_memory = memory.db.upsert_user_memory_raw(
            memory=MemoryRow(
                id=None,
                memory={"memory": payload.memory, "topics": payload.topics},
                user_id=payload.user_id,
                last_updated=datetime.now(),
            )
        )
        if not user_memory:
            raise HTTPException(status_code=500, detail="Failed to create memory")

        return UserMemorySchema.from_dict(user_memory)

    @router.put("/memories/{memory_id}", response_model=UserMemorySchema, status_code=200)
    def update_memory(payload: UserMemoryCreateSchema, memory_id: str = Path()) -> UserMemorySchema:
        if memory.db is None:
            raise HTTPException(status_code=500, detail="Database not initialized")

        user_memory = memory.db.upsert_user_memory_raw(
            memory=MemoryRow(
                id=memory_id,
                memory={"memory": payload.memory, "topics": payload.topics or []},
                user_id=payload.user_id,
                last_updated=datetime.now(),
            )
        )
        if not user_memory:
            raise HTTPException(status_code=500, detail="Failed to update memory")

        return UserMemorySchema.from_dict(user_memory)

    @router.delete("/memories/{memory_id}", status_code=204)
    def delete_memory(memory_id: str = Path()) -> None:
        memory.delete_user_memory(memory_id=memory_id)

    return router
