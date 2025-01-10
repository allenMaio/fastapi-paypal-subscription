from fastapi import HTTPException

paypal_token_store = {
    "access_token": None
}

def store_paypal_token(access_token: str):
    paypal_token_store["access_token"] = access_token

def get_paypal_token():
    access_token = paypal_token_store.get("access_token")
    if not access_token:
        raise HTTPException(401, "Token not found, please login first.")
    return access_token