from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tournament import Tournament,Player


class TournamentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_tournament(self, name: str, max_players: int, start_at) -> Tournament:
        new_tournament = Tournament(name=name, max_players=max_players, start_at=start_at)
        self.session.add(new_tournament)
        await self.session.commit()
        await self.session.refresh(new_tournament)
        return new_tournament

    async def get_tournament(self, tournament_id: int) -> Optional[Tournament]:
        result = await self.session.execute(
            select(Tournament).where(Tournament.id == tournament_id)
        )
        return result.scalars().first()

    async def count_registered_players(self, tournament_id: int) -> int:
        result = await self.session.execute(
            select(func.count(Player.id)).where(Player.tournament_id == tournament_id)
        )
        return result.scalar_one()

