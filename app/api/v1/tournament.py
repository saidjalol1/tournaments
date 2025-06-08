from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tournament import TournamentCreate, TournamentOut
from app.schemas.player import PlayerRegister, PlayerOut


from app.services.tournament import TournamentService
from app.db import get_session

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


async def get_tournament_service(session: AsyncSession = Depends(get_session)) -> TournamentService:
    return TournamentService(session)


@router.post("/", response_model=TournamentOut, status_code=status.HTTP_201_CREATED)
async def create_tournament(
    data: TournamentCreate,
    service: TournamentService = Depends(get_tournament_service),
):
    tournament = await service.create_tournament(data.name, data.max_players, data.start_at)
    return TournamentOut.model_validate(tournament)


@router.post("/{tournament_id}/register", response_model=PlayerOut, status_code=status.HTTP_201_CREATED)
async def register_player(
    tournament_id: int,
    player_data: PlayerRegister,
    service: TournamentService = Depends(get_tournament_service),
):
    player = await service.register_player(tournament_id, player_data.name, player_data.email)
    return PlayerOut.model_validate(player)


@router.get("/{tournament_id}/players", response_model=List[PlayerOut])
async def list_players(
    tournament_id: int,
    service: TournamentService = Depends(get_tournament_service),
):
    players = await service.get_registered_players(tournament_id)
    return players
