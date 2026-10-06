import pandas as pd


def calculate_baseline():
    # Load health data
    data = pd.read_csv("data/health_data.csv")

    # Calculate personal baseline
    baseline = {
        "sleep_hours": data["sleep_hours"].mean(),
        "water_liters": data["water_liters"].mean(),
        "food_quality": data["food_quality"].mean(),
        "activity_minutes": data["activity_minutes"].mean(),
        "energy_level": data["energy_level"].mean(),
        "temperature": data["temperature"].mean(),
        "heart_rate": data["heart_rate"].mean()
    }

    return baseline


if __name__ == "__main__":
    baseline = calculate_baseline()

    print("PERSONAL HEALTH BASELINE")
    print("------------------------")

    for parameter, value in baseline.items():
        print(f"{parameter}: {value:.2f}")