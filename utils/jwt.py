from typing import Optional

import jwt
from fastapi import HTTPException, Header

from config import settings

ALGORITHM = "HS256"


def get_tenant_id_from_token(token: str) -> str:
    try:
        # Decodifica o token usando a chave secreta e o algoritmo definido
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])

        # Extrai o tenant_id do payload
        tenant_id: str = payload.get("tenant")

        if tenant_id is None:
            raise HTTPException(status_code=401, detail="Tenant ID not found in token.")

        return tenant_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token.")


# Dependência que extrai o token do cabeçalho e decodifica o tenant_id
def get_current_tenant_id(authorization: Optional[str] = Header(None)) -> str:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")

    # Remove o prefixo "Bearer " para obter apenas o token
    token = authorization[len("Bearer "):]
    return get_tenant_id_from_token(token)
