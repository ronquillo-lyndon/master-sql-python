"""
╔══════════════════════════════════════════════╗
║         SQL Practice Terminal (DuckDB)       ║
╚══════════════════════════════════════════════╝

Usage:
  Run this script to open an interactive SQL shell.
  Type SQL queries and press Enter to execute.

Special Commands:
  .datasets        -> List all available datasets
  .load <name>     -> Load a dataset (e.g: .load dataset1-1)
  .tables          -> Show tables in current session
  .schema <table>  -> Show column info for a table
  .clear           -> Clear the current session (drop all tables)
  .help            -> Show this help
  .exit / .quit    -> Exit the terminal
"""

import duckdb
import os
import glob

DATASETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "practice-activities-sql")

BANNER = """
\033[96m+------------------------------------------------------+
|      SQL Practice Terminal  *  Powered by DuckDB    |
+------------------------------------------------------+\033[0m
\033[93mType .help for commands  |  Type .datasets to see all datasets\033[0m
"""

HELP_TEXT = """
\033[1mSpecial Commands:\033[0m
  \033[92m.datasets\033[0m              -> List all available practice datasets
  \033[92m.load <dataset-name>\033[0m   -> Load a dataset into the session
                           e.g: .load dataset1-1
                           e.g: .load dataset2-5
  \033[92m.tables\033[0m                -> Show all tables in the current session
  \033[92m.schema <table>\033[0m        -> Show column details for a table
  \033[92m.clear\033[0m                 -> Clear all tables from current session
  \033[92m.help\033[0m                  -> Show this help message
  \033[92m.exit\033[0m  or  \033[92m.quit\033[0m      -> Exit the terminal

\033[1mSQL Tips:\033[0m
  * End multi-line queries with ; to execute
  * Press Ctrl+C to cancel current input
  * Use SELECT * FROM <table> to preview data
"""


def color(text, code):
    return f"\033[{code}m{text}\033[0m"


def list_datasets():
    files = sorted(glob.glob(os.path.join(DATASETS_DIR, "dataset*.sql")))
    if not files:
        print(color("  No datasets found in: " + DATASETS_DIR, "91"))
        return
    print(color("\n  Available Datasets:", "1"))
    print(color("  " + "-" * 55, "90"))
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        parts = name.split("-", 3)
        dataset_id = f"{parts[0]}-{parts[1]}"
        difficulty = parts[2].capitalize() if len(parts) > 2 else ""
        topic = parts[3].replace("-", " ").title() if len(parts) > 3 else ""
        diff_color = {"Easy": "92", "Medium": "93", "Hard": "91"}.get(difficulty, "97")
        print(f"  \033[96m{dataset_id:<14}\033[0m \033[{diff_color}m{difficulty:<8}\033[0m {topic}")
    print(color("  " + "-" * 55, "90"))
    print(color(f"  Total: {len(files)} datasets\n", "90"))


def load_dataset(conn, name):
    pattern = os.path.join(DATASETS_DIR, f"{name}*.sql")
    matches = sorted(glob.glob(pattern))

    if not matches:
        all_files = glob.glob(os.path.join(DATASETS_DIR, "*.sql"))
        matches = [f for f in all_files if name.lower() in os.path.basename(f).lower()]

    if not matches:
        print(color(f"  [ERROR] Dataset '{name}' not found. Use .datasets to list all.\n", "91"))
        return

    filepath = matches[0]
    filename = os.path.basename(filepath)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            sql = f.read()
        conn.execute(sql)
        print(color(f"  [OK] Loaded: {filename}", "92"))

        tables = conn.execute("SHOW TABLES").fetchall()
        if tables:
            table_names = [t[0] for t in tables]
            print(color(f"  Tables available: {', '.join(table_names)}", "96"))
        print()
    except Exception as e:
        print(color(f"  [ERROR] {e}\n", "91"))


def show_tables(conn):
    try:
        tables = conn.execute("SHOW TABLES").fetchall()
        if not tables:
            print(color("  (no tables -- use .load <dataset> to load one)\n", "90"))
        else:
            print(color("\n  Tables in current session:", "1"))
            for t in tables:
                print(f"  * {color(t[0], '96')}")
            print()
    except Exception as e:
        print(color(f"  [ERROR] {e}\n", "91"))


def show_schema(conn, table):
    try:
        rows = conn.execute(f"DESCRIBE {table}").fetchall()
        print(color(f"\n  Schema for '{table}':", "1"))
        print(color(f"  {'Column':<25} {'Type':<20} Null", "90"))
        print(color("  " + "-" * 52, "90"))
        for r in rows:
            col_name = r[0]
            col_type = r[1]
            nullable = r[2] if len(r) > 2 else "YES"
            print(f"  \033[96m{col_name:<25}\033[0m {col_type:<20} {nullable}")
        print()
    except Exception as e:
        print(color(f"  [ERROR] {e}\n", "91"))


def clear_session(conn):
    try:
        tables = conn.execute("SHOW TABLES").fetchall()
        for t in tables:
            conn.execute(f'DROP TABLE IF EXISTS "{t[0]}"')
        print(color("  [OK] Session cleared. All tables dropped.\n", "92"))
    except Exception as e:
        print(color(f"  [ERROR] {e}\n", "91"))


def execute_query(conn, sql):
    try:
        result = conn.execute(sql)
        rows = result.fetchall()

        if rows:
            result2 = conn.execute(sql)
            col_names = [d[0] for d in result2.description]
            rows2 = result2.fetchall()

            widths = [len(c) for c in col_names]
            for row in rows2:
                for i, val in enumerate(row):
                    widths[i] = max(widths[i], len(str(val) if val is not None else "NULL"))

            # Header
            print()
            header = "  " + "  ".join(color(c.ljust(widths[i]), "1") for i, c in enumerate(col_names))
            print(header)
            print(color("  " + "  ".join("-" * w for w in widths), "90"))

            # Rows
            for row in rows2:
                vals = []
                for i, val in enumerate(row):
                    if val is None:
                        vals.append(color("NULL".ljust(widths[i]), "90"))
                    else:
                        vals.append(str(val).ljust(widths[i]))
                print("  " + "  ".join(vals))

            print(color(f"\n  {len(rows2)} row(s)\n", "90"))
        else:
            print(color("  [OK] Query executed successfully.\n", "92"))

    except Exception as e:
        print(color(f"\n  [ERROR] {e}\n", "91"))


def main():
    print(BANNER)
    conn = duckdb.connect()
    buffer = []

    while True:
        try:
            prompt = color("sql> ", "92") if not buffer else color("  -> ", "90")
            line = input(prompt)
        except KeyboardInterrupt:
            if buffer:
                buffer = []
                print(color("\n  (input cancelled)\n", "90"))
            else:
                print(color("\n  Use .exit to quit\n", "90"))
            continue
        except EOFError:
            print()
            break

        stripped = line.strip()

        if stripped.lower() in (".exit", ".quit"):
            print(color("\n  Goodbye!\n", "96"))
            break
        elif stripped.lower() == ".help":
            print(HELP_TEXT)
        elif stripped.lower() == ".datasets":
            list_datasets()
        elif stripped.lower().startswith(".load"):
            parts = stripped.split(maxsplit=1)
            if len(parts) < 2:
                print(color("  Usage: .load <dataset-name>  (e.g: .load dataset1-1)\n", "93"))
            else:
                load_dataset(conn, parts[1])
        elif stripped.lower() == ".tables":
            show_tables(conn)
        elif stripped.lower().startswith(".schema"):
            parts = stripped.split(maxsplit=1)
            if len(parts) < 2:
                print(color("  Usage: .schema <table_name>\n", "93"))
            else:
                show_schema(conn, parts[1])
        elif stripped.lower() == ".clear":
            clear_session(conn)
        elif stripped == "":
            continue
        else:
            buffer.append(line)
            full_sql = "\n".join(buffer).strip()
            if full_sql.endswith(";"):
                execute_query(conn, full_sql)
                buffer = []


if __name__ == "__main__":
    main()
