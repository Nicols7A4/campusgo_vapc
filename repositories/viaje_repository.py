class ViajeRepository:
    def __init__(self, connection):
            self.connection = connection

    def obtener_conductor_id_por_usuario(self, usuario_id):
        cursor = self.connection.cursor()
        try:
            sql = "SELECT id FROM conductor WHERE usuario_id = %s"
            cursor.execute(sql, (usuario_id,))
            fila = cursor.fetchone()
            return fila["id"] if fila else None
        finally:
            cursor.close()

    def crear(self, conductor_id, datos):
        cursor = self.connection.cursor()
        try:
            sql = """
                INSERT INTO viaje (
                conductor_id, origen, destino, fecha,
                hora, cupos, precio, estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'DISPONIBLE')
            """
            cursor.execute(sql, (
                conductor_id,
                datos["origen"],
                datos["destino"],
                datos["fecha"],
                datos["hora"],
                datos["cupos"],
                datos["precio"]
            ))

            # MySQLdb.OperationalError: (1292, "Incorrect date value: '17-10-2026' for column `campusgo`.`viaje`.`fecha` at row 1")

            return cursor.lastrowid
        finally:
            cursor.close()

    def listar(self, origen=None, destino=None, fecha=None, estado=None):
        cursor = self.connection.cursor()
        try:
            sql = """
                SELECT
                v.id, v.origen, v.destino, v.fecha, v.hora,
                v.cupos, v.precio, v.estado,
                CONCAT(u.nombres, ' ', u.apellidos) AS conductor
                FROM viaje v
                INNER JOIN conductor c ON c.id = v.conductor_id
                INNER JOIN usuario u ON u.id = c.usuario_id
                WHERE 1 = 1
            """
            params = []
            if origen:
                sql += " AND v.origen LIKE %s"
                params.append(f"%{origen}%")
            if destino:
                sql += " AND v.destino LIKE %s"
                params.append(f"%{destino}%")
            if fecha:
                sql += " AND v.fecha = %s"
                params.append(fecha)
            if estado:
                sql += " AND v.estado = %s"
                params.append(estado)

            sql += " ORDER BY v.fecha, v.hora"
            cursor.execute(sql, tuple(params))
            return cursor.fetchall()
        finally:
            cursor.close()

    def obtener_por_id(self, viaje_id):
        cursor = self.connection.cursor()
        try:
            sql = """
                SELECT
                v.*, c.usuario_id AS conductor_usuario_id
                FROM viaje v
                INNER JOIN conductor c ON c.id = v.conductor_id
                WHERE v.id = %s
            """
            cursor.execute(sql, (viaje_id,))
            return cursor.fetchone()
        finally:
            cursor.close()



    def actualizar(self, viaje_id, datos):
        cursor = self.connection.cursor()
        try:
            sql = """
                UPDATE viaje
                SET origen = %s,
                destino = %s,
                fecha = %s,
                hora = %s,
                cupos = %s,
                precio = %s
                WHERE id = %s
            """
            cursor.execute(sql, (
                datos["origen"], datos["destino"],
                datos["fecha"], datos["hora"],
                datos["cupos"], datos["precio"],
                viaje_id
            ))
            return cursor.rowcount
        finally:
            cursor.close()

    def cancelar(self, viaje_id):
        cursor = self.connection.cursor()
        try:
            sql = """
                UPDATE viaje
                SET estado = 'CANCELADO'
                WHERE id = %s
            """
            cursor.execute(sql, (viaje_id,))
            return cursor.rowcount
        finally:
            cursor.close()