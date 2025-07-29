from dataheroes.data.databricks.connection import DatabricksConnection

from typing import Iterator, Optional
import pandas as pd
DATABRICKS_CHUNK_SIZE = 100_000
class DatabricksQueryManager:
    """
    Data manager for Databricks SQL warehouses.

    Parameters
    ----------
    connection: DatabricksConnection
        Connection to Databricks SQL warehouse
    """

    def __init__(
        self,
        connection: DatabricksConnection,
    ):
        self.connection = connection
        self._use_arrow: bool = False
        try:
            import pyarrow  # check if pyarrow is installed, if not, use the default method. fetchall_arrow() needs pyarrow installed

            self._use_arrow = True
        except ImportError:
            print("pyarrow is not installed, using the default method")

    def _get_chunks_from_table(
        self,
        query: str,
        chunk_size: Optional[int] = DATABRICKS_CHUNK_SIZE,
    ) -> Iterator[pd.DataFrame]:
        """
        Executes a query and yields pandas DataFrames in chunks.

        Parameters
        ----------

        query : str
            The query to execute.

        chunk_size : int
            The size of the chunk to fetch.

        Returns
        -------
        Iterator[pd.DataFrame]
            An iterator of pandas DataFrames.
        """
        if chunk_size is None:
            chunk_size = DATABRICKS_CHUNK_SIZE  # Default chunk size when not specified
        with self.connection.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)

                # Grab column names from DB-API cursor.description
                col_names = [desc[0] for desc in cursor.description]
                # -1 means that the chunk size is set to the number of instances of the dataset
                if chunk_size == -1:
                    if self._use_arrow:
                        # This is faster than the default method
                        df = cursor.fetchall_arrow().to_pandas()
                    else:
                        df = pd.DataFrame(cursor.fetchall(), columns=col_names)

                    yield df
                else:
                    while True:
                        chunk = (
                            cursor.fetchmany_arrow(chunk_size)
                            if self._use_arrow
                            else cursor.fetchmany(chunk_size)
                        )
                        if not chunk:
                            break
                        df = (
                            chunk.to_pandas()
                            if self._use_arrow
                            else pd.DataFrame(chunk, columns=col_names)
                        )

                        yield df

    def get_data(self, query: str, chunk_size: Optional[int] = DATABRICKS_CHUNK_SIZE) -> Iterator[pd.DataFrame]:
        """
        Get data from Databricks SQL warehouse in chunks.

        Parameters
        ----------
        query: str
            SQL query to execute
        chunk_size: int, default=100_000
            Number of rows to fetch in each chunk

        Returns
        -------
        Iterator[pd.DataFrame]
            Iterator yielding chunks of data as pandas DataFrames
        """
        return self._get_chunks_from_table(query, chunk_size)
