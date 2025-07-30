from google_flights.filter import create_filter
from google_flights.flights_pb_implem import FlightData, Passengers, TFSData
from google_flights.main import get_one_way_options, get_round_trip_options
# 1) One-way, direct only, economy, specific airline (UX), single adult
flight_filter_direct_ux = create_filter(
    flight_data=[
        FlightData(
            airlines=["UX"],           # only search UX (Air Europa)
            date="2025-08-01",
            from_airport=["ORY"],
            to_airport=["BCN"],
        )
    ],
    trip="one-way",
    passengers=Passengers(adults=1, children=0, infants_in_seat=0, infants_on_lap=0),
    seat="economy",                    # direct flights only
)

# 2) Round-trip, up to 1 stop, mixed cabin: 2 adults + 1 infant on lap
flight_filter_round_family = create_filter(
    flight_data=[
        FlightData(
            date="2025-09-10",
            from_airport=["LHR"],
            to_airport=["JFK"],
        ),
        FlightData(
            date="2025-09-20",
            from_airport=["JFK"],
            to_airport=["LHR"],
        ),
    ],
    trip="round-trip",
    passengers=Passengers(adults=2, children=0, infants_in_seat=0, infants_on_lap=1),
    seat="economy",
    max_stops=1,
)

# 3) One-way, business class, children included
flight_filter_business_family = create_filter(
    flight_data=[
        FlightData(
            date="2025-10-05",
            from_airport=["MAD"],
            to_airport=["VNO"],
        )
    ],
    trip="one-way",
    passengers=Passengers(adults=2, children=2, infants_in_seat=0, infants_on_lap=0),
    seat="business",
    max_stops=2,                    # allow up to 2 stops
)

# 4) Multi-city (VNO → MAD → ORY), round-trip wrapped as two-segment round-trip
flight_filter_multi_city = create_filter(
    flight_data=[
        FlightData(
            date="2025-11-01",
            from_airport=["VNO"],
            to_airport=["MAD"],
        ),
        FlightData(
            date="2025-11-05",
            from_airport=["MAD"],
            to_airport=["ORY"],
        ),
        FlightData(
            date="2025-11-10",
            from_airport=["ORY"],
            to_airport=["VNO"],
        ),
    ],
    trip="round-trip",
    passengers=Passengers(adults=1, children=1, infants_in_seat=0, infants_on_lap=0),
    seat="economy",
    max_stops=1,
)



# Example invocation
if __name__ == "__main__":
    

    print("Direct UX one-way fares:")
    for f in get_one_way_options(flight_filter_direct_ux):
        print(f.get("url"))

    print("\nFamily round-trip fares:")
    for f in get_round_trip_options(flight_filter_round_family):
        print(f.get("url"))
    
    print("\nBusiness class family fares:")
    for f in get_one_way_options(flight_filter_business_family):
        print(f.get("url"))
    
    
