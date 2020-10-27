import os

import requests


def get_distance(address_from: str, address_to: str, road_type: str = "fastest"):
    API_KEY = os.getenv("API_KEY")
    MILES_TO_KM_EFF = 1.609

    f_address_from = address_from.replace(" ", "+")
    f_address_to = address_to.replace(" ", "+")

    get_route = requests.get(
        f"http://www.mapquestapi.com/directions/v2/route?key={API_KEY}&"
        f"from={f_address_from}&to={f_address_to}"
        f"&outFormat=json&ambiguities=ignore&routeType={road_type}"
        f"&doReverseGeocode=false&enhancedNarrative=false&avoidTimedConditions=false"
    ).json()

    return round(float(get_route["route"]["distance"]) * MILES_TO_KM_EFF, 2)


if __name__ == "__main__":
    print(get_distance("Kraków, Czerwone Maki 49", "Kraków, Grota Roweckiego 2"))
