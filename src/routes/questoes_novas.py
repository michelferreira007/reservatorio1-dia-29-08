from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.questao_nova import QuestaoNova
from sqlalchemy import or_, and_

questoes_novas_bp = Blueprint('questoes_novas', __name__)

@questoes_novas_bp.route('/api/questoes-novas', methods=['GET'])
def listar_questoes_novas():
    try:
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Parâmetros de filtro
        busca = request.args.get('busca', '')
        ano = request.args.get('ano', '')
        materia = request.args.get('materia', '')
        assunto = request.args.get('assunto', '')
        vestibular = request.args.get('vestibular', '')
        
        # Construir query base
        query = QuestaoNova.query
        
        # Aplicar filtros
        if busca:
            query = query.filter(
                or_(
                    QuestaoNova.enunciado.contains(busca),
                    QuestaoNova.assunto.contains(busca)
                )
            )
        
        if ano:
            query = query.filter(QuestaoNova.ano == int(ano))
        
        if materia:
            query = query.filter(QuestaoNova.materia.contains(materia))
        
        if assunto:
            query = query.filter(QuestaoNova.assunto.contains(assunto))
        
        if vestibular:
            query = query.filter(QuestaoNova.vestibular.contains(vestibular))
        
        # Ordenar por ano e número
        query = query.order_by(QuestaoNova.ano.desc(), QuestaoNova.numero.asc())
        
        # Paginar
        questoes_paginadas = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Converter para dicionário
        questoes = [questao.to_dict() for questao in questoes_paginadas.items]
        
        return jsonify({
            'questoes': questoes,
            'total': questoes_paginadas.total,
            'pages': questoes_paginadas.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': questoes_paginadas.has_next,
            'has_prev': questoes_paginadas.has_prev
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_novas_bp.route('/api/questoes-novas/<int:questao_id>', methods=['GET'])
def obter_questao_nova(questao_id):
    try:
        questao = QuestaoNova.query.get_or_404(questao_id)
        return jsonify(questao.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_novas_bp.route('/api/questoes-novas/filtros', methods=['GET'])
def obter_filtros_questoes_novas():
    try:
        # Obter valores únicos para filtros
        anos = db.session.query(QuestaoNova.ano).distinct().order_by(QuestaoNova.ano.desc()).all()
        materias = db.session.query(QuestaoNova.materia).distinct().order_by(QuestaoNova.materia).all()
        assuntos = db.session.query(QuestaoNova.assunto).filter(QuestaoNova.assunto.isnot(None)).distinct().order_by(QuestaoNova.assunto).all()
        vestibulares = db.session.query(QuestaoNova.vestibular).distinct().order_by(QuestaoNova.vestibular).all()
        
        return jsonify({
            'anos': [ano[0] for ano in anos],
            'materias': [materia[0] for materia in materias],
            'assuntos': [assunto[0] for assunto in assuntos if assunto[0]],
            'vestibulares': [vestibular[0] for vestibular in vestibulares]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_novas_bp.route('/api/questoes-novas/<int:questao_id>/verificar-resposta', methods=['POST'])
def verificar_resposta(questao_id):
    try:
        data = request.get_json()
        alternativas_selecionadas = data.get('alternativas_selecionadas', [])
        
        questao = QuestaoNova.query.get_or_404(questao_id)
        
        # Converter alternativas selecionadas para conjunto
        selecionadas_set = set(alternativas_selecionadas)
        corretas_set = set(questao.to_dict()['alternativas_corretas'])
        
        # Verificar se a resposta está correta
        resposta_correta = selecionadas_set == corretas_set
        
        # Calcular pontuação parcial
        acertos = len(selecionadas_set.intersection(corretas_set))
        erros = len(selecionadas_set.difference(corretas_set))
        total_corretas = len(corretas_set)
        
        pontuacao_parcial = max(0, acertos - erros) / total_corretas if total_corretas > 0 else 0
        
        return jsonify({
            'correto': resposta_correta,
            'alternativas_corretas': list(corretas_set),
            'alternativas_selecionadas': alternativas_selecionadas,
            'acertos': acertos,
            'erros': erros,
            'pontuacao_parcial': round(pontuacao_parcial * 100, 1),
            'explicacao': questao.explicacao,
            'resposta_esperada': questao.resposta_correta
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_novas_bp.route('/api/questoes-novas/estatisticas', methods=['GET'])
def estatisticas_questoes_novas():
    try:
        total_questoes = QuestaoNova.query.count()
        
        # Estatísticas por matéria
        materias_stats = db.session.query(
            QuestaoNova.materia,
            db.func.count(QuestaoNova.id)
        ).group_by(QuestaoNova.materia).all()
        
        # Estatísticas por ano
        anos_stats = db.session.query(
            QuestaoNova.ano,
            db.func.count(QuestaoNova.id)
        ).group_by(QuestaoNova.ano).order_by(QuestaoNova.ano.desc()).all()
        
        # Estatísticas por vestibular
        vestibulares_stats = db.session.query(
            QuestaoNova.vestibular,
            db.func.count(QuestaoNova.id)
        ).group_by(QuestaoNova.vestibular).all()
        
        return jsonify({
            'total_questoes': total_questoes,
            'por_materia': [{'materia': m[0], 'quantidade': m[1]} for m in materias_stats],
            'por_ano': [{'ano': a[0], 'quantidade': a[1]} for a in anos_stats],
            'por_vestibular': [{'vestibular': v[0], 'quantidade': v[1]} for v in vestibulares_stats]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

