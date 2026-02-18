import bcrypt


def hash_password(plain_password: str) -> str:
    # Hash the password using bcrypt
    # plain_password is str, need to encode it to bytes.
    # encode defaults using UTF-8, which is standard for text data.
    # result of hashpw is bytes, decode it back to str for storage in the database.
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()


def is_password_valid(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
