from typing import Tuple
import os
import json
import re


def check_directory(current_dir: str) -> Tuple[str, str, str]:
    """Checking existing directory

    Args:
        current_dir (str): Current directory

    Returns:
        Tuple[str, str, str]: Directory name, directory path, and file path
    """
    output_dir = os.path.join(current_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    figures_dir = os.path.join(output_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    magma_dir = os.path.join(output_dir, "magma")
    os.makedirs(magma_dir, exist_ok=True)

    return output_dir, figures_dir, magma_dir


def transform(files: list[str], index: int = 0) -> list[dict[str, str]]:
    """Transform all json files

    Args:
        files (list[str]): list of json files
        index (int, optional): Starting index. Defaults to 0.

    Returns:
        dict[str, str]: transformed json files
    """
    events: list[dict[str, str]] = []
    for file in files:
        response = json.load(open(file))
        data = response["data"] if "data" in response.keys() else response
        for _data in data:
            notice_number: str = _data["laporan_terakhir"]["noticenumber"]
            year = notice_number[0:4]
            month = notice_number[4:6]
            day = notice_number[6:8]
            descriptions: list[str] = _data["laporan_terakhir"]["gempa"]["deskripsi"]
            for description in descriptions:
                index = index + 1
                _events: dict[str, str] = {
                    "index": int(index),
                    "date": f"{year}-{month}-{day}",
                    "event": description,
                }
                events.append(_events)

    if len(events) > 0:
        events.sort(key=lambda x: x["index"], reverse=True)

    return events


def extracted(
    date: str,
    description: str,
    event_name: str = None,
    count: int = None,
    amplitude: str = None,
    sp_time: str = None,
    duration: str = None,
    dominant: str = None,
) -> dict[str, str]:
    amp_min = None
    amp_max = amplitude
    sp_min = None
    sp_max = sp_time
    duration_min = None
    duration_max = duration

    if amplitude is not None:
        amps = amplitude.split("-")
        if len(amps) == 2:
            amp_min, amp_max = amplitude.split("-")

    if sp_time is not None:
        sp_times = sp_time.split("-")
        if len(sp_times) == 2:
            sp_min, sp_max = sp_time.split("-")

    if duration is not None:
        durations = duration.split("-")
        if len(durations) == 2:
            duration_min, duration_max = durations

    return {
        "date": date,
        "description": description,
        "event_name": event_name,
        "count": count,
        "amplitude_min": float(amp_min) if amp_min is not None else None,
        "amplitude_max": float(amp_max) if amp_max is not None else None,
        "sp_min": float(sp_min) if sp_min is not None else None,
        "sp_max": float(sp_max) if sp_max is not None else None,
        "duration_min": float(duration_min) if duration_min is not None else None,
        "duration_max": float(duration_max) if duration_max is not None else None,
        "dominant": float(dominant) if dominant is not None else None,
    }


def extract(events: list[dict[str, str]], verbose: bool = False) -> list[dict[str, str]]:
    extracted_list: list[dict[str, str]] = []

    for event in events:
        date = event["date"]
        text: str = event["event"].strip()

        name_match_pattern = r"gempa\s+(.+?)\s+dengan"
        if "Harmonik" in text:
            name_match_pattern = r"kali\s+(.+?)\s+dengan"

        count_match = re.search(r"(\d+)\s+kali", text)
        name_match = re.search(name_match_pattern, text)
        amp_match = re.search(r"amplitudo\s+([\d\-.]+)\s+mm", text)
        sp_match = re.search(r"S-P\s+([\d\-.]+)\s+detik", text)
        duration_match = re.search(r"lama\s+gempa\s+([\d\-.]+)\s+detik", text)
        dominant_match = re.search(r"dominan\s+([\d\-.]+)\s+mm", text)

        try:
            if count_match and name_match and amp_match:
                if verbose:
                    print(f'ℹ️ Found match :: {count_match} {name_match} {amp_match}')
                data = {
                    "count": int(count_match.group(1)),
                    "event_name": name_match.group(1).strip(),
                    "amplitude": amp_match.group(1),
                    "sp": sp_match.group(1) if sp_match else None,
                    "duration": duration_match.group(1) if duration_match else None,
                    "dominant": dominant_match.group(1) if dominant_match else None,
                }

                extracted_list.append(
                    extracted(
                        date=date,
                        description=text,
                        event_name=data["event_name"],
                        count=int(data["count"]),
                        amplitude=data["amplitude"],
                        sp_time=data["sp"],
                        duration=data["duration"],
                        dominant=data["dominant"],
                    )
                )
            else:
                if verbose:
                    print(f'⚠️ No found match {text} :: {count_match} || {name_match} || {amp_match}')
                extracted_list.append(
                    extracted(
                        date=date,
                        description=text,
                    )
                )
        except Exception as e:
            print(f"❌ Cannot extract of date {date} :: {text}")
            print(e)
            continue

    return extracted_list


def save(filename: str, response: dict) -> str:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

    return filename
