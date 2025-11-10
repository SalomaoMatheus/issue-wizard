# Issue Wizard

O Issue Wizard é uma ferramenta simples para ajudar no gerenciamento de tempo gasto em issues do GitLab. Ele permite que você visualize issues de uma milestone específica, inicie um cronômetro, e adicione o tempo gasto diretamente na issue.

---

### ✨ Features

- **Listagem de Issues:** Visualize todas as issues atribuídas a você em uma milestone específica.
- **Cronômetro Integrado:** Inicie e pare um cronômetro para registrar o tempo de trabalho em cada issue.
- **Adição de Tempo Manual:** Adicione tempo manualmente, se necessário.
- **Reabertura de Issues:** Reabra issues fechadas diretamente da interface.
- **Persistência:** A milestone selecionada é salva localmente para sua conveniência.

---

### 🛠️ Stack

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=for-the-badge&logo=flask)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript)
![GitLab](https://img.shields.io/badge/GitLab-API-orange?style=for-the-badge&logo=gitlab)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn)


---

### 🚀 Como Executar

Para executar o projeto, siga os passos abaixo.

**1. Clone o repositório:**
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd issue-wizard
```

**2. Configure as Variáveis de Ambiente:**

Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis:

```
GITLAB_URL="https://gitlab.com"  # Ou a URL da sua instância GitLab
PRIVATE_TOKEN="SEU_TOKEN_DE_ACESSO_PRIVADO"
GROUP_NAME="NOME_DO_SEU_GRUPO"
```

- `GITLAB_URL`: A URL da sua instância do GitLab (e.g., `https://gitlab.com`).
- `PRIVATE_TOKEN`: Seu token de acesso pessoal do GitLab com escopo de `api`.
- `GROUP_NAME`: O nome (slug) do grupo onde suas issues estão.

**3. Instale as Dependências:**

É recomendado criar um ambiente virtual.

```bash
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

Em seguida, instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

**4. Execute a Aplicação:**

Para desenvolvimento local, você pode usar:

```bash
python app.py
```

A aplicação estará disponível em `http://127.0.0.1:8888`.

Para um ambiente de produção, é recomendado usar o Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```
