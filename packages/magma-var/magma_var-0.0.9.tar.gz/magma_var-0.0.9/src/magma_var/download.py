from magma_var.utils import save, transform as tf, extract as ext
from magma_var import MagmaVar
import os
import json
import pandas as pd
import requests
from typing import Self


class Download(MagmaVar):
    url_filter = "https://magma.esdm.go.id/api/v1/magma-var/filter"
    url_volcano = "https://magma.esdm.go.id/api/v1/home/gunung-api"

    def __init__(
        self,
        token: str,
        volcano_code: str,
        start_date: str,
        end_date: str,
        current_dir: str = None,
        verbose: bool = False,
        url_filter: str = None,
        url_volcano: str = None,
    ):
        super().__init__(volcano_code, start_date, end_date, current_dir, verbose)

        self.token = token
        self.url_filter = url_filter or self.url_filter
        self.url_volcano = url_volcano or self.url_volcano

        self.page_dir = os.path.join(self.json_dir, "pages", self.volcano_code)
        self.daily_dir = os.path.join(self.json_dir, "daily", self.volcano_code)

        self.json_filename = f"{self.filename}"
        self.files: list[str] = []
        self.events: list[dict[str, str]] = []
        self._df: pd.DataFrame = pd.DataFrame()

        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        if self.verbose:
            print(f"ℹ️ JSON Directory: {self.json_dir}")
            print(f"ℹ️ Volcano Directory: {self.page_dir}")

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @df.setter
    def df(self, values: list[dict[str, str]]):
        self._df = pd.DataFrame(values)

    def _download_daily(self, data: dict, overwrite: bool = False) -> None:
        """Saving daily json file

        Args:
            data (dict): Data from response['data']
            overwrite (bool, optional): Overwrite existing file. Defaults to False.

        Returns:
            None
        """
        notice_number: str = data["laporan_terakhir"]["noticenumber"]
        year = notice_number[0:4]
        month = notice_number[4:6]
        day = notice_number[6:8]
        filename = f"{year}-{month}-{day}.json"
        filepath = os.path.join(self.daily_dir, filename)

        if os.path.isfile(filepath) and not overwrite:
            if self.verbose:
                print(f"ℹ️ File Exists. Skipping: {filepath}")
            return None

        save(filepath, data)

        if self.verbose:
            print(f"🗃️ File Saved: {filepath}")

        return None

    def download_daily(self, overwrite: bool = False) -> None:
        """Download as daily json file

        Args:
            overwrite (bool, optional): Overwrite file if exists. Defaults to False.
        """
        os.makedirs(self.daily_dir, exist_ok=True)

        if self.verbose:
            print("=" * 60)
            print(f"ℹ️ Downloading first page")

        response = self.download()
        first_page_data = response["data"]

        if self.verbose:
            print(f"ℹ️ Data found : {len(first_page_data)}")
            print("=" * 60)

        for _data in first_page_data:
            self._download_daily(_data, overwrite)

        # Downloading rest of data
        last_page = response["last_page"]
        if last_page == 1:
            pass

        if self.verbose:
            print("=" * 60)
            print(f"ℹ️ Downloading from page 2 to {last_page}")
            print("=" * 60)

        for page in range(2, last_page + 1):
            response = self.download({"page": page})
            for _data in response["data"]:
                self._download_daily(_data, overwrite)

    def download(self, params: dict = None) -> dict:
        """Download VAR from Filter URL

        Args:
            params (dict): Page parameter to pass

        Returns:
            response (dict): Dictionary of response
        """
        volcano_code = self.volcano_code
        start_date = self.start_date
        end_date = self.end_date

        payload: str = json.dumps(
            {
                "code": volcano_code,
                "start_date": start_date,
                "end_date": end_date,
            }
        )

        try:
            response = requests.request(
                "GET",
                self.url_filter,
                headers=self.headers,
                data=payload,
                params=params,
            ).json()

            if "errors" in response.keys():
                raise ValueError(f'❌ Download Error :: {response["errors"]}')

            if "data" not in response.keys():
                raise KeyError(f"❌ Data not found in response :: {response}")

            if len(response["data"]) == 0:
                raise ValueError(
                    f"❌ No data found for {self.volcano_code} :: {response}"
                )

            return response
        except Exception as e:
            raise ValueError(f"❌ Failed to download JSON :: {e}")

    def download_per_page(self, response: dict) -> list[str]:
        """Download VAR per page from Filter URL

        Args:
            response (dict): Dictionary of response

        Returns:
            list of filenames
        """
        pages: list[str] = []
        last_page = response["last_page"]

        if last_page == 1:
            pass

        if self.verbose:
            print(f"ℹ️ Downloading from page 2 to {last_page}")
            print("=" * 60)

        for page in range(2, last_page + 1):
            # code_startDate_endDate_page.json
            # example: AWU_2025-01-01_2025-01-31_1.json
            filename = f"{self.json_filename}_{page}.json"
            json_per_page = os.path.join(self.page_dir, filename)

            if os.path.exists(json_per_page):
                if self.verbose:
                    print(f"✅ Skip. JSON for page #{page} exists :: {json_per_page}")
                pages.append(json_per_page)
                continue

            response = self.download({"page": page})
            save(json_per_page, response)

            pages.append(json_per_page)

            if self.verbose:
                print(f"✅ JSON for page #{page} downloaded :: {json_per_page}")
                print("=" * 60)

        self.files = self.files + pages
        return pages

    def download_first_page(self) -> dict:
        """Download first page to be used as reference and get metadata pagination

        Returns:
            response (dict): Dictionary of response
        """
        first_page_json = os.path.join(self.page_dir, f"{self.json_filename}_1.json")

        if os.path.isfile(first_page_json):
            if self.verbose:
                print(f"✅ JSON First Page exists :: {first_page_json}")
            self.files.append(first_page_json)
            return json.load(open(first_page_json))

        if self.verbose:
            print(f"⌛ Downloading JSON First Page :: {first_page_json}")

        response = self.download()

        save(first_page_json, response)

        if self.verbose:
            total = response["total"]
            print(f"ℹ️ Total Data :: {total}")
            print(f"✅ JSON First Page downloaded :: {first_page_json}")

        self.files.append(first_page_json)

        return response

    def extract(self) -> Self:
        """Extract description

        Returns:
            self: Self
        """
        self.df = ext(events=self.events, verbose=self.verbose)
        return self

    def transform(self) -> Self:
        """Transform all json files

        Returns:
            self: Self
        """
        self.events = tf(files=self.files)
        return self

    def var(self, as_daily: bool = False) -> Self:
        """Download VAR from Filter URL and save it to JSON files

        Args:
            as_daily (bool, optional): Whether to save daily json file. Defaults to False.

        Returns:
            self: Self
        """
        if as_daily:
            if self.verbose:
                print(f"ℹ️ Save VAR as daily JSON file.")
            self.download_daily(overwrite=True)
            return self

        os.makedirs(self.page_dir, exist_ok=True)

        response = self.download_first_page()
        self.download_per_page(response)

        if self.verbose:
            print("ℹ️ JSON Files :: ", len(self.files))

        self.transform().extract()

        if len(self.events) != len(self.df):
            if self.verbose:
                print(
                    f"⚠️ Events length not equal to DataFrame length :: {len(self.events)} vs {len(self.df)}"
                )
            print(f"⚠️ Please kindly to check the results.")

        return self

    def _to(
        self, filetype: str, filename: str = None, verbose: bool = True
    ) -> str | None:
        """Save wrapper

        Args:
            filetype (str): Type of wrapper. 'csv' or 'excel'
            filename (str, optional): Name of file. Defaults to None.
            verbose (bool, optional): Print verbose output. Defaults to True.

        Returns:
            Saved path location
        """
        if len(self.df) == 0:
            print(f"⚠️ No data found.")
            return None

        to_dir = os.path.join(self.magma_dir, filetype)
        os.makedirs(to_dir, exist_ok=True)

        _filename = filename if filename is not None else self.filename
        path = os.path.join(to_dir, f"{_filename}.{filetype}")

        (
            self.df.to_csv(path, index=False)
            if filetype == "csv"
            else self.df.to_excel(path, index=False)
        )

        if verbose:
            print(f"🗃️ Saved to :: {path}")

        return path

    def to_csv(self, filename: str = None, verbose: bool = True) -> str | None:
        """Save to CSV files

        Args:
            filename (str, optional): CSV filename. Defaults to None.
            verbose (bool, optional): For debugging. Defaults to True.

        Returns:
            str: CSV file location
        """
        return self._to(filetype="csv", filename=filename, verbose=verbose)

    def to_excel(self, filename: str = None, verbose: bool = True) -> str | None:
        """Save to Excel Files

        Args:
            filename (str, optional): Excel filename. Defaults to None.
            verbose (bool, optional): For debugging. Defaults to True.
        """
        return self._to(filetype="xlsx", filename=filename, verbose=verbose)
