import os
import gitlab
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração inicial
GITLAB_URL = os.getenv('GITLAB_URL')
PRIVATE_TOKEN = os.getenv('PRIVATE_TOKEN')
GROUP_NAME = os.getenv('GROUP_NAME')

# Inicializa o Flask App
app = Flask(__name__)

# Conecta-se ao GitLab
# A opção ssl_verify=False pode ser necessária se o seu GitLab
# usar um certificado SSL autoassinado. Remova se não for o caso.
gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN, ssl_verify=True)

@app.route('/')
def index():
    """Renderiza a página inicial."""
    return render_template('index.html')

@app.route('/api/issues')
def get_issues():
    """API para buscar as issues de uma milestone, assinadas ao usuário."""
    milestone = request.args.get('milestone')
    if not milestone:
        return jsonify({"error": "O nome da milestone é obrigatório."}), 400

    try:
        # Autentica para buscar informações do usuário logado (dono do token)
        gl.auth()
        
        # Pega o grupo especificado
        group = gl.groups.get(GROUP_NAME)
        
        # Busca as issues no grupo filtrando pela milestone e assinadas ao usuário
        issues = group.issues.list(milestone=milestone, scope='assigned_to_me', all=True)
        
        # Formata os dados para o frontend
        issues_data = [
            {
                'id': issue.id,
                'iid': issue.iid,
                'project_id': issue.project_id,
                'title': issue.title,
                'state': issue.state,
                'time_estimate': issue.time_stats['human_time_estimate'] or '0h',
                'total_time_spent': issue.time_stats['human_total_time_spent'] or '0h',
                'web_url': issue.web_url
            }
            for issue in issues
        ]
        return jsonify(issues_data)

    except gitlab.exceptions.GitlabError as e:
        return jsonify({"error": f"Erro ao contatar o GitLab: {e.error_message}"}), e.response_code
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {str(e)}"}), 500


@app.route('/api/add_time', methods=['POST'])
def add_time():
    """API para adicionar tempo a uma issue."""
    data = request.json
    project_id = data.get('project_id')
    issue_iid = data.get('issue_iid')
    duration = data.get('duration') # Formato: "1h 30m"

    if not all([project_id, issue_iid, duration]):
        return jsonify({"error": "project_id, issue_iid e duration são obrigatórios."}), 400

    try:
        project = gl.projects.get(project_id)
        issue = project.issues.get(issue_iid)
        
        # Adiciona o tempo gasto
        issue.add_spent_time(duration)
        
        # Pega a issue atualizada para retornar o novo tempo total
        updated_issue = project.issues.get(issue_iid)

        # O atributo time_stats pode se comportar de forma diferente (dict vs method)
        # dependendo de como o objeto issue foi obtido.
        # Esta abordagem garante que lidamos com ambos os casos.
        time_stats = getattr(updated_issue, 'time_stats')
        if callable(time_stats):
            time_stats = time_stats()
            
        new_total_spent = time_stats['human_total_time_spent'] or '0h'

        return jsonify({"success": True, "new_total_spent": new_total_spent})

    except gitlab.exceptions.GitlabError as e:
        return jsonify({"error": f"Erro ao contatar o GitLab: {e.error_message}"}), e.response_code
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {str(e)}"}), 500


@app.route('/api/reopen_issue', methods=['POST'])
def reopen_issue():
    """API para reabrir uma issue."""
    data = request.json
    project_id = data.get('project_id')
    issue_iid = data.get('issue_iid')

    if not all([project_id, issue_iid]):
        return jsonify({"error": "project_id e issue_iid são obrigatórios."}), 400

    try:
        project = gl.projects.get(project_id)
        issue = project.issues.get(issue_iid)
        
        # Reabrir a issue
        issue.state_event = 'reopen'
        issue.save()
        
        return jsonify({"success": True})

    except gitlab.exceptions.GitlabError as e:
        return jsonify({"error": f"Erro ao contatar o GitLab: {e.error_message}"}), e.response_code
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {str(e)}"}), 500


@app.route('/api/milestones')
def get_milestones():
    """API para listar milestones do grupo."""
    try:
        group = gl.groups.get(GROUP_NAME)
        milestones = group.milestones.list(all=True)
        
        milestones_data = [
            {
                'id': m.id,
                'title': m.title
            }
            for m in milestones
        ]
        return jsonify(milestones_data)

    except gitlab.exceptions.GitlabError as e:
        return jsonify({"error": f"Erro ao contatar o GitLab: {e.error_message}"}), e.response_code
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro inesperado: {str(e)}"}), 500


if __name__ == '__main__':
    # Usado apenas para desenvolvimento local. Para produção, use Gunicorn.
    app.run(debug=True, port=8888)
