import orjson
from pathlib import Path
import polars as pl
from colorama import Fore
from tqdm import tqdm


def write_orjson(data, path: Path, file_name: str):
    # config
    json_options = orjson.OPT_NAIVE_UTC | orjson.OPT_INDENT_2
    json_bytes = orjson.dumps(data, option=json_options)

    # export
    path.mkdir(parents=True, exist_ok=True)
    (path / f"{file_name}.json").write_bytes(json_bytes)


class JsonToDataFrame:
    def __init__(self, files: list[Path]):
        self.files = files
        self.df_json = None
        print(f"{Fore.BLUE}[JSON -> DataFrame]{Fore.RESET}")

    def parse_and_collect(self, str_list: list[str]) -> list[dict]:
        parsed_list = []
        for s in tqdm(str_list, desc="[JSON] Parsing"):
            if isinstance(s, list):
                s = s[0]
            start = s.find("{")
            end = s.rfind("}") + 1
            if start != -1 and end != 0:
                try:
                    parsed_list.append(orjson.loads(s[start:end]))
                except orjson.JSONDecodeError:
                    parsed_list.append({})
        return parsed_list

    def wrap_values_in_list(self, item: dict) -> dict:
        for key, value in item.items():
            if not isinstance(value, list):
                item[key] = [value]
            else:
                item[key] = [
                    item
                    for sublist in value
                    if sublist
                    for item in (sublist if isinstance(sublist, list) else [sublist])
                ]
        return item

    def load_json_to_list(self, col: str = "response") -> pl.DataFrame:
        # load
        lst = [
            orjson.loads(open(str(i), "r").read())
            for i in tqdm(self.files, desc="[JSON] Loading in folder")
        ]
        lst = sum(lst, [])
        df_json = pl.DataFrame(lst)

        # json -> dict
        lst_response = self.parse_and_collect(df_json[col].to_list())
        lst_response = [self.wrap_values_in_list(i) for i in lst_response]

        df_response = pl.DataFrame(lst_response, strict=False)
        df_process = pl.concat([df_json.drop([col]), df_response], how="horizontal")
        return df_process


def md_file_read_write(path: Path, data: str = None):
    """Read prompt file."""
    if not data:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
            print(f"File written to: {path}")
            return None
