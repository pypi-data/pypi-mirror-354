import tempfile
import unittest

import pandas as pd
from lstchain.io.io import dl2_params_lstcam_key

from gammalearn.data.save_results.write_dl2_files import write_dl2_dataframe


class TestWrite(unittest.TestCase):
    def test_write_dl2_dataframe(self):
        data = {"col1": [1, 2, 3], "col2": [4.0, 5, 6]}
        df = pd.DataFrame(data)

        # Write the DataFrame to a temporary file and read back
        with tempfile.NamedTemporaryFile() as f:
            output_path = f.name
            write_dl2_dataframe(df, output_path)
            df_read = pd.read_hdf(output_path, key=dl2_params_lstcam_key)
            self.assertTrue(df.equals(df_read))
