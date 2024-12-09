from builtins import str
import random


def generate_nickname() -> str:
    """Generate a URL-safe nickname using verbs, nouns, and a number."""
    verbs = ["jumping", "running", "flying", "dancing", "swimming"]
    nouns = ["tiger", "eagle", "whale", "dolphin", "dragon"]
    number = random.randint(100, 999)  # Use a wider range for more uniqueness

    # Use hyphens instead of underscores for URL-friendliness and readability
    return f"{random.choice(verbs)}-{random.choice(nouns)}-{number}"
