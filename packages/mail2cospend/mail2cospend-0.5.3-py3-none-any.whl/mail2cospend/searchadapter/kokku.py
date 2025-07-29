from datetime import datetime
from typing import Iterable, Optional

from PyPDF2 import PdfReader
import re
from mail2cospend.data import BonSummary
from mail2cospend.searchadapter.searchadapter import SearchAdapter


class KokkuSearchAdapter(SearchAdapter):
    @classmethod
    def adapter_name(cls) -> str:
        return "Kokku"

    @classmethod
    def _use_pdf_in_mail(cls) -> bool:
        return False

    @classmethod
    def _use_plain_text_in_mail(cls) -> bool:
        return False

    @classmethod
    def _use_html_text_in_mail(self) -> bool:
        return True

    @property
    def _search_query(self) -> str:
        return f'(FROM order@kokku-online.de) (SUBJECT "Vielen") (SINCE "{self.config.get_since_for_imap_query()}")'

    def _get_bon_from_pdf(
        self, pdf: PdfReader, email_timestamp: datetime
    ) -> Optional[BonSummary]:
        return None

    def _get_bon_from_text(
        self, payload: Iterable[str], email_timestamp: datetime, is_html: bool
    ) -> Optional[BonSummary]:
        sum = 0
        # beleg = payload[1] + " " + payload[5]
        next_is_sum = False
        for row in payload:
            if "Gesamtsumme" in row:
                next_is_sum = True
            elif next_is_sum:
                m = re.search(r"\d+\.\d\d €", row)
                sum = float(m.group(0)[:-2])
                break
        bon = BonSummary(
            sum=sum,
            document="",
            timestamp=email_timestamp,
            adapter_name=self.adapter_name(),
        )
        return bon
