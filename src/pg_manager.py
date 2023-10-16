import random
import string

class PGManager:
    
    def __init__(self):
        self.existing_usernames = set()
    
    def _generate_password(self, password_length=12):
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(password_length))

    def _generate_unique_username(self, prefix="RM-PG", length=5):
        """Generate a unique username with a given prefix and random number length."""
        max_tries = 1000  # Max number of attempts to find a unique username
        for _ in range(max_tries):
            random_number = ''.join(random.choice(string.digits) for _ in range(length))
            username = f"{prefix}{random_number}"
            if username not in self.existing_usernames:
                self.existing_usernames.add(username)
                return username
        raise ValueError("Failed to generate a unique username. Increase the random number length or change the prefix.")
    
    
    def create_pg_credentials(self):
        """Create PostgreSQL username and password."""
        # Generate unique username
        username = self._generate_unique_username()
        
        # Generate password
        password = self._generate_password()

        
        return username, password 
