from  qualitics.Connectors.redshift_connector import RedshiftConnector
from  qualitics.Connectors.rds_connector import RDSConnector
class ConnectorFactory:
    CONNECTOR_MAP = {
        "redshift": RedshiftConnector,
        "rds": RDSConnector
    }
    @staticmethod
    def get_connector(config: dict, usage: str = 'none'):
        if usage == 'audit':
            print("connection selected on basis of audit")
            if not config.get('audit', {}).get('enabled', False):
                print("Audit is disabled.")
                return None
            conn_config = config['audit']['database']
        else:
            print("connection selected on basis of data_source")
            conn_config = config['data_source']
        conn_type = conn_config['type']
        connector_class = ConnectorFactory.CONNECTOR_MAP.get(conn_type.lower())
        print(f'{connector_class} has been selected for {usage} based on details in config YAML.')
        if not connector_class:
            raise ValueError(f"Unsupported connector type: {conn_type}")
        return connector_class(config, usage=usage)

