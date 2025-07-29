import json
from pathlib import Path
from typing import List

THIS_DIR = Path(__file__).parent
# Adjusted path for cities.json to be in the same directory as the script
# If cities.json is truly in the parent directory, your original path is fine.
# I'm assuming it's in the same directory for simplicity here,

CITIES_JSON_FPATH = THIS_DIR / "./cities.json"


def is_city_capitol_of_state(city_name: str, state_name: str) -> bool:
    """
    Check if the given city is the capital of the specified state.

    Args:
        city_name (str): The name of the city.
        state_name (str): The name of the state.

    Returns:
        bool: True if the city is the capital of the state, False otherwise.
    """
    try:
        cities_json_content = CITIES_JSON_FPATH.read_text(encoding="utf-8")
        cities: List[dict] = json.loads(cities_json_content)
    except FileNotFoundError:
        print(f"Error: cities.json not found at {CITIES_JSON_FPATH}")
        return False
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {CITIES_JSON_FPATH}")
        return False

    for city_data in cities:
        if city_data["city"] == city_name and city_data["state"]:
            return True
    return False


if __name__ == "__main__":

    print(f"{is_city_capitol_of_state('Bismarck', 'North Dakota')}")
    print(f"{is_city_capitol_of_state('Phoenix', 'Arizona')}")
    print(f"{is_city_capitol_of_state('New York', 'New York')}")
    print(f"{is_city_capitol_of_state('Springfield', 'Illinois')}")
    print(f"{is_city_capitol_of_state('NonExistentCity', 'SomeState')}")
    print(f"{is_city_capitol_of_state('Chicago', 'Illinois')}")
