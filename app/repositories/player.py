from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tournament import Player


class PlayerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register_player(self, tournament_id: int, name: str, email: str) -> Player:
        new_player = Player(name=name, email=email, tournament_id=tournament_id)
        self.session.add(new_player)
        await self.session.commit()
        await self.session.refresh(new_player)
        return new_player

    async def get_registered_players(self, tournament_id: int) -> List[Player]:
        result = await self.session.execute(
            select(Player).where(Player.tournament_id == tournament_id)
        )
        return result.scalars().all()

    async def is_email_registered(self, tournament_id: int, email: str) -> bool:
        result = await self.session.execute(
            select(Player).where(Player.tournament_id == tournament_id, Player.email == email)
        )
        return result.scalars().first() is not None
