from decimal import Decimal
import datetime

from flask.json.provider import DefaultJSONProvider


class CustomJSONProvider(DefaultJSONProvider):

    ensure_ascii = False

    def default(self, obj):

        # Decimal → float
        if isinstance(obj, Decimal):
            return float(obj)

        # datetime → texto
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%d-%m-%Y %H:%M:%S")

        # date → texto
        if isinstance(obj, datetime.date):
            return obj.strftime("%d-%m-%Y")

        # timedelta → HH:mm:ss
        if isinstance(obj, datetime.timedelta):

            total_seconds = int(obj.total_seconds())

            horas = total_seconds // 3600
            minutos = (total_seconds % 3600) // 60
            segundos = total_seconds % 60

            return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

        return super().default(obj)