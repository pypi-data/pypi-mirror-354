from sqlalchemy import Table, Integer, String, DateTime, Boolean, Float, Date, Text, Numeric


def entity_by_table(base, connection, table_name):
    """
    Reflete uma tabela existente no banco, na conexão fornecida.\n
    Gera uma entidade SQLAlchemy com mapeamento automático de tipos.

    Args:
        base: Base declarativa do SQLAlchemy
        connection: Conexão com o banco de dados
        table_name: Nome da tabela a ser refletida

    Returns:
        Dicionário com informações da tabela e código da classe
    """
    type_mapping = {
        'integer': (Integer, {"primary_key": True, "autoincrement": True}),
        'bigint': (Integer, {}),
        'smallint': (Integer, {}),
        'string': (String, {}),
        'text': (Text, {}),
        'varchar': (String, {}),
        'datetime': (DateTime, {}),
        'timestamp': (DateTime, {}),
        'boolean': (Boolean, {}),
        'bool': (Boolean, {}),
        'float': (Float, {}),
        'real': (Float, {}),
        'numeric': (Numeric, {}),
        'decimal': (Numeric, {}),
        'date': (Date, {})
    }

    some_table = Table(
        table_name,
        base.metadata,
        autoload_with=connection.get_engine()
    )

    # Extrai tipos de colunas
    dict_table = {
        col.name: col.type.__visit_name__.lower()
        for col in some_table.c
    }

    # Gera código da classe com importações
    class_code = f"""from sqlalchemy import {', '.join(set(
        type_mapping.get(col_type, (String,))[0].__name__ 
        for col_type in dict_table.values()
    ))}
from sqlalchemy.orm import mapped_column

class {table_name.replace('_', '').capitalize()}(Base):
    __tablename__ = "{table_name}"

"""

    for col_name, col_type in dict_table.items():
        # Obtém o tipo e opções padrão
        column_type, default_options = type_mapping.get(col_type, (String, {}))

        # Formata as opções
        options_str = ', '.join(f"{k}={v}" for k, v in default_options.items())

        # Adiciona a coluna ao código
        if options_str:
            class_code += f"    {col_name} = mapped_column({column_type.__name__}, {options_str})\n"
        else:
            class_code += f"    {col_name} = mapped_column({column_type.__name__})\n"

    return {
        'table_info': dict_table,
        'class_code': class_code
    }


def entity_by_dataframe(df, table_name='GeneratedTable'):
    """
    Gera uma entidade SQLAlchemy a partir de um DataFrame pandas.
    
    Args:
        df (pd.DataFrame): DataFrame de origem
        table_name (str): Nome da tabela a ser gerada
    
    Returns:
        dict: Dicionário com informações da tabela e código da classe
    """
    # Mapeamento de tipos pandas para SQLAlchemy
    type_mapping = {
        'int64': (Integer, {}),
        'int32': (Integer, {}),
        'float64': (Float, {}),
        'float32': (Float, {}),
        'bool': (Boolean, {}),
        'datetime64[ns]': (DateTime, {}),
        'object': (String, {}),
        'string': (String, {})
    }
    
    # Extrai tipos de colunas do DataFrame
    dict_table = {
        col: str(df[col].dtype)
        for col in df.columns
    }
    
    # Gera código da classe com importações
    class_code = f"""from sqlalchemy import {', '.join(set(
        type_mapping.get(col_type, (String,))[0].__name__ 
        for col_type in dict_table.values()
    ))}
from sqlalchemy.orm import mapped_column

class {table_name.replace('_', '').capitalize()}(Base):
    __tablename__ = "{table_name}"

"""
    
    # Adiciona colunas dinamicamente
    for col_name, col_type in dict_table.items():
        # Obtém o tipo e opções padrão
        column_type, default_options = type_mapping.get(col_type, (String, {}))
        
        # Formata as opções
        options_str = ', '.join(f"{k}={v}" for k, v in default_options.items())
        
        # Adiciona a coluna ao código
        if options_str:
            class_code += f"    {col_name} = mapped_column({column_type.__name__}, {options_str})\n"
        else:
            class_code += f"    {col_name} = mapped_column({column_type.__name__})\n"

    return {
        'table_info': dict_table,
        'class_code': class_code
    }