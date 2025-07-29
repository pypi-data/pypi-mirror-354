# Rivia Cognito FastAPI Authorizer

Este projeto fornece uma implementação de um autorizador JWT usando o Amazon Cognito e FastAPI. Ele verifica tokens JWT para autenticação e autorização de usuários.

## Requisitos

Certifique-se de que as seguintes variáveis de ambiente estejam configuradas:

- `REGION`: A região AWS onde seu User Pool do Cognito está localizado.
- `COGNITO_USER_POOL_ID`: O ID do User Pool do Cognito.
- `COGNITO_APP_CLIENT_ID`: O ID do cliente da aplicação do Cognito.

## Instalação

1. Clone o repositório:
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd rivia-cognito-fastapi-authorizer
    ```

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Verificação de Token

A função `verify_token` verifica a validade de um token JWT. Ela realiza várias verificações, incluindo a assinatura do token, a expiração e a audiência.

Exemplo de uso:
```python
from fastapi import FastAPI, Depends
from rivia-cognito-authorizer import verify_token

app = FastAPI()

@app.get("/secure-endpoint")
async def secure_endpoint(token_payload: dict = Depends(verify_token)):
    return {"message": "This is a secure endpoint", "user": token_payload}
```

### Verificação de Grupos

A função `allowed_for_groups` cria uma dependência que verifica se o usuário pertence a um dos grupos especificados.

Exemplo de uso:
```python
from fastapi import FastAPI, Depends
from rivia-cognito-authorizer import allowed_for_groups

app = FastAPI()

@app.get("/admin-endpoint")
async def admin_endpoint(token_payload: dict = Depends(allowed_for_groups(["admin"]))):
    return {"message": "This is an admin endpoint", "user": token_payload}
```

## Licença

Este projeto está licenciado sob a Licença Apache 2.0. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.