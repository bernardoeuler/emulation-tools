import uuid

def generate_public_id() -> str:
    return uuid.uuid4().hex