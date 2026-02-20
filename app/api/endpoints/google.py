from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_sheets import google_api_service

router = APIRouter()


class GoogleSheetsError(HTTPException):
    """Исключение для ошибок Google Sheets."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f'Ошибка Google Sheets: {detail}',
        )


class ProjectNotFoundError(HTTPException):
    """Исключение для отсутствующих проектов."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проекты не найдены'
        )


@router.post(
    '/',
    response_model=dict,
    dependencies=[Depends(current_superuser)],
    summary='Обновить отчет в Google Таблице',
    description='Обновляет отчет с закрытыми проектами, '
                'отсортированными по скорости сбора средств'
)
async def update_google_report(
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    """Обновляет отчет в существующей Google Таблице."""
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    if not projects:
        return {
            'message': 'Нет закрытых проектов для отчета',
            'spreadsheet_url': None,
            'projects_count': 0
        }
    spreadsheet_url = google_api_service.update_spreadsheet(projects)

    return {
        'message': 'Отчет успешно обновлен',
        'spreadsheet_url': spreadsheet_url,
        'projects_count': len(projects)
    }