class InvalidCountryError(LookupError):
    def __init__(self, received_country: str):
        self.received_country = received_country

    def __str__(self):
        return f"Country '{self.received_country}' is not a valid country"

