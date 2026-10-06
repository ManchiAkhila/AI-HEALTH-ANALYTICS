import pandas as pd


def detect_patterns():

    # Load health data
    data = pd.read_csv("data/health_data.csv")

    # Personal baseline
    baseline = {
        "sleep_hours": data["sleep_hours"].mean(),
        "water_liters": data["water_liters"].mean(),
        "food_quality": data["food_quality"].mean(),
        "activity_minutes": data["activity_minutes"].mean(),
        "energy_level": data["energy_level"].mean(),
        "temperature": data["temperature"].mean(),
        "heart_rate": data["heart_rate"].mean()
    }

    # Latest health record
    latest = data.iloc[-1]

    score = 0
    patterns = []

    # Check sleep
    if latest["sleep_hours"] < baseline["sleep_hours"] - 1:
        score += 1
        patterns.append("Low sleep")

    # Check water
    if latest["water_liters"] < baseline["water_liters"] - 0.5:
        score += 1
        patterns.append("Low water intake")

    # Check food
    if latest["food_quality"] < baseline["food_quality"] - 2:
        score += 1
        patterns.append("Lower food quality")

    # Check activity
    if latest["activity_minutes"] < baseline["activity_minutes"] - 15:
        score += 1
        patterns.append("Low physical activity")

    # Check energy
    if latest["energy_level"] < baseline["energy_level"] - 2:
        score += 1
        patterns.append("Low energy")

    # Check temperature
    if latest["temperature"] > baseline["temperature"] + 0.5:
        score += 1
        patterns.append("Higher temperature")

    # Check heart rate
    if latest["heart_rate"] > baseline["heart_rate"] + 15:
        score += 1
        patterns.append("Higher heart rate")

    # Check headache
    if latest["headache"] == 1:
        score += 1
        patterns.append("Headache")

    # Check pain
    if latest["pain"] > 0:
        score += 1
        patterns.append("Pain")

    print("HEALTH PATTERN ANALYSIS")
    print("-----------------------")

    print("Pattern Score:", score)

    if score == 0:
        print("Status: Normal")

    elif score <= 2:
        print("Status: Slight change detected")

    elif score <= 4:
        print("Status: Multiple changes detected")

    else:
        print("Status: Significant change detected")

    if patterns:
        print("\nDetected changes:")

        for pattern in patterns:
            print("-", pattern)

    print("\nNote: This system detects changes from the user's personal baseline.")
    print("It does not diagnose medical conditions.")


if __name__ == "__main__":
    detect_patterns()