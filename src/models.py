
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    email: str = ""

@dataclass
class Movie:
    id: Optional[int] = None
    title: str = ""
    year: int = 0
    language: str = ""
    
@dataclass
class Staff:
    id: Optional[int] = None
    name: str = ""
    birth_country: str = ""
    role: str = ""
    is_alive: bool = True
    
@dataclass
class Nomination:
    id: Optional[int] = None
    staff_id: int = 0
    movie_id: int = 0
    category: str = ""
    year: int = 0
    
@dataclass
class Oscar(Nomination):
    """Oscar win extends nomination with the same fields"""
    pass

@dataclass
class UserNomination:
    id: Optional[int] = None
    user_id: int = 0
    staff_id: int = 0
    movie_id: int = 0
    category: str = ""
