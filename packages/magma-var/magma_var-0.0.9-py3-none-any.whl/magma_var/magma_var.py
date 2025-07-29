from magma_var.utils import check_directory
import os


class MagmaVar:
    def __init__(
        self,
        volcano_code: str,
        start_date: str,
        end_date: str,
        current_dir: str = None,
        verbose: bool = False,
    ):
        self.volcano_code = volcano_code
        self.start_date = start_date
        self.end_date = end_date

        if current_dir is None:
            current_dir = os.getcwd()
        self.current_dir = current_dir

        self.output_dir, self.figures_dir, self.magma_dir = check_directory(current_dir)

        self.json_dir = os.path.join(self.magma_dir, "json")
        os.makedirs(self.json_dir, exist_ok=True)

        self.filename = f"{self.volcano_code}_{self.start_date}_{self.end_date}"

        self.verbose = verbose
