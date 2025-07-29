# your_package_name/gupta_heuristic.py
import pandas as pd
import argparse # Importar argparse
import os       # Importar os para verificar la existencia del archivo
from typing import List, Dict, Tuple, Literal

def calculate_gupta_index(processing_times: pd.Series) -> float:
    """
    Calculates the Gupta index for a single job.
    ... (rest of your code)
    """
    m = len(processing_times)
    if m < 2:
        raise ValueError("Gupta's heuristic requires at least 2 machines.")

    numerator_sum = 0.0
    for k in range(1, m):
        numerator_sum += 1 / (processing_times.iloc[k-1] + processing_times.iloc[k])

    e_j: Literal[-1, 1]
    if processing_times.iloc[0] < processing_times.iloc[m-1]:
        e_j = -1
    else:
        e_j = 1

    s_j = e_j / numerator_sum
    return s_j

def gupta_heuristic(df: pd.DataFrame) -> List[int]:
    """
    Applies Gupta's heuristic to sequence jobs in a Flow Shop problem.
    ... (rest of your code)
    """
    df = df.set_index('Job')

    gupta_indices: Dict[int, float] = {}
    for job_id, row in df.iterrows():
        processing_times_for_job = row.squeeze()
        gupta_indices[job_id] = calculate_gupta_index(processing_times_for_job)

    sorted_jobs: List[Tuple[float, float, int]] = []
    for job_id, gupta_index in gupta_indices.items():
        total_processing_time = df.loc[job_id].sum()
        sorted_jobs.append((gupta_index, total_processing_time, job_id))

    sorted_jobs.sort()

    return [job_id for _, _, job_id in sorted_jobs]

def calculate_cmax(original_df: pd.DataFrame, sequence: List[int]) -> int:
    """
    Calculates the makespan (C_max) for a given job sequence.
    ... (rest of your code)
    """
    df = original_df.set_index('Job').copy()
    num_jobs = len(sequence)
    num_machines = df.shape[1]

    completion_times: List[List[int]] = [[0] * num_machines for _ in range(num_jobs)]

    for i, job_id in enumerate(sequence):
        for j in range(num_machines):
            processing_time = df.loc[job_id].iloc[j]

            if i == 0 and j == 0:
                completion_times[i][j] = processing_time
            elif i == 0:
                completion_times[i][j] = completion_times[i][j-1] + processing_time
            elif j == 0:
                completion_times[i][j] = completion_times[i-1][j] + processing_time
            else:
                completion_times[i][j] = max(completion_times[i-1][j], completion_times[i][j-1]) + processing_time

    return completion_times[num_jobs-1][num_machines-1]

# Elimina la función `main()` y el bloque `if __name__ == "__main__":`
# Esto es porque el paquete será importado, no ejecutado directamente como un script.
# Si quieres una interfaz de línea de comandos, usa 'console_scripts' en pyproject.toml.

# Dentro de gupta_heuristic.py, después de las otras funciones
def main_cli() -> None:
    """
    Main function for command-line execution of Gupta's heuristic.
    Accepts an input file name as an argument, with a default value.
    """
    parser = argparse.ArgumentParser(
        description="Aplica la heurística de Gupta para secuenciar tareas en un Flow Shop."
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="gupta_data.csv", # Nombre de archivo por defecto
        help="Ruta al archivo de entrada (CSV o Excel). Por defecto: gupta_data.csv"
    )

    args = parser.parse_args()
    input_file_path = args.input

    # Determinar el tipo de archivo y la función de lectura
    if input_file_path.endswith('.csv'):
        read_func = pd.read_csv
    elif input_file_path.endswith('.xlsx') or input_file_path.endswith('.xls'):
        read_func = pd.read_excel
    else:
        print(f"Error: Tipo de archivo no soportado para '{input_file_path}'. Use .csv o .xlsx/.xls.")
        return

    # Verificar si el archivo existe
    if not os.path.exists(input_file_path):
        print(f"Error: El archivo '{input_file_path}' no fue encontrado.")
        print("Asegúrese de que el archivo esté en el directorio actual o proporcione la ruta completa.")
        return

    try:
        print(f"Intentando leer datos de {input_file_path}")
        df = read_func(input_file_path)
        print("Original Processing Times:")
        print(df)
        print("-" * 30)

        job_sequence = gupta_heuristic(df.copy())
        print(f"Job Sequence according to Gupta's Heuristic: {job_sequence}")
        print("-" * 30)

        c_max = calculate_cmax(df.copy(), job_sequence)
        print(f"Calculated C_max for the sequence: {c_max}")

    except Exception as e:
        print(f"An error occurred: {e}")