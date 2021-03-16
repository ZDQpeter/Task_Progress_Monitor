import pandas as pd

def function_Save_Data_Matrix_into_CSV(data_matrix, Path):

    data_matrix_df = pd.DataFrame(data_matrix)
    data_matrix_df.to_csv(Path, header=False, index=False)

    return