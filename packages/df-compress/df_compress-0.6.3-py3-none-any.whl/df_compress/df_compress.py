import pandas as pd
import numpy as np

def compress(df, convert_strings=True, numeric_threshold=0.999, show_conversions=False) -> pd.DataFrame:
    """
    Compress DataFrame by:
    - Downcasting numeric types
    - Converting object types to categories
    - Optionally converting strings to numeric types if a % are numeric
    
    Parameters:
    - convert_strings (bool): attempt to parse object columns as numbers
    - numeric_threshold (float): proportion of valid numeric entries needed to convert (0.0 - 1.0)
    - show_conversions (bool): whether to report the changes made column by column

    Returns:
    - Compressed DataFrame (in place)
    """

    start_mem = df.memory_usage(deep=True).sum() / 1024**2
    print(f"Initial memory usage: {start_mem:.2f} MB")

    changes = []

    for col in df.columns:
        col_data = df[col]
        old_dtype = col_data.dtype
        old_mem = col_data.memory_usage(deep=True)
        new_data = col_data.copy()

        if pd.api.types.is_object_dtype(old_dtype):
            # Attempt numeric conversion if enabled
            if convert_strings:
                temp = pd.to_numeric(new_data, errors='coerce')
                if temp.notna().mean() >= numeric_threshold:
                    new_data = temp

            # If still object, consider converting to category
            if pd.api.types.is_object_dtype(new_data.dtype):
                if new_data.nunique() / len(new_data) < 0.5:
                    new_data = new_data.astype('category')

        # Downcast numeric types
        if pd.api.types.is_integer_dtype(new_data):
            # Downcast interger types
            new_data = pd.to_numeric(new_data, downcast='integer')
        elif pd.api.types.is_float_dtype(new_data):
            # Attempt to downcast float types to integers, if no information is lost. Otherwise, keep as float
            if np.all(np.isclose(new_data.dropna() % 1, 0)):
                new_data = pd.to_numeric(new_data, downcast='integer')
            else:
                new_data = pd.to_numeric(new_data, downcast='float')

        new_dtype = new_data.dtype
        new_mem = new_data.memory_usage(deep=True)

        if new_dtype != old_dtype:
            changes.append({
                "column": col,
                "from": str(old_dtype),
                "to": str(new_dtype),
                "memory saved (MB)": (old_mem - new_mem) / 1024**2
            })

        df[col] = new_data

    end_mem = df.memory_usage(deep=True).sum() / 1024**2
    print(f"Final memory usage: {end_mem:.2f} MB")
    print(f"Memory reduced by: {start_mem - end_mem:.2f} MB ({100 * (start_mem - end_mem) / start_mem:.1f}%)\n")

    if show_conversions==True:
        if changes:
            print("Variable type conversions:")
            print(pd.DataFrame(changes).to_string(index=False))
        else:
            print("No conversions were applied.")

    return df