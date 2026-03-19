"""Password security with bcrypt hashing."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash password with bcrypt and cryptographic salt.
    
    Args:
        password: Plain text password
        
    Returns:
        Bcrypt hashed password bytes
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password: str, hashed_password: bytes) -> bool:
    """Verify password against bcrypt hash.
    
    Args:
        password: Plain text password to verify
        hashed_password: Bcrypt hash to verify against
        
    Returns:
        True if password matches hash, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)