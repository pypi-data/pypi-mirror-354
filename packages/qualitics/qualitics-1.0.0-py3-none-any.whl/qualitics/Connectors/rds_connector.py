from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from  qualitics.Connectors.base import BaseConnector
from  qualitics.Connectors.credential_manager import CredentialManager
from  qualitics.Error.errorHandler import DatabaseOperationError
from  qualitics.Query_builder.PSQL_queries import QueryBuilder
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
import logging
from datetime import datetime
import json
import uuid
from decimal import Decimal

# Configure logger
logger = logging.getLogger(__name__)


class RDSConnector(BaseConnector):
    def __init__(self, config: dict, usage: str):
        self.config = config
        self.engine = None
        self.usage = usage

    def _get_credentials(self):
        if self.usage == 'audit':
            conn_config = self.config['audit']['database']
        else:
            conn_config = self.config['data_source']
        self.credential_manager = CredentialManager(conn_config)
        creds = self.credential_manager.get_credentials()
        return creds

    def connect(self):
        creds = self._get_credentials()
        conn_str = (
            f"postgresql+psycopg2://{creds['username']}:{creds['password']}"
            f"@{creds['host']}:{creds['port']}/{creds['dbname']}"
        )
        self.engine = create_engine(conn_str, poolclass=QueuePool, pool_size=5, max_overflow=10)
        return self.engine

    def run_query(self, query: str) -> list[dict]:
        try:
            if not self.engine:
                self.connect()
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                return [dict(row._mapping) for row in result]  # Convert to dicts
        except Exception as e:
            print(e)
            raise e

    def run_query_batch(self, query: str, batch_size: int = 1000):
        """
        Generator that yields batches of rows (list of dicts).
        """
        if not self.engine:
            self.connect()
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            cursor = result.cursor  # raw DBAPI cursor
            # Get column names
            columns = [col[0] for col in cursor.description]
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield [dict(zip(columns, row)) for row in rows]

