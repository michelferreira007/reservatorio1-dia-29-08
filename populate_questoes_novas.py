import json
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app
from src.models.user import db
from src.models.questao_nova import QuestaoNova

def popular_questoes_novas():
    with app.app_context():
        # Criar as tabelas se não existirem
        db.create_all()
        
        # Carregar questões do arquivo JSON
        with open('../questoes_pas_uem.json', 'r', encoding='utf-8') as f:
            questoes_data = json.load(f)
        
        print(f"Carregando {len(questoes_data)} questões...")
        
        for questao_data in questoes_data:
            # Verificar se a questão já existe
            questao_existente = QuestaoNova.query.filter_by(
                vestibular=questao_data['vestibular'],
                ano=questao_data['ano'],
                numero=questao_data['numero']
            ).first()
            
            if questao_existente:
                print(f"Questão {questao_data['numero']} já existe, pulando...")
                continue
            
            # Criar nova questão
            nova_questao = QuestaoNova(
                vestibular=questao_data['vestibular'],
                ano=questao_data['ano'],
                etapa=questao_data.get('etapa'),
                numero=questao_data['numero'],
                materia=questao_data['materia'],
                assunto=questao_data.get('assunto'),
                enunciado=questao_data['enunciado'],
                alternativas=questao_data['alternativas'],
                alternativas_numeracao=questao_data['alternativas_numeracao'],
                resposta_correta=questao_data['resposta_correta'],
                alternativas_corretas=questao_data['alternativas_corretas'],
                explicacao=questao_data.get('explicacao'),
                dificuldade=questao_data.get('dificuldade', 'Média')
            )
            
            db.session.add(nova_questao)
            print(f"Adicionada questão {questao_data['numero']}: {questao_data['materia']}")
        
        # Salvar no banco
        db.session.commit()
        print("Questões populadas com sucesso!")
        
        # Mostrar estatísticas
        total_questoes = QuestaoNova.query.count()
        print(f"Total de questões no banco: {total_questoes}")

if __name__ == '__main__':
    popular_questoes_novas()

