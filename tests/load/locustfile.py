import os
import random
from uuid import uuid4

from locust import HttpUser, between, task
from locust.exception import StopUser


class MovieApiUser(HttpUser):
    wait_time = between(0.2, 1.0)

    def on_start(self) -> None:
        self.full_profile = os.getenv("LOAD_PROFILE", "full") == "full"
        self.showtime_id = None
        if self.full_profile:
            credentials = {"email": f"load-{uuid4().hex}@example.com", "password": "LoadTest123!"}
            with self.client.post(
                "/auth/register", json=credentials, name="POST /auth/register", catch_response=True
            ) as response:
                if response.status_code != 201:
                    response.failure(f"Register failed: {response.status_code}")
                    raise StopUser
            with self.client.post(
                "/auth/login", json=credentials, name="POST /auth/login", catch_response=True
            ) as response:
                if response.status_code != 200 or not response.json().get("access_token"):
                    response.failure(f"Login failed: {response.status_code}")
                    raise StopUser
                self.client.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
        with self.client.get("/showtimes", name="GET /showtimes", catch_response=True) as response:
            if response.status_code != 200 or not response.json().get("items"):
                response.failure("No showtimes available; seed data and finish the feature first")
                raise StopUser
            self.showtime_id = response.json()["items"][0]["id"]

    @task(5)
    def list_movies(self) -> None:
        with self.client.get("/movies", name="GET /movies", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status {response.status_code}")

    @task(3)
    def list_showtimes(self) -> None:
        with self.client.get("/showtimes", name="GET /showtimes", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status {response.status_code}")

    @task(2)
    def list_seats(self) -> None:
        self.client.get(
            f"/showtimes/{self.showtime_id}/seats", name="GET /showtimes/{showtime_id}/seats"
        )

    @task(2)
    def list_my_bookings(self) -> None:
        if self.full_profile:
            self.client.get("/bookings/me", name="GET /bookings/me")

    @task(1)
    def booking_lifecycle(self) -> None:
        if not self.full_profile:
            return
        seats = self.client.get(
            f"/showtimes/{self.showtime_id}/seats", name="GET /showtimes/{showtime_id}/seats"
        )
        if seats.status_code != 200:
            return
        available = [seat for seat in seats.json()["items"] if seat["status"] == "AVAILABLE"]
        if not available:
            return
        payload = {"showtime_id": self.showtime_id, "seat_id": random.choice(available)["id"]}
        with self.client.post(
            "/bookings", json=payload, name="POST /bookings", catch_response=True
        ) as response:
            if (
                response.status_code == 409
                and response.json().get("error", {}).get("code") == "SEAT_ALREADY_BOOKED"
            ):
                # A competing user won this seat; this is expected business contention.
                response.success()
                return
            if response.status_code != 201:
                response.failure(f"Booking failed: {response.status_code}")
                return
            booking_id = response.json()["id"]
        try:
            self.client.get(f"/bookings/{booking_id}", name="GET /bookings/{booking_id}")
        finally:
            with self.client.delete(
                f"/bookings/{booking_id}", name="DELETE /bookings/{booking_id}", catch_response=True
            ) as response:
                if response.status_code != 204:
                    response.failure(f"Cancel failed: {response.status_code}")
