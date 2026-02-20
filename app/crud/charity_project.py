from typing import Optional
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCharityRepository
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectReport
from app.services.constants import (
    SECONDS_IN_HOUR,
    SECONDS_IN_MINUTE,
)


class CRUDCharityProject(BaseCharityRepository):
    """Класс дополнительных методов модели CharityProject."""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[CharityProjectReport]:
        """Получает закрытые проекты, отсортированные по скорости закрытия."""
        stmt = (
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(True))
            .order_by(
                (CharityProject.close_date - CharityProject.create_date).asc()
            )
        )
        db_projects = await session.execute(stmt)
        projects = db_projects.scalars().all()
        report_projects = []
        for project in projects:
            if project.close_date and project.create_date:
                collection_time = self._format_time_delta(
                    project.close_date - project.create_date
                )
                report_project = CharityProjectReport(
                    name=project.name,
                    collection_time=collection_time,
                    description=project.description,
                    collected_amount=project.invested_amount,
                    close_date=project.close_date
                )
                report_projects.append(report_project)
        return report_projects

    def _format_time_delta(self, time_delta: timedelta) -> str:
        """Форматирует timedelta в читаемый вид."""
        days = time_delta.days
        hours, remainder = divmod(time_delta.seconds, SECONDS_IN_HOUR)
        minutes, seconds = divmod(remainder, SECONDS_IN_MINUTE)
        if days > 0:
            return f'{days} дн. {hours:02} ч. {minutes:02} мин.'
        if hours > 0:
            return f'{hours} ч. {minutes:02} мин.'
        return f'{minutes} мин. {seconds:02} сек.'


charity_project_crud = CRUDCharityProject(CharityProject)