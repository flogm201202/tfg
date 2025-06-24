import pandas as pd

def load_csv(path: str) -> list[str]:
    """
    Lee un archivo CSV y convierte cada fila en una string legible,
    ideal para ser usada en procesamiento semántico y vectorización.
    """
    df = pd.read_csv(path)
    filas_texto = []

    for i, row in df.iterrows():
        fila = [f"{col.strip()}: {str(val).strip()}" for col, val in row.items()]
        texto = " | ".join(fila)
        filas_texto.append(texto)

    return filas_texto
