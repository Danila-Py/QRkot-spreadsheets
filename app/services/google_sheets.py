import logging
from http import HTTPStatus
from typing import List, Optional

import gspread
from fastapi import HTTPException
from google.oauth2.service_account import Credentials

from app.core.config import settings
from app.schemas.charity_project import CharityProjectReport
from app.services.constants import BASE_SCOPE, SPREADSHEET_HEADERS

logger = logging.getLogger(__name__)


class GoogleAPIService:
    """Сервис для работы с Google Sheets API."""

    def __init__(self):
        self.client = self._get_client()

    def _get_client(self):
        """Инициализирует клиент Google Sheets."""
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

        creds = Credentials.from_service_account_info(
            creds_dict
        ).with_scopes(SCOPES)
        return gspread.authorize(creds)

    def update_spreadsheet(
        self,
        projects: List[CharityProjectReport],
        spreadsheet_id: Optional[str] = None
    ) -> str:
        """Обновляет данные в существующей таблице."""
        target_id = spreadsheet_id or settings.spreadsheet_id

        if not target_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Не указан ID таблицы'
            )

        try:
            sheet = self.client.open_by_key(target_id).sheet1
        except gspread.SpreadsheetNotFound:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Таблица не найдена. Проверьте ID и права доступа'
            )

        sheet.clear()
        sheet.update('A1', [SPREADSHEET_HEADERS])

        if projects:
            data = [[
                p.name, p.collection_time, p.description,
                p.collected_amount, p.close_date
            ] for p in projects]
            sheet.update('A2', data)

        sheet.format('A1:E1', {'textFormat': {'bold': True}})
        logger.info(f'Таблица обновлена {len(projects)} проектами')
        return sheet.url


google_api_service = GoogleAPIService()