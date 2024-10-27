class User:
    """The User class represents a generic user within the application, encapsulating basic attributes 
    such as the user's ID and email. It provides methods for converting user data to 
    a dictionary format and creating a User instance from a dictionary.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The email address of the user.

    Methods:
        to_dict(): Converts the User instance into a dictionary representation.
        from_dict(data): A class method that creates a User instance from a dictionary containing user data."""
    
    def __init__(self, id, email):
        self.id = id
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["email"])
