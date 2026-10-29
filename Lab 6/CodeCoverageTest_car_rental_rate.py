import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics


def rental(**kw):
    base = {"is_confirmed": True, "vehicle_type": "economy",
            "driver_age": 30, "days": 1, "trip_segments": []}
    base.update(kw)
    return base


def test_single_economy_rental():
    r = process_rental_fleet([rental(days=2, trip_segments=[100])], 10.0)
    assert r == {"total_revenue": 110.0, "status": "STANDARD"}


def test_invalid_rentals_type():
    with pytest.raises(ValueError):
        process_rental_fleet("not a list", 10.0)


def test_negative_admin_fee():
    with pytest.raises(ValueError):
        process_rental_fleet([], -1)


def test_unconfirmed_skipped():
    r = process_rental_fleet([{"is_confirmed": False}], 10.0)
    assert r == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


def test_zero_days_flagged():
    r = process_rental_fleet([rental(days=0)], 10.0)
    assert r["status"] == "EMPTY_BATCH"


def test_luxury_rate():
    r = process_rental_fleet([rental(vehicle_type="luxury")], 10.0)
    assert r["total_revenue"] == 130.0


def test_suv_rate():
    r = process_rental_fleet([rental(vehicle_type="suv")], 10.0)
    assert r["total_revenue"] == 80.0


def test_negative_miles_flagged():
    r = process_rental_fleet([rental(trip_segments=[-5])], 10.0)
    assert r["total_revenue"] == 50.0


def test_long_trip_adult():
    r = process_rental_fleet([rental(trip_segments=[400])], 10.0)
    assert r["total_revenue"] == 210.0


def test_long_trip_underage_penalty_break():
    r = process_rental_fleet([rental(driver_age=20, trip_segments=[400, 50])], 10.0)
    assert r["total_revenue"] == 320.0


def test_young_luxury_surcharge():
    r = process_rental_fleet([rental(vehicle_type="luxury", driver_age=22, days=2)], 10.0)
    assert r["total_revenue"] == 350.0


def test_young_economy_surcharge():
    r = process_rental_fleet([rental(driver_age=22)], 10.0)
    assert r["total_revenue"] == 70.0


def test_high_risk_audit():
    r = process_rental_fleet([rental(days=0)] * 5, 10.0)
    assert r["status"] == "HIGH_RISK_AUDIT"


def test_telematics_no_data():
    assert check_fleet_telematics([]) == "NO_DATA"


def test_telematics_ground_vehicle():
    assert check_fleet_telematics([[110, 120]]) == "GROUND_VEHICLE"


def test_telematics_safe_streak_reset():
    assert check_fleet_telematics([[110, 50, 110]]) == "SAFE"