from flask import Blueprint, jsonify
from src.models.questao_nova import QuestaoNova

questoes_pas_uem_bp = Blueprint('questoes_pas_uem', __name__)

@questoes_pas_uem_bp.route('/api/questoes_pas_uem', methods=['GET'])
def listar_questoes_pas_uem():
    """Listar todas as questões do PAS UEM sem paginação para compatibilidade com o frontend"""
    try:
        # Buscar todas as questões do PAS UEM
        questoes = QuestaoNova.query.filter_by(vestibular='PAS-UEM').order_by(QuestaoNova.numero.asc()).all()
        
        # Converter para dicionário
        questoes_dict = [questao.to_dict() for questao in questoes]
        
        return jsonify(questoes_dict)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

