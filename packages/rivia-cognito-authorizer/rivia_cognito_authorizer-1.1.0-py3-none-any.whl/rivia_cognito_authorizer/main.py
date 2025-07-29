import jwt
import requests
import os
import boto3
from typing import Callable
from jwt import PyJWKClient
from fastapi import Security, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Check for required environment variables
required_env_vars = {
    'REGION': os.getenv('REGION'),
    'COGNITO_USER_POOL_ID': os.getenv('COGNITO_USER_POOL_ID'),
    'COGNITO_APP_CLIENT_ID': os.getenv('COGNITO_APP_CLIENT_ID')
}

missing_vars = [var for var, value in required_env_vars.items() if not value]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

REGION = required_env_vars['REGION']
USER_POOL_ID = required_env_vars['COGNITO_USER_POOL_ID']
APP_CLIENT_ID = required_env_vars['COGNITO_APP_CLIENT_ID'].split(',')
JWKS_URL = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
JWKS_KEYS = None
jwks_client = PyJWKClient(JWKS_URL)
cognito_client = boto3.client('cognito-idp', region_name=REGION)
security = HTTPBearer()


def get_public_key(token):
    """
    Retrieve the public signing key from a JWT token.
    Args:
        token (str): The JWT token from which to extract the public key.
    Returns:
        str: The public signing key associated with the provided JWT token.
    """
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    return signing_key.key


def get_jwks():
    """
    Retrieve JSON Web Key Set (JWKS) from a specified URL.
    This function checks if the global variable JWKS_KEYS is empty. If it is,
    it makes an HTTP GET request to the JWKS_URL to fetch the JWKS. The response
    is then parsed as JSON and stored in the JWKS_KEYS variable. If JWKS_KEYS
    is already populated, it simply returns the existing keys.
    Returns:
        dict: The JSON Web Key Set (JWKS) as a dictionary.
    Raises:
        requests.exceptions.HTTPError: If the HTTP request to fetch the JWKS fails.
    """
    global JWKS_KEYS
    if not JWKS_KEYS:
        response = requests.get(JWKS_URL)
        response.raise_for_status()
        JWKS_KEYS = response.json()
    return JWKS_KEYS


def verify_token(auth: HTTPAuthorizationCredentials = Security(security)):
    """
    Validates a JWT token against a Cognito user pool.
    Args:
        token (str): The JWT token to be validated.
        scopes (list, optional): A list of required scopes. Defaults to an empty list.
    Returns:
        dict: The decoded token payload if the token is valid.
    Raises:
        ValueError: If the token is invalid, expired, or does not contain the required scopes.
    The function performs the following steps:
    1. Extracts the 'kid' from the token header.
    2. Retrieves the JSON Web Key Set (JWKS) and finds the corresponding key using 'kid'.
    3. Uses the public key to decode the token and validate its signature, audience, and issuer.
    4. Checks if the token contains the required scopes.
    Note:
        The function assumes that `REGION` and `USER_POOL_ID` are defined as environment variables.
    """
    token = auth.credentials
    headers = jwt.get_unverified_header(token)
    kid = headers.get('kid')
    if not kid:
        raise ValueError("Invalid token: kid not found in token header")

    jwks = get_jwks()
    key = next((key for key in jwks['keys'] if key['kid'] == kid), None)
    if not key:
        raise ValueError("Invalid token: kid not found in jwks")

    public_key = get_public_key(token)
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience=APP_CLIENT_ID,
            issuer=f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}",
        )
    except jwt.ExpiredSignatureError:
        raise ValueError("Invalid token: token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token: invalid token")
    return payload


def allowed_for_groups(groups: list[str]) -> Callable:
    """
    Create a dependency that checks if the user belongs to any of the specified groups.
    Args:
        groups: List of group names to check against
    Returns:
        A dependency function that verifies group membership
    """
    async def verify_user(token_payload: dict = Depends(verify_token)) -> dict:
        if not any(group in token_payload.get('cognito:groups', []) for group in groups):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='User does not belong to any of the required groups'
            )
        return token_payload
        
    return verify_user
