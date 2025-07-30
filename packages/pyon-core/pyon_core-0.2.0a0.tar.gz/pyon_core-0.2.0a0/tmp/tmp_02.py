import pandas as pd
import numpy as np
import pyon

# 1. Test Objects...
example_data = {

    # 1.1 Numpy Array...
    "np.ndarray": np.array([[1, 2, 3], [4, 5, 6]]),

    # 1.2 Pandas Dataframe...
    "pd.DataFrame": pd.DataFrame(
        {"col1": [1, 2], "col2": ["a", "b"]}
    ),

    # 1.3 Pandas Series...
    "pd.Series": pd.Series(
        data=[10, 20, 30],
        index=pd.date_range("2025-01-01", periods=3, freq="D"),
        name="daily_values"
    )

}

# 2. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Perform encoding and decoding...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 1.3 Print the results...
    print(f"Original:\n{value}\n")
    print(f" Decoded:\n{decoded}\n")
    print(f" Encoded: {encoded}")
    print('----------------\n')