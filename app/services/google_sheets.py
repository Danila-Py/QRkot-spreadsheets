from http import HTTPStatus

import gspread
import logging
from google.oauth2.service_account import Credentials
from fastapi import HTTPException
from typing import Optional, List
from gspread.exceptions import SpreadsheetNotFound, APIError

from app.core.config import settings
from app.schemas.charity_project import CharityProjectReport
from app.services.constants import (
    BASE_SCOPE,
    SPREADSHEET_HEADERS,
    SPREADSHEET_COLUMN_COUNT,
    SPREADSHEET_HEADER_RANGE,
    SPREADSHEET_HEADER_BACKGROUND
)

logger = logging.getLogger(__name__)


class GoogleAPIService:
    """Сервис для работы с Google Sheets API."""

    def __init__(self):
        self.client = self._get_client()

    def _get_client(self):
        """Инициализирует клиент Google Sheets."""
        try:
            creds_dict = {
                'type': settings.type,
                'project_id': settings.project_id,
                'private_key_id': settings.private_key_id,
                'private_key': settings.private_key.replace('\\n', '\n'),
                'client_email': settings.client_email,
                'client_id': settings.client_id,
                'auth_uri': settings.auth_uri,
                'token_uri': settings.token_uri,
                'auth_provider_x509_cert_url': (
                    settings.auth_provider_x509_cert_url
                ),
                'client_x509_cert_url': settings.client_x509_cert_url,
            }

            SCOPES = [
                f'{BASE_SCOPE}spreadsheets',
                f'{BASE_SCOPE}drive.file'
            ]

            creds = Credentials.from_service_account_info(creds_dict)
            creds = creds.with_scopes(SCOPES)
            return gspread.authorize(creds)

        except Exception as e:
            logger.error(f'Ошибка инициализации Google API: {str(e)}')
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Ошибка подключения к Google Sheets'
            )

    def update_spreadsheet(
        self,
        projects: List[CharityProjectReport],
        spreadsheet_id: Optional[str] = None
    ) -> str:
        """Обновляет данные в существующей таблице."""
        target_id = spreadsheet_id or settings.spreadsheet_id

        if not target_id:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Не указан ID таблицы'
            )

        try:
            spreadsheet = self.client.open_by_key(target_id)
            worksheet = spreadsheet.sheet1

            worksheet.clear()
            worksheet.update(SPREADSHEET_HEADER_RANGE, [SPREADSHEET_HEADERS])

            data = []
            for project in projects:
                data.append([
                    project.name,
                    project.collection_time,
                    project.description,
                    project.collected_amount,
                    project.close_date
                ])

            if data:
                worksheet.update(f'A2:E{len(data) + 1}', data)

            worksheet.format(SPREADSHEET_HEADER_RANGE, {
                'textFormat': {'bold': True},
                'backgroundColor': SPREADSHEET_HEADER_BACKGROUND
            })

            try:
                worksheet.columns_auto_resize(0, SPREADSHEET_COLUMN_COUNT)
            except APIError as e:
                logger.warning(f'Не удалось изменить размер колонок: {e}')

            logger.info(f'Таблица обновлена {len(data)} проектами')
            return spreadsheet.url

        except SpreadsheetNotFound:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Таблица не найдена. Проверьте ID и права доступа'
            )
        except Exception as e:
            logger.error(f'Ошибка обновления таблицы: {str(e)}')
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Ошибка при обновлении таблицы'
            )


google_api_service = GoogleAPIService()