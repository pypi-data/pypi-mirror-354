import json
import uuid

from nsj_sql_utils_lib.dbadapter3 import DBAdapter3


class DAO:
    def __init__(
        self,
        dbconn,
        index_table: str,
    ):
        self._db = DBAdapter3(dbconn)
        self._index_table = index_table

    def get_list(
        self,
        metadata: dict = None,
        limit_results: int = 1000,
        tenant: int = 0,
    ):

        where_clause = "WHERE tenant = %(tenant)s"
        if metadata is not None:
            where_clause += """
            and metadata @> %(metadata)s
            """

        sql = f"""
        SELECT
            external_id, title, embedding, content, reference,
            metadata, chunck_number, total_chunks, created_at, updated_at, tenant
        FROM {self._index_table}
        {where_clause}
        ORDER BY external_id, chunck_number, total_chunks
        LIMIT {limit_results}
        """

        return self._db.execute(sql, metadata=json.dumps(metadata), tenant=tenant)

    def insert(
        self,
        external_id: uuid.UUID,
        embedding: list[float],
        title: str,
        content: str,
        reference: dict[str, any],
        metadata: dict[str, any],
        chunck_number: int,
        total_chunks: int,
        tenant: int = 0,
    ):
        sql = f"""
        insert into {self._index_table}
        (external_id, title, embedding, content, reference, metadata, chunck_number, total_chunks, tenant)
        values (%(external_id)s, %(title)s, %(embedding)s, %(content)s, %(reference)s, %(metadata)s, %(chunck_number)s, %(total_chunks)s, %(tenant)s)
        """

        self._db.execute(
            sql,
            external_id=str(external_id),
            title=title,
            embedding=json.dumps(embedding),
            content=content,
            reference=json.dumps(reference),
            metadata=json.dumps(metadata),
            chunck_number=chunck_number,
            total_chunks=total_chunks,
            tenant=tenant,
        )

    def delete(self, external_id: uuid.UUID, tenant: int = 0):
        sql = f"""
        DELETE FROM {self._index_table}
        WHERE external_id = %(external_id)s
        and tenant = %(tenant)s
        """

        self._db.execute(sql, external_id=external_id, tenant=tenant)
