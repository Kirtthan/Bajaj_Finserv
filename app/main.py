# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List
import os
import re


# ===============================
# Config (adjust or set via env)
# ===============================
FULL_NAME_LOWER = os.getenv("FULL_NAME_LOWER", "john_doe")  # lowercase with underscores
DOB_DDMMYYYY = os.getenv("DOB_DDMMYYYY", "17091999")        # ddmmyyyy
EMAIL = os.getenv("EMAIL", "john@xyz.com")
ROLL_NUMBER = os.getenv("ROLL_NUMBER", "ABCD123")


# =====================
# FastAPI + middleware
# =====================
app = FastAPI(title="BFHL API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Utilities / Core Business
# =========================
INT_RE = re.compile(r"^[+-]?\d+$")  # strict integer, supports +/-


def is_integer_string(token: str) -> bool:
    return bool(INT_RE.match(token))


def classify_and_compute(data: List[Any]) -> Dict[str, Any]:
    """
    Classify tokens & compute required outputs.

    - Numbers: tokens matching integer regex. Return as strings in odd/even lists; sum as string.
    - Alphabets: tokens with only letters. Return UPPERCASE tokens.
    - Special characters: everything else (including mixed alnum like 'abc123', punctuation, empty).
    - concat_string: take *all alphabetic characters* across tokens, reverse, then alternating caps
      starting with UPPER (index 0 upper, 1 lower, ...).
    """
    tokens: List[str] = [str(x).strip() for x in (data or [])]

    odd_numbers: List[str] = []
    even_numbers: List[str] = []
    alphabets: List[str] = []
    special_characters: List[str] = []
    alpha_chars: List[str] = []       # for concat_string characters
    numeric_values: List[int] = []

    for tok in tokens:
        if tok == "":
            # Treat empty as special
            special_characters.append(tok)
        elif is_integer_string(tok):
            # numeric
            try:
                val = int(tok)
            except ValueError:
                # extremely defensive; regex ensures val is int-like
                special_characters.append(tok)
            else:
                numeric_values.append(val)
                (even_numbers if val % 2 == 0 else odd_numbers).append(tok)
        elif tok.isalpha():
            # pure letters token
            alphabets.append(tok.upper())
        else:
            # mixed or symbol
            special_characters.append(tok)

        # collect alphabetic characters (for concat_string)
        for ch in tok:
            if ch.isalpha():
                alpha_chars.append(ch)

    total_sum_str = str(sum(numeric_values))

    # concat_string: reversed letters, alternating caps (Upper, lower, ...)
    rev_chars = list(reversed(alpha_chars))
    alt_cased = [c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(rev_chars)]
    concat_string = "".join(alt_cased)

    return {
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": total_sum_str,
        "concat_string": concat_string,
    }


# ============
# Pydantic I/O
# ============
class BFHLRequest(BaseModel):
    data: List[Any]


# ============
# Health check
# ============
@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "BFHL API is up. Use POST /bfhl"}


# ================================
# Main endpoint: POST /bfhl (200)
# ================================
@app.post("/bfhl")
async def bfhl_endpoint(payload: BFHLRequest, request: Request) -> Dict[str, Any]:
    try:
        result = classify_and_compute(payload.data)
        response = {
            "is_success": True,
            "user_id": f"{FULL_NAME_LOWER}_{DOB_DDMMYYYY}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            **result,
        }
        return response
    except Exception as e:
        # Graceful failure: return is_success false and safe defaults
        return {
            "is_success": False,
            "user_id": f"{FULL_NAME_LOWER}_{DOB_DDMMYYYY}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": [],
            "even_numbers": [],
            "alphabets": [],
            "special_characters": [],
            "sum": "0",
            "concat_string": "",
            "error": str(e),
        }
