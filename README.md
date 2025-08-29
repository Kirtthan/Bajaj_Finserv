# Bajaj_Finserv

## 📘 BFHL API – FastAPI Implementation

A FastAPI-based REST API implementing the BFHL specification.
Built with Python, fully tested, and deployable on Vercel, Render, or Railway.

## 📑 Problem Statement

The API must expose a POST /bfhl route that accepts an array and returns:

✅ is_success → operation status

✅ user_id → {full_name_ddmmyyyy} (lowercase, underscores)

✅ email → your email

✅ roll_number → your roll number

✅ odd_numbers → numeric tokens that are odd (as strings)

✅ even_numbers → numeric tokens that are even (as strings)

✅ alphabets → alphabet-only tokens, converted to uppercase

✅ special_characters → all other tokens

✅ sum → sum of numeric tokens (as string)

✅ concat_string → all alphabetic characters, reversed, with alternating caps (Upper, lower, …)

Examples given in the prompt are replicated as unit tests.

## ⚙️ Tech Stack

FastAPI
 → high-performance Python web framework (ASGI)

Uvicorn
 → ASGI server for local dev

Pydantic
 → request validation

Mangum
 → adapter for serverless (Vercel/AWS Lambda)

Pytest
 → unit tests

## 📂 Project Structure
.
├── api
│   └── index.py          # Vercel entrypoint (wraps FastAPI with Mangum)
├── app
│   ├── __init__.py
│   └── main.py           # Core FastAPI app
├── tests
│   └── test_bfhl.py      # Unit tests (Examples A/B/C + edge cases)
├── requirements.txt
├── vercel.json           # Config for Vercel
└── README.md

## 🖥️ Run Locally

Clone repo:

git clone https://github.com/<your-username>/bfhl-api.git
cd bfhl-api


Create virtual env & install deps:

python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.\.venv\Scripts\activate         # Windows CMD
pip install -r requirements.txt


Set environment variables:

export FULL_NAME_LOWER="kirtthan_duvvi"
export DOB_DDMMYYYY="17032005"
export EMAIL="kirtthanduvvi17@gmail.com"
export ROLL_NUMBER="22BCE0061"


(Windows CMD)

set FULL_NAME_LOWER=kirtthan_duvvi
set DOB_DDMMYYYY=17032005
set EMAIL=kirtthanduvvi17@gmail.com
set ROLL_NUMBER=22BCE0061


Run server:

uvicorn app.main:app --reload


Visit:

Health: http://127.0.0.1:8000/

Swagger Docs: http://127.0.0.1:8000/docs

Endpoint: POST /bfhl

## 🔍 Example Requests
Request A
{
  "data": ["a","1","334","4","R","$"]
}

Response A
{
  "is_success": true,
  "user_id": "parth_suri_17092004",
  "email": "parthsuri009@gmail.com",
  "roll_number": "22BCE0061",
  "odd_numbers": ["1"],
  "even_numbers": ["334","4"],
  "alphabets": ["A","R"],
  "special_characters": ["$"],
  "sum": "339",
  "concat_string": "Ra"
}

✅ Unit Tests

Run tests locally:

pip install pytest
pytest -q


Covers:

Example A, B, C from the prompt

Mixed alphanumerics (abc123) → special

Signed ints (-42, +9) → valid numbers

Empty tokens → special

## ☁️ Deployment
🔹 Render / Railway

Build Command: pip install -r requirements.txt

Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT

Add env vars (FULL_NAME_LOWER, DOB_DDMMYYYY, EMAIL, ROLL_NUMBER)

Test URL: https://<service>.onrender.com/bfhl

## 🔹 Vercel (preferred)

Project includes:

api/index.py → wraps FastAPI with Mangum

vercel.json → tells Vercel to use Python runtime

Push to GitHub.

Import project on Vercel Dashboard.

Add env vars in Settings → Environment Variables.

Deploy → you get https://<project>.vercel.app.

Test:

curl -X POST https://<project>.vercel.app/bfhl \
  -H "Content-Type: application/json" \
  -d '{"data":["a","1","334","4","R","$"]}'

## ⚠️ Troubleshooting

404 on /bfhl → check you’re using POST, not GET.

500 error on Vercel → ensure mangum is in requirements.txt and api/index.py exports handler.

ModuleNotFoundError: app.main → ensure app/__init__.py exists.

Numbers not returned as strings → never cast tokens to int before appending to lists.

## 📌 Submission Reminder

The URL you submit must be:

https://<your-project>.vercel.app/bfhl


And the response must exactly match the required schema with your user_id, email, and roll_number.

