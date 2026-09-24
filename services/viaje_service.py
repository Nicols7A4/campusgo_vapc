from database import get_connection
from repositories.viaje_repository import ViajeRepository
from datetime import datetime, timedelta

class ViajeService:
    def crear(self, usuario_id, datos):
        obligatorios = ["origen", "destino", "fecha", "hora", "cupos", "precio"]
        if any(campo not in datos for campo in obligatorios):
            return None, "Faltan datos obligatorios", 400
        try:
            datos = dict(datos)
            datos["fecha"] = datetime.strptime(
                datos["fecha"], "%d-%m-%Y"
            ).date().isoformat()
        except (TypeError, ValueError):
            return None, "La fecha debe tener el formato DD-MM-YYYY", 400
        if int(datos["cupos"]) <= 0:
            return None, "Los cupos deben ser mayores que cero", 400
        if float(datos["precio"]) < 0:
            return None, "El precio no puede ser negativo", 400

        connection = get_connection()

        try:
            repository = ViajeRepository(connection)
            conductor_id = repository.obtener_conductor_id_por_usuario(usuario_id)
            if conductor_id is None:
                return None, "El usuario no posee perfil de conductor", 403
            viaje_id = repository.crear(conductor_id, datos)
            connection.commit()
            return {"viaje_id": viaje_id}, "Viaje creado correctamente", 201
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def listar(self, filtros):
        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            viajes = repository.listar(
                filtros.get("origen"),
                filtros.get("destino"),
                filtros.get("fecha"),
                filtros.get("estado")
            )

            for viaje in viajes:
                if isinstance(viaje.get("hora"), timedelta):
                    viaje["hora"] = str(viaje["hora"])

            return viajes, "Viajes obtenidos correctamente", 200
        finally:
            connection.close()

    def obtener(self, viaje_id):
        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            viaje = repository.obtener_por_id(viaje_id)
            if viaje is None:
                return None, "Viaje no encontrado", 404
            return viaje, "Viaje obtenido correctamente", 200
        finally:
            connection.close()


    def actualizar(self, usuario_id, viaje_id, datos):
        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            viaje = repository.obtener_por_id(viaje_id)
            if viaje is None:
                return None, "Viaje no encontrado", 404
            if str(viaje["conductor_usuario_id"]) != str(usuario_id):
                return None, "No puede modificar un viaje de otro conductor", 403
            if viaje["estado"] in ("FINALIZADO", "CANCELADO"):
                return None, "El estado actual no permite modificar el viaje", 409
            repository.actualizar(viaje_id, datos)
            connection.commit()
            return {"viaje_id": viaje_id}, "Viaje actualizado correctamente", 200
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def cancelar(self, usuario_id, viaje_id):
        connection = get_connection()
        try:
            repository = ViajeRepository(connection)
            viaje = repository.obtener_por_id(viaje_id)
            if viaje is None:
                return None, "Viaje no encontrado", 404
            if str(viaje["conductor_usuario_id"]) != str(usuario_id):
                return None, "No puede cancelar un viaje de otro conductor", 403
            if viaje["estado"] == "CANCELADO":
                return None, "El viaje ya se encuentra cancelado", 409
            repository.cancelar(viaje_id)
            connection.commit()
            return {"viaje_id": viaje_id}, "Viaje cancelado correctamente", 200
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()