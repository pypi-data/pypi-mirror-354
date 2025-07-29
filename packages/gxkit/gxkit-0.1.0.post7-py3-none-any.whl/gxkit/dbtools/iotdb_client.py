import logging
import re
import time
from datetime import datetime, timedelta
import pandas as pd
from typing import Optional, List, Tuple, Iterator, Sequence, Union, Any
from iotdb import SessionPool
from iotdb.SessionPool import create_session_pool, PoolConfig
from iotdb.utils.exception import IoTDBConnectionException
from gxkit.dbtools._base import BaseDBClient, DBConnectionError, SQLExecutionError
from gxkit.dbtools.sql_parser import SQLParser


class IoTDBClient(BaseDBClient):
    """
    IoTDBClient - Apache IoTDB 原生客户端
    Version: 0.1.1
    """

    def __init__(self, host: str, port: int, user: str, password: str, max_pool_size: int = 10,
                 wait_timeout_in_ms: int = 3000, **kwargs):
        self.pool: Optional[SessionPool] = None
        self.db_type = "iotdb"
        self._last_success_time: Optional[datetime] = None
        self._reconnect_delay: timedelta = timedelta(minutes=10)
        self._connection_params = dict(host=host, port=port, user=user, password=password,
                                       max_pool_size=max_pool_size,
                                       wait_timeout_in_ms=wait_timeout_in_ms, **kwargs)
        self.connect(host, port, user, password, max_pool_size, wait_timeout_in_ms, **kwargs)

    def connect(self, host: str, port: int, user: str, password: str, max_pool_size: int, wait_timeout_in_ms: int,
                **kwargs) -> None:
        try:
            config = PoolConfig(host=host, port=str(port), user_name=user, password=password, **kwargs)
            self.pool = create_session_pool(config, max_pool_size=max_pool_size, wait_timeout_in_ms=wait_timeout_in_ms)
            session = self.pool.get_session()
            try:
                session.execute_query_statement("SHOW STORAGE GROUP").close_operation_handle()
                self._last_success_time = datetime.now()
            finally:
                self.pool.put_back(session)
        except Exception as e:
            raise DBConnectionError("dbtools.IoTDBClient.connect", "iotdb", str(e)) from e

    def execute(self, sql: str, auto_decision: bool = False, stream: bool = False, batch_size: int = 10000,
                prefix_path: int = 1, use_native: bool = False, max_retry: int = 3) -> Union[
        pd.DataFrame, Iterator[pd.DataFrame], int, None]:
        if self.pool is None:
            raise DBConnectionError("dbtools.IoTDBClient.execute", "iotdb", "Database not connected")
        parsed_sql = SQLParser(sql, db_type="iotdb")
        sql_type = parsed_sql.sql_type()
        session = self.pool.get_session()

        if sql_type == "statement" and stream:
            logging.warning(
                "[dbtools.IoTDBClient.execute] | Stream function unsupported for this SQL. Using normal execution.")
            stream = False
        try:
            if auto_decision and sql_type == "query":
                need_page, limit_size = self._decision(session, sql, parsed_sql, prefix_path)
                if need_page:
                    if stream:
                        batch_size = self._adjust_batch_size_for_limit(batch_size, limit_size, context="execute")
                        return self._stream_paged(session, parsed_sql, batch_size, prefix_path, use_native)
                    return self._execute_paged(session, parsed_sql, prefix_path, use_native, limit_size)
            if stream and sql_type == "query":
                return self._stream_core_retry_wrapper(session, sql, batch_size, prefix_path, use_native, max_retry)
            return self._execute_core_retry_wrapper(session, sql, sql_type, prefix_path, use_native, max_retry)
        except Exception as e:
            raise SQLExecutionError("dbtools.IoTDBClient.execute", sql, str(e)) from e
        finally:
            if not (stream and sql_type == "query"):
                self.pool.put_back(session)

    def executemany(self, sqls: Sequence[str], auto_decision: bool = False, stream: bool = False,
                    batch_size: int = 10000, collect_results: bool = True, prefix_path: int = 1,
                    use_native: bool = False, max_retry: int = 3) -> Optional[list]:
        if self.pool is None:
            raise DBConnectionError("dbtools.IoTDBClient.executemany", "iotdb", "Not connected")

        session = self.pool.get_session()
        results = []
        try:
            for sql in sqls:
                parsed = SQLParser(sql, db_type="iotdb")
                sql_type = parsed.sql_type()
                if auto_decision and sql_type == "query":
                    need_page, limit_size = self._decision(session, sql, parsed, prefix_path)
                    if need_page:
                        if stream:
                            batch_size = self._adjust_batch_size_for_limit(batch_size, limit_size,
                                                                           context="executemany")
                            result = self._stream_paged(session, parsed, batch_size, prefix_path, use_native)
                        else:
                            result = self._execute_paged(session, parsed, prefix_path, use_native, limit_size)
                    else:
                        result = self._stream_core_retry_wrapper(session, sql, batch_size, prefix_path,
                                                                 use_native, max_retry) if stream else \
                            self._execute_core_retry_wrapper(session, sql, sql_type, prefix_path, use_native, max_retry)
                else:
                    result = self._stream_core_retry_wrapper(session, sql, batch_size, prefix_path,
                                                             use_native, max_retry) if (
                            stream and sql_type == "query") else \
                        self._execute_core_retry_wrapper(session, sql, sql_type, prefix_path, use_native, max_retry)
                if collect_results and sql_type == "query":
                    results.append(result)
            return results if collect_results else None
        except Exception as e:
            raise SQLExecutionError("dbtools.IoTDBClient.executemany", "\n".join(sqls), str(e)) from e
        finally:
            self.pool.put_back(session)

    def close(self) -> None:
        if self.pool:
            self.pool.close()
            self.pool = None

    def _execute_core_retry_wrapper(self, session, sql: str, sql_type: str, prefix_path: int,
                                    use_native: bool, max_retry: int) -> Union[pd.DataFrame, int, None]:
        current_session = session
        for retry in range(max_retry):
            try:
                return self._execute_core(current_session, sql, sql_type, prefix_path, use_native)
            except IoTDBConnectionException as e:
                logging.warning(f"[IoTDBClient._execute_core] Retry {retry + 1}/{max_retry}: {e}")
                try:
                    self.pool.put_back(current_session)
                except Exception:
                    pass
                self.close()
                self.connect(**self._connection_params)
                time.sleep(0.5)
                current_session = self.pool.get_session()
            except SQLExecutionError as e:
                raise SQLExecutionError("dbtools.IoTDBClient._execute_core_retry_wrapper", sql, str(e)) from e
        raise SQLExecutionError("dbtools.IoTDBClient._execute_core", sql, f"Failed after {max_retry} retries")

    def _stream_core_retry_wrapper(self, session, sql: str, batch_size: int, prefix_path: int,
                                   use_native: bool, max_retry: int) -> Optional[Iterator[pd.DataFrame]]:
        current_session = session
        for retry in range(max_retry):
            try:
                return self._stream_core(current_session, sql, batch_size, prefix_path, use_native)
            except IoTDBConnectionException as e:
                logging.warning(f"[IoTDBClient._stream_core] Retry {retry + 1}/{max_retry}: {e}")
                try:
                    self.pool.put_back(current_session)
                except Exception:
                    pass
                self.close()
                self.connect(**self._connection_params)
                time.sleep(0.5)
                current_session = self.pool.get_session()
            except SQLExecutionError as e:
                raise SQLExecutionError("dbtools.IoTDBClient._stream_core_retry_wrapper", sql, str(e)) from e
        raise SQLExecutionError("dbtools.IoTDBClient._stream_core", sql, f"Failed after {max_retry} retries")

    def _execute_paged(self, session, parsed_sql: SQLParser, prefix_path: int, use_native: bool,
                       limit: int) -> Optional[pd.DataFrame]:
        dfs = list(self._paged_generator(session, parsed_sql, limit, prefix_path, use_native))
        if not dfs:
            return None
        return pd.concat(dfs, ignore_index=True)

    def _stream_paged(self, session, parsed_sql: SQLParser, batch_size: int, prefix_path: int,
                      use_native: bool) -> Optional[Iterator[pd.DataFrame]]:
        generator = self._paged_generator(session, parsed_sql, batch_size, prefix_path, use_native)

        try:
            first_batch = next(generator)
        except StopIteration:
            return None

        def stream_generator():
            yield first_batch
            for batch in generator:
                yield batch

        return stream_generator()

    def _paged_generator(self, session, parsed_sql: SQLParser, limit: int, prefix_path: int,
                         use_native: bool) -> Iterator[pd.DataFrame]:
        seg_where = parsed_sql.segments('where').get('where')
        original_where = seg_where[0] if seg_where else None
        start_ts, end_ts = None, None
        if original_where:
            time_start_pattern = r"(?i)\bTime\s*(>=|>)\s*(\d+(?:\.\d+)?|'[^']+'|\"[^\"]+\")"
            time_end_pattern = r"(?i)\bTime\s*(<=|<)\s*(\d+(?:\.\d+)?|'[^']+'|\"[^\"]+\")"
            match_start = re.search(time_start_pattern, original_where)
            match_end = re.search(time_end_pattern, original_where)
            if match_start:
                start_ts = match_start.group(2).strip("'\"")
            if match_end:
                end_ts = match_end.group(2).strip("'\"")
        last_ts = start_ts
        max_iterations = 1000
        iteration = 0

        while True:
            iteration += 1
            if iteration >= max_iterations:
                logging.warning("[IoTDBClient._paged_generator] | Reached max page iterations.")
                break
            logging.debug(f"[IoTDBClient._paged_generator] | last_ts: {last_ts}")
            if original_where and original_where.strip():
                where_clause = original_where.strip()
                cond = f"Time > {last_ts}" if last_ts is not None else None
                if cond:
                    time_gt_pattern = r"(?i)\bTime\s*(>=|>)\s*(\d+(?:\.\d+)?|'[^']+'|\"[^\"]+\")"
                    if re.search(time_gt_pattern, where_clause):
                        final_where = re.sub(time_gt_pattern, cond, where_clause, count=1)
                    else:
                        final_where = f"({where_clause}) AND {cond}"
                else:
                    final_where = where_clause
            elif last_ts:
                final_where = f"Time > {last_ts}"
            else:
                final_where = None
            logging.debug(f"[IoTDBClient._paged_generator] | final_where: {final_where}")
            replacements = {"limit": str(limit)}
            if final_where:
                replacements["where"] = final_where
            page_sql = parsed_sql.change_segments(replacements)
            logging.debug(f"[IoTDBClient._paged_generator] | page_sql: {page_sql}")
            df = self._execute_core_retry_wrapper(session, page_sql, "query", prefix_path, use_native, max_retry=3)
            if df is None or df.empty:
                break
            yield df
            if len(df) < limit:
                break
            prev_ts = last_ts
            ts_max = df["timestamp"].max()
            if pd.notnull(ts_max):
                try:
                    last_ts = int(ts_max) + 1
                except Exception:
                    logging.warning(f"[IoTDBClient._paged_generator] | Invalid timestamp {ts_max}")
                    break
            else:
                break
            if last_ts == prev_ts:
                logging.warning("[IoTDBClient._paged_generator] | Timestamp not progressing. Breaking to avoid loop.")
                break
            if end_ts is not None and float(last_ts) >= float(end_ts):
                break

    def _execute_core(self, session, sql: str, sql_type: str, prefix_path: int, use_native: bool) -> Union[
        pd.DataFrame, int, None]:
        self._check_and_reconnect()
        if sql_type != "query":
            session.execute_non_query_statement(sql)
            self._last_success_time = datetime.now()
            return 1
        result_set, col_mapping, columns = self._get_result_set(session, sql, prefix_path)

        rows = [self._build_row(record, col_mapping, use_native) for record in iter(result_set.next, None)]
        result_set.close_operation_handle()
        self._last_success_time = datetime.now()
        if not rows:
            return None
        return pd.DataFrame(rows, columns=columns)

    def _stream_core(self, session, sql: str, batch_size: int, prefix_path: int, use_native: bool) -> Optional[
        Iterator[pd.DataFrame]]:
        self._check_and_reconnect()
        result_set, col_mapping, columns = self._get_result_set(session, sql, prefix_path)

        first_record = result_set.next()
        if first_record is None:
            result_set.close_operation_handle()
            return None

        def generator():
            try:
                batch = [self._build_row(first_record, col_mapping, use_native)]
                has_yielded = False
                for record in iter(result_set.next, None):
                    batch.append(self._build_row(record, col_mapping, use_native))
                    if len(batch) >= batch_size:
                        self._last_success_time = datetime.now()
                        yield pd.DataFrame(batch, columns=columns)
                        has_yielded = True
                        batch.clear()
                if batch:
                    self._last_success_time = datetime.now()
                    yield pd.DataFrame(batch, columns=columns)
                    has_yielded = True
            finally:
                result_set.close_operation_handle()
                if self.pool:
                    self.pool.put_back(session)
            if not has_yielded:
                return None

        return generator()

    def _get_result_set(self, session, sql: str, prefix_path: int) -> Tuple[pd.DataFrame, List, List]:
        self._check_and_reconnect()
        result_set = session.execute_query_statement(sql)
        self._last_success_time = datetime.now()
        raw_cols = result_set.get_column_names()
        col_mapping = self._build_col_mapping(raw_cols, prefix_path)
        columns = [short for _, short in col_mapping]
        return result_set, col_mapping, columns

    def _check_and_reconnect(self):
        if self.pool is None or self._last_success_time is None:
            return

        now = datetime.now()
        if now - self._last_success_time > self._reconnect_delay:
            session = None
            try:
                logging.info("[dbtools.IoTDBClient] Reconnecting due to inactivity timeout")
                session = self.pool.get_session()
                session.execute_query_statement("SHOW STORAGE GROUP").close_operation_handle()
                self._last_success_time = now
            except Exception:
                logging.warning("[dbtools.IoTDBClient] Ping failed, reconnecting from scratch...")
                if session is not None:
                    try:
                        self.pool.put_back(session)
                    except Exception:
                        pass
                self.close()
                self.connect(**self._connection_params)
                self._last_success_time = datetime.now()
            else:
                self.pool.put_back(session)

    def _decision(self, session, sql: str, parsed_sql: SQLParser, prefix_path: int) -> Tuple[bool, int]:
        max_columns = 200
        max_rows = 100_000
        max_cells = 1_000_000
        fallback_limit = 10_000
        small_limit_threshold = 2_000

        if parsed_sql.sql_type() != "query":
            return False, fallback_limit
        if parsed_sql.operation() not in {"select", "union", "intersect", "except", "with"}:
            return False, fallback_limit

        try:
            columns = self._get_columns(session, parsed_sql, prefix_path)
            column_count = len(columns)
            # 空字段直接return
            if column_count == 0:
                logging.warning("[IoTDBClient._decision] | No columns found, skipping pagination.")
                return False, fallback_limit
            # 聚合函数单字段直接return
            if column_count == 1 and re.match(r"(?i)\b(count|sum|avg|min|max)\s*\(.*\)", columns[0]):
                logging.debug("[IoTDBClient._decision] | Single aggregation column detected, skipping pagination.")
                return False, 1

            # sql中主动设定了 limit
            user_limit = parsed_sql.segments("limit").get("limit")
            if user_limit:
                try:
                    limit_value = int(user_limit[0].split()[1])
                    if limit_value <= small_limit_threshold:
                        return False, limit_value
                except Exception:
                    pass

            # 获取数据总行数
            count_column = columns[1].split(".")[-1] if len(columns) > 1 else columns[0].split(".")[-1]
            row_count = self._get_rows(session, parsed_sql, count_column)

            limit_value = max(1, max_cells // column_count)
            if row_count:
                limit_value = min(limit_value, row_count)
            cell_score = (column_count * row_count) / max_cells
            need_page = cell_score > 1.0 or column_count > max_columns or row_count > max_rows

            return need_page, limit_value
        except Exception as e:
            raise SQLExecutionError("dbtools.IoTDBClient._decision", sql, str(e)) from e

    def _get_columns(self, session, parsed_sql: SQLParser, prefix_path: int) -> Optional[List[str]]:
        try:
            column_sql = parsed_sql.change_segments({"limit": "10"})
            _, _, columns = self._get_result_set(session, column_sql, prefix_path)
            return columns
        except Exception:
            return []

    def _get_rows(self, session, parsed_sql: SQLParser, column: str) -> int:
        limit = parsed_sql.segments("limit").get("limit")
        count_limit = None if not limit else int(limit[0].split()[1])
        try:
            count_sql = SQLParser(parsed_sql.change_columns(f"count({column})"), db_type="iotdb").sql()
        except Exception:
            inner_sql = parsed_sql.sql()
            count_sql = f"SELECT count(*) FROM ({inner_sql})"
        count_df = self._execute_core_retry_wrapper(session, count_sql, "query", prefix_path=1, use_native=False,
                                                    max_retry=3)
        count_lines = int(count_df.iloc[0, 0]) if count_df is not None else 0
        return min(count_limit, count_lines) if count_limit else count_lines

    @staticmethod
    def _build_col_mapping(raw_cols: List[str], prefix_path: int) -> List[tuple[bool, str]]:
        def shorten(col: str) -> tuple[bool, str]:
            if col.lower() == "time":
                return True, "timestamp"

            # 尝试解析COUNT类字段
            if "(" in col and ")" in col:
                start = col.index("(")
                end = col.rindex(")")
                inner = col[start + 1:end]
                if "." in inner:
                    inner_short = ".".join(inner.split(".")[-prefix_path:]) if prefix_path > 0 else inner
                    new_col = f"{col[:start + 1]}{inner_short}{col[end:]}"
                else:
                    new_col = col
            else:
                parts = col.split(".")
                new_col = ".".join(parts[-prefix_path:]) if prefix_path > 0 else col

            return False, new_col

        return [shorten(col) for col in raw_cols]

    @staticmethod
    def _build_row(record, col_mapping: List[tuple[bool, str]], use_native: bool) -> List[Any]:
        fields = record.get_fields()
        row = []
        field_idx = 0
        for is_time, _ in col_mapping:
            if is_time:
                row.append(record.get_timestamp())
            else:
                if field_idx < len(fields):
                    field = fields[field_idx]
                    row.append(
                        field.get_long_value() if use_native and field.get_data_type() == 0 else field.get_string_value())
                    field_idx += 1
                else:
                    row.append(None)
        return row

    @staticmethod
    def _adjust_batch_size_for_limit(batch_size: int, limit_size: int, context: str = "execute") -> int:
        if batch_size > limit_size:
            logging.warning(
                f"[IoTDBClient.{context}] | batch_size ({batch_size}) exceeds optimal limit ({limit_size}). "
                f"Using limit_size instead.")
            return limit_size
        return batch_size
