import json
import logging
import os
import re
from typing import Any

import psycopg2
from psycopg2 import sql


LOGGER = logging.getLogger(__name__)


def _get_database_url() -> str | None:
    return (
        os.getenv("DATABASE_URL")
        or os.getenv("RENDER_POSTGRES_URL")
        or os.getenv("POSTGRES_URL")
    )


def _sanitize_identifier(name: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", str(name).strip())
    return sanitized.lower().strip("_")


def _normalize_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (dict, list, tuple, set)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _ensure_table_and_columns(cur, table_name: str, columns: list[str]) -> None:
    table_ident = sql.Identifier(table_name)

    create_columns = [sql.SQL("id BIGSERIAL PRIMARY KEY")]
    for column in columns:
        create_columns.append(sql.SQL("{} TEXT").format(sql.Identifier(column)))
    create_columns.append(sql.SQL("created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()"))

    cur.execute(
        sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            table_ident,
            sql.SQL(", ").join(create_columns),
        )
    )

    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        """,
        (table_name,),
    )
    existing_columns = {row[0] for row in cur.fetchall()}

    for column in columns:
        if column not in existing_columns:
            cur.execute(
                sql.SQL("ALTER TABLE {} ADD COLUMN {} TEXT").format(
                    table_ident,
                    sql.Identifier(column),
                )
            )


def append_row(table_name: str, row: dict[str, Any]) -> None:
    """
    Append one row to Postgres if DATABASE_URL/RENDER_POSTGRES_URL/POSTGRES_URL is set.
    Silently skips when Postgres is not configured.
    """
    database_url = _get_database_url()
    if not database_url:
        return

    safe_table_name = _sanitize_identifier(table_name)
    if not safe_table_name:
        LOGGER.warning("Skipping Postgres write: invalid table name '%s'", table_name)
        return

    normalized_items: list[tuple[str, Any]] = []
    for raw_key, raw_value in row.items():
        safe_key = _sanitize_identifier(raw_key)
        if not safe_key:
            continue
        normalized_items.append((safe_key, _normalize_value(raw_value)))

    if not normalized_items:
        LOGGER.warning("Skipping Postgres write: row has no valid columns")
        return

    columns = [column for column, _ in normalized_items]
    values = [value for _, value in normalized_items]

    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                _ensure_table_and_columns(cur, safe_table_name, columns)

                cur.execute(
                    sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                        sql.Identifier(safe_table_name),
                        sql.SQL(", ").join(sql.Identifier(column) for column in columns),
                        sql.SQL(", ").join(sql.Placeholder() for _ in columns),
                    ),
                    values,
                )
    except Exception as exc:
        LOGGER.exception("Failed to write row to Postgres table '%s': %s", safe_table_name, exc)
