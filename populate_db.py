import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.questao import db, Questao
from src.main import app
import json

# Carregar questões de exemplo
with open('../questoes_exemplo.json', 'r', encoding='utf-8') as f:
    questoes_data = json.load(f)

with app.app_context():
    # Criar tabelas
    db.create_all()
    
    # Verificar se já existem questões
    if Questao.query.count() > 0:
        print('Banco de dados já contém questões.')
    else:
        # Adicionar questões de exemplo
        for q_data in questoes_data:
            questao = Questao(
                ano=q_data['ano'],
                vestibular=q_data['vestibular'],
                dia=q_data['dia'],
                caderno=q_data['caderno'],
                numero=q_data['numero'],
                materia=q_data['materia'],
                assunto=q_data['assunto'],
                enunciado=q_data['enunciado'],
                alternativas=q_data['alternativas'],
                resposta_correta=q_data['resposta_correta'],
                explicacao=q_data['explicacao']
            )
            db.session.add(questao)
        
        db.session.commit()
        print('Questões de exemplo adicionadas com sucesso!')

