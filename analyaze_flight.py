import os
import json
import time
import numpy as np
from collections import defaultdict

# Parameters (adjust as needed)
output_dir = "/tmp/flights1"  # Input directory for the generated flight files

def analyze_and_clean_files(input_dir):
    start_time = time.time()

    total_records = 0
    dirty_records = 0
    city_passengers_in = defaultdict(int)
    city_passengers_out = defaultdict(int)
    destination_durations = defaultdict(list)

    # Traverse the directory and process files
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    try:
                        data = json.load(f)
                        for record in data:
                            total_records += 1

                            # Check for dirty records
                            if None in record.values():
                                dirty_records += 1
                                continue

                            # Process valid records
                            origin = record["origin_city"]
                            destination = record["destination_city"]
                            duration = record["flight_duration_secs"]
                            passengers = record["num_passengers"]

                            city_passengers_out[origin] += passengers
                            city_passengers_in[destination] += passengers
                            destination_durations[destination].append(duration)
                    except json.JSONDecodeError:
                        dirty_records += 1

    # Compute statistics
    top_25_destinations = sorted(destination_durations.keys(), key=lambda x: -len(destination_durations[x]))[:25]
    avg_durations = {
        city: np.mean(destination_durations[city]) for city in top_25_destinations
    }
    p95_durations = {
        city: np.percentile(destination_durations[city], 95) for city in top_25_destinations
    }

    max_passengers_in = max(city_passengers_in.items(), key=lambda x: x[1])
    max_passengers_out = max(city_passengers_out.items(), key=lambda x: x[1])

    end_time = time.time()
    total_duration = end_time - start_time

    # Print results
    print("Analysis Results:")
    print(f"Total records processed: {total_records}")
    print(f"Dirty records: {dirty_records}")
    print(f"Total run duration: {total_duration:.2f} seconds")

    print("\nTop 25 Destination Cities:")
    for city in top_25_destinations:
        print(f"{city}: AVG={avg_durations[city]:.2f}, P95={p95_durations[city]:.2f}")

    print("\nCities with Maximum Passengers:")
    print(f"Max Passengers Arrived: {max_passengers_in[0]} ({max_passengers_in[1]})")
    print(f"Max Passengers Left: {max_passengers_out[0]} ({max_passengers_out[1]})")

# Run analysis
analyze_and_clean_files(output_dir)
