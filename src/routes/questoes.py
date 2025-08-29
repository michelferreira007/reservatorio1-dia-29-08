from flask import Blueprint, request, jsonify
from src.models.questao import db, Questao, Simulado, ResultadoSimulado
from sqlalchemy import and_, or_
import json

questoes_bp = Blueprint('questoes', __name__)

@questoes_bp.route('/questoes', methods=['GET'])
def get_questoes():
    """Buscar questões com filtros opcionais"""
    try:
        # Parâmetros de filtro
        ano = request.args.get('ano', type=int)
        vestibular = request.args.get('vestibular')
        materia = request.args.get('materia')
        assunto = request.args.get('assunto')
        dificuldade = request.args.get('dificuldade')
        busca = request.args.get('busca')
        
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Construir query
        query = Questao.query
        
        if ano:
            query = query.filter(Questao.ano == ano)
        if vestibular:
            query = query.filter(Questao.vestibular.ilike(f'%{vestibular}%'))
        if materia:
            query = query.filter(Questao.materia.ilike(f'%{materia}%'))
        if assunto:
            query = query.filter(Questao.assunto.ilike(f'%{assunto}%'))
        if dificuldade:
            query = query.filter(Questao.dificuldade == dificuldade)
        if busca:
            query = query.filter(or_(
                Questao.enunciado.ilike(f'%{busca}%'),
                Questao.assunto.ilike(f'%{busca}%')
            ))
        
        # Executar query com paginação
        questoes_paginadas = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'questoes': [q.to_dict() for q in questoes_paginadas.items],
            'total': questoes_paginadas.total,
            'pages': questoes_paginadas.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/questoes/<int:questao_id>', methods=['GET'])
def get_questao(questao_id):
    """Buscar uma questão específica"""
    try:
        questao = Questao.query.get_or_404(questao_id)
        return jsonify(questao.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/questoes', methods=['POST'])
def create_questao():
    """Criar uma nova questão"""
    try:
        data = request.get_json()
        
        questao = Questao(
            ano=data['ano'],
            vestibular=data['vestibular'],
            numero=data['numero'],
            materia=data['materia'],
            enunciado=data['enunciado'],
            alternativas=data['alternativas'],
            resposta_correta=data['resposta_correta'],
            dia=data.get('dia'),
            caderno=data.get('caderno'),
            assunto=data.get('assunto'),
            explicacao=data.get('explicacao'),
            dificuldade=data.get('dificuldade')
        )
        
        db.session.add(questao)
        db.session.commit()
        
        return jsonify(questao.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/questoes/filtros', methods=['GET'])
def get_filtros():
    """Obter opções disponíveis para filtros"""
    try:
        anos = db.session.query(Questao.ano.distinct()).all()
        vestibulares = db.session.query(Questao.vestibular.distinct()).all()
        materias = db.session.query(Questao.materia.distinct()).all()
        assuntos = db.session.query(Questao.assunto.distinct()).filter(Questao.assunto.isnot(None)).all()
        dificuldades = db.session.query(Questao.dificuldade.distinct()).filter(Questao.dificuldade.isnot(None)).all()
        
        return jsonify({
            'anos': sorted([a[0] for a in anos], reverse=True),
            'vestibulares': sorted([v[0] for v in vestibulares]),
            'materias': sorted([m[0] for m in materias]),
            'assuntos': sorted([a[0] for a in assuntos]),
            'dificuldades': sorted([d[0] for d in dificuldades])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/simulados', methods=['GET'])
def get_simulados():
    """Listar todos os simulados"""
    try:
        simulados = Simulado.query.order_by(Simulado.created_at.desc()).all()
        return jsonify([s.to_dict() for s in simulados])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/simulados', methods=['POST'])
def create_simulado():
    """Criar um novo simulado"""
    try:
        data = request.get_json()
        
        simulado = Simulado(
            nome=data['nome'],
            questoes_ids=data['questoes_ids'],
            descricao=data.get('descricao'),
            tempo_limite=data.get('tempo_limite')
        )
        
        db.session.add(simulado)
        db.session.commit()
        
        return jsonify(simulado.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/simulados/<int:simulado_id>', methods=['GET'])
def get_simulado(simulado_id):
    """Buscar um simulado específico com suas questões"""
    try:
        simulado = Simulado.query.get_or_404(simulado_id)
        questoes_ids = json.loads(simulado.questoes_ids)
        questoes = Questao.query.filter(Questao.id.in_(questoes_ids)).all()
        
        simulado_dict = simulado.to_dict()
        simulado_dict['questoes'] = [q.to_dict() for q in questoes]
        
        return jsonify(simulado_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/simulados/<int:simulado_id>/resultado', methods=['POST'])
def salvar_resultado_simulado(simulado_id):
    """Salvar resultado de um simulado"""
    try:
        data = request.get_json()
        
        resultado = ResultadoSimulado(
            simulado_id=simulado_id,
            usuario_nome=data['usuario_nome'],
            respostas=data['respostas'],
            pontuacao=data['pontuacao'],
            total_questoes=data['total_questoes'],
            tempo_gasto=data.get('tempo_gasto')
        )
        
        db.session.add(resultado)
        db.session.commit()
        
        return jsonify(resultado.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/resultados/<usuario_nome>', methods=['GET'])
def get_resultados_usuario(usuario_nome):
    """Buscar resultados de um usuário"""
    try:
        resultados = ResultadoSimulado.query.filter_by(usuario_nome=usuario_nome).order_by(ResultadoSimulado.created_at.desc()).all()
        return jsonify([r.to_dict() for r in resultados])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/estatisticas', methods=['GET'])
def get_estatisticas():
    """Obter estatísticas gerais do banco de questões"""
    try:
        total_questoes = Questao.query.count()
        total_simulados = Simulado.query.count()
        total_resultados = ResultadoSimulado.query.count()
        
        questoes_por_vestibular = db.session.query(
            Questao.vestibular, 
            db.func.count(Questao.id)
        ).group_by(Questao.vestibular).all()
        
        questoes_por_materia = db.session.query(
            Questao.materia, 
            db.func.count(Questao.id)
        ).group_by(Questao.materia).all()
        
        return jsonify({
            'total_questoes': total_questoes,
            'total_simulados': total_simulados,
            'total_resultados': total_resultados,
            'questoes_por_vestibular': dict(questoes_por_vestibular),
            'questoes_por_materia': dict(questoes_por_materia)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

