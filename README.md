# Instruções para o Issue Wizard

## Configuração

1.  **Instale o Python 3.8+** se ainda não o tiver.
2.  **Clone este repositório** e navegue até a pasta `issue_wizard`.
3.  **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    ```
4.  **Ative o ambiente virtual:**
    *   No Windows: `venv\Scripts\activate`
    *   No macOS/Linux: `source venv/bin/activate`
5.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Configure suas credenciais:**
    *   Renomeie o arquivo `.env.example` para `.env`.
    *   Abra o arquivo `.env` e preencha com seus dados do GitLab.

## Execução

1.  Com o ambiente virtual ativado, inicie o servidor:
    ```bash
    gunicorn --bind 0.0.0.0:8000 app:app
    ```
2.  Abra seu navegador e acesse `http://localhost:8000`.
