def get_profiling_config(config):
    """Resolves the database and schema from config - checks profiling.profiling_database and profiling.profiling_schema"""
    profiling_config = config.get('profiling', {})
    if not profiling_config or not isinstance(profiling_config, dict):
        raise ValueError("Profiling configuration is missing or invalid")

    if 'profiling_database' not in profiling_config:
        raise ValueError("No database specified in config. Define 'profiling.profiling_database'")

    if 'profiling_schema' not in profiling_config:
        raise ValueError("No schema specified in config. Define 'profiling.profiling_schema'")

    return {
        'database': profiling_config['profiling_database'],
        'schema': profiling_config['profiling_schema']
    }


def run_profiling(profiler, config):
    """Executes profiling with configuration from YAML"""
    profiling_info = get_profiling_config(config)
    database = profiling_info['database']
    schema = profiling_info['schema']

    profiling_config = config.get('profiling', {})

    # Get tables (support both string and list)
    tables = None
    if 'table' in profiling_config:
        tables = [profiling_config['table']]
    elif 'table_list' in profiling_config:
        tables = profiling_config['table_list']

    # Get columns (support both string and list)
    columns = None
    if 'column' in profiling_config:
        columns = [profiling_config['column']]
    elif 'column_list' in profiling_config:
        columns = profiling_config['column_list']

    # Prepare arguments with mandatory database and schema
    profile_args = {
        'database': database,
        'schema': schema
    }
    if tables:
        profile_args['tables'] = tables
    if columns:
        profile_args['columns'] = columns

    return profiler.profile(**profile_args)