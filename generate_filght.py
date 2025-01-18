import os
import json
import random
from datetime import datetime, timedelta

# Parameters
N = 5000  # Total number of JSON files to generate
M_min, M_max = 50, 100  # Size of each JSON array (number of records per file)
L_min, L_max = 0.005, 0.001  # Probability of NULL in any property
output_dir = "tmp/flights1"

# Expanded list of cities
cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "San Francisco", "Indianapolis", "Columbus", "Fort Worth", "Charlotte",
    "Detroit", "El Paso", "Seattle", "Denver", "Washington",
    "Boston", "Memphis", "Nashville", "Portland", "Oklahoma City",
    "Las Vegas", "Louisville", "Baltimore", "Milwaukee", "Albuquerque",
    "Tucson", "Fresno", "Mesa", "Sacramento", "Kansas City",
    "Atlanta", "Long Beach", "Colorado Springs", "Raleigh", "Miami",
    "Virginia Beach", "Omaha", "Oakland", "Minneapolis", "Tulsa",
    "Arlington", "New Orleans", "Wichita", "Cleveland", "Tampa",
    "Bakersfield", "Aurora", "Honolulu", "Anaheim", "Santa Ana",
    "Corpus Christi", "Riverside", "Lexington", "Henderson", "Stockton",
    "St. Paul", "Cincinnati", "St. Louis", "Pittsburgh", "Greensboro",
    "Lincoln", "Anchorage", "Plano", "Orlando", "Irvine"
]

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def random_date():
    """Generate a random date within the last year."""
    start_date = datetime.now() - timedelta(days=365)
    random_days = random.randint(0, 365)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def random_flight_record():
    """Generate a random flight record."""
    record = {
        "date": random_date(),
        "origin_city": random.choice(cities),
        "destination_city": random.choice(cities),
        "flight_duration_secs": random.randint(1800, 14400),  # 30 mins to 4 hours
        "num_passengers": random.randint(1, 300)  # 1 to 300 passengers
    }
    
    # Introduce NULL values with probability L
    if random.random() < random.uniform(L_min, L_max):
        record[random.choice(list(record.keys()))] = None
    
    return record

# Generate JSON files
for i in range(N):
    origin_city = random.choice(cities)
    folder_name = os.path.join(output_dir, f"{datetime.now().strftime('%m-%y')}-{origin_city}")
    os.makedirs(folder_name, exist_ok=True)

    file_name = os.path.join(folder_name, f"flights-{i}.json")
    
    # Generate random number of flight records
    flight_count = random.randint(M_min, M_max)
    flight_data = [random_flight_record() for _ in range(flight_count)]

    # Save to file
    with open(file_name, "w") as f:
        json.dump(flight_data, f, indent=4)

print(f"Generated {N} JSON files in {output_dir}")
