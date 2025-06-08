from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.tournament import Tournament, Player
from app.repositories.tournament import TournamentRepository
from app.repositories.player import PlayerRepository
from app.schemas.player import PlayerOut



class TournamentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.tournament_repo = TournamentRepository(session)
        self.player_repo = PlayerRepository(session)


    async def create_tournament(self, name: str, max_players: int, start_at) -> Tournament:
        return await self.tournament_repo.create_tournament(name, max_players, start_at)

    async def register_player(self, tournament_id: int, name: str, email: str) -> Player:
        tournament = await self.tournament_repo.get_tournament(tournament_id)
        if not tournament:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tournament not found")

        registered_count = await self.tournament_repo.count_registered_players(tournament_id)
        if registered_count >= tournament.max_players:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tournament player limit reached")

        if await self.player_repo.is_email_registered(tournament_id, email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered in this tournament")

        return await self.player_repo.register_player(tournament_id, name, email)

    async def get_registered_players(self, tournament_id: int) -> List[PlayerOut]:
        tournament = await self.tournament_repo.get_tournament(tournament_id)
        if not tournament:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tournament not found")

        players = await self.player_repo.get_registered_players(tournament_id)
        
        return [PlayerOut.model_validate(player) for player in players]
