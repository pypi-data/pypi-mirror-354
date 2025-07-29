from magma_var.magma_var import MagmaVar
from magma_var.utils import transform, extract
from glob import glob
import os
import pandas as pd


class JsonVar(MagmaVar):
    def __init__(
        self,
        volcano_code: str,
        start_date: str,
        end_date: str,
        current_dir: str = None,
        verbose: bool = False,
    ):
        super().__init__(volcano_code, start_date, end_date, current_dir, verbose)
        self.files: list[str] = []
        self._df: pd.DataFrame = pd.DataFrame()

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @df.setter
    def df(self, values: list[dict[str, str]]):
        self._df = pd.DataFrame(values)

    def get(self, from_daily: bool = False):
        _subdir = "daily" if from_daily is True else "pages"
        volcano_json_dir = os.path.join(self.json_dir, _subdir, self.volcano_code)

        if self.verbose:
            print(f"ℹ️ Looking JSON files in : {volcano_json_dir}")

        self.files = glob(os.path.join(volcano_json_dir, "*.json"))

        if len(self.files) == 0:
            raise FileNotFoundError(
                f"⚠️ JSON files not found in {volcano_json_dir}. "
                f"Try to download them manually."
            )

        if self.verbose:
            print(f"ℹ️ Total JSON files :: {len(self.files)}")
            print("=" * 60)

        self.df = extract(events=transform(files=self.files))
