"""Data collection and synthetic dataset generation."""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

LOCATIONS = ["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad"]
PROPERTY_TYPES = ["Apartment", "Villa", "Penthouse", "Studio", "Duplex"]
FACING = ["East", "West", "North", "South", "North-East", "South-West"]

LOCATION_MULTIPLIERS = {
    "Mumbai": 1.8,
    "Delhi": 1.5,
    "Bangalore": 1.4,
    "Pune": 1.1,
    "Hyderabad": 1.0,
    "Chennai": 0.95,
    "Kolkata": 0.85,
    "Ahmedabad": 0.8,
}


def generate_synthetic_data(n_samples: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Generate realistic synthetic real estate data for training."""
    rng = np.random.default_rng(seed)

    areas = rng.integers(400, 5000, n_samples).astype(float)
    bedrooms = rng.integers(1, 6, n_samples)
    bathrooms = np.clip(bedrooms + rng.integers(-1, 2, n_samples), 1, 5)
    ages = rng.integers(0, 40, n_samples)
    floors = rng.integers(1, 25, n_samples)
    locations = rng.choice(LOCATIONS, n_samples)
    property_types = rng.choice(PROPERTY_TYPES, n_samples)
    facing = rng.choice(FACING, n_samples)

    amenities_score = rng.uniform(1, 10, n_samples)

    base_price_per_sqft = 8000
    prices = []
    for i in range(n_samples):
        loc_mult = LOCATION_MULTIPLIERS[locations[i]]
        type_mult = {"Apartment": 1.0, "Villa": 1.3, "Penthouse": 1.5, "Studio": 0.7, "Duplex": 1.2}[
            property_types[i]
        ]
        age_factor = max(0.6, 1 - ages[i] * 0.008)
        amenity_factor = 1 + (amenities_score[i] - 5) * 0.03
        bedroom_bonus = 1 + (bedrooms[i] - 2) * 0.05

        price = (
            areas[i]
            * base_price_per_sqft
            * loc_mult
            * type_mult
            * age_factor
            * amenity_factor
            * bedroom_bonus
        )
        price += rng.normal(0, price * 0.05)
        prices.append(max(price, 500000))

    df = pd.DataFrame(
        {
            "area": areas,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "age": ages,
            "floor": floors,
            "location": locations,
            "property_type": property_types,
            "facing": facing,
            "amenities_score": amenities_score,
            "price": prices,
        }
    )
    return df


def collect_data(output_path: str | Path | None = None, n_samples: int = 5000) -> pd.DataFrame:
    """Collect data from sources (simulated via synthetic generation)."""
    logger.info("Collecting data from 3 APIs + 2 databases (simulated)")
    df = generate_synthetic_data(n_samples)

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        logger.info("Saved %d records to %s", len(df), path)

    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    base = Path(__file__).resolve().parent
    collect_data(base / "raw" / "real_estate_data.csv")
