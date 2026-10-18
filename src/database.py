"""SQLite ingestion and read-only summary checks for original observations."""
import argparse
import sqlite3
from .config import DATABASE, ROOT, create_output_dirs
from .data import load_data

SQL_FIELDS = ['udi', 'product_id', 'product_type', 'air_temperature_k', 'process_temperature_k',
              'rotational_speed_rpm', 'torque_nm', 'tool_wear_min', 'machine_failure',
              'twf', 'hdf', 'pwf', 'osf', 'rnf']


def initialise_database():
    df = load_data()
    create_output_dirs()
    with sqlite3.connect(DATABASE) as conn:
        conn.executescript((ROOT / 'sql' / 'schema.sql').read_text(encoding='utf-8'))
        # Replace only the derived table contents, never the source CSV.
        conn.execute('DELETE FROM machine_observations')
        values = [tuple(None if __import__('pandas').isna(v) else v.item() if hasattr(v, 'item') else v
                        for v in row) for row in df.itertuples(index=False, name=None)]
        sql = 'INSERT INTO machine_observations (' + ','.join(SQL_FIELDS) + ') VALUES (' + ','.join(['?'] * len(SQL_FIELDS)) + ')'
        conn.executemany(sql, values)
        total, failures, distinct_udis = conn.execute(
            'SELECT COUNT(*), SUM(machine_failure), COUNT(DISTINCT udi) FROM machine_observations').fetchone()
        assert total == len(df) == distinct_udis
        assert failures == int(df['Machine failure'].sum())
    print(f'SQLite ready: {DATABASE}; rows={total}; failures={failures}')


def show_summary():
    if not DATABASE.exists():
        raise FileNotFoundError(f'No SQLite database at {DATABASE}; run --init first.')
    with sqlite3.connect(DATABASE) as conn:
        for record in conn.execute('SELECT product_type, COUNT(*), SUM(machine_failure), '
                                   'ROUND(100.0*AVG(machine_failure), 2) '
                                   'FROM machine_observations GROUP BY product_type ORDER BY product_type'):
            print('Type, observations, failures, failure %:', record)


def main():
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--init',action='store_true')
    group.add_argument('--summary',action='store_true')
    args=parser.parse_args()
    if args.init:initialise_database()
    else:show_summary()

if __name__=='__main__':main()
