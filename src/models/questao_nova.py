from src.models.user import db
from datetime import datetime
import json

class QuestaoNova(db.Model):
    __tablename__ = 'questoes_novas'
    
    id = db.Column(db.Integer, primary_key=True)
    vestibular = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    etapa = db.Column(db.String(50))  # Para vestibulares com etapas
    numero = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    assunto = db.Column(db.String(200))
    enunciado = db.Column(db.Text, nullable=False)
    alternativas = db.Column(db.Text, nullable=False)  # JSON string com lista de alternativas
    alternativas_numeracao = db.Column(db.Text, nullable=False)  # JSON string com numeração (01, 02, 04, 08, 16)
    resposta_correta = db.Column(db.String(10), nullable=False)  # Soma das alternativas corretas
    alternativas_corretas = db.Column(db.Text, nullable=False)  # JSON string com lista das alternativas corretas
    explicacao = db.Column(db.Text)
    dificuldade = db.Column(db.String(20), default='Média')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, vestibular, ano, numero, materia, enunciado, alternativas, 
                 alternativas_numeracao, resposta_correta, alternativas_corretas,
                 etapa=None, assunto=None, explicacao=None, dificuldade='Média'):
        self.vestibular = vestibular
        self.ano = ano
        self.etapa = etapa
        self.numero = numero
        self.materia = materia
        self.assunto = assunto
        self.enunciado = enunciado
        self.alternativas = json.dumps(alternativas) if isinstance(alternativas, list) else alternativas
        self.alternativas_numeracao = json.dumps(alternativas_numeracao) if isinstance(alternativas_numeracao, list) else alternativas_numeracao
        self.resposta_correta = resposta_correta
        self.alternativas_corretas = json.dumps(alternativas_corretas) if isinstance(alternativas_corretas, list) else alternativas_corretas
        self.explicacao = explicacao
        self.dificuldade = dificuldade
    
    def to_dict(self):
        return {
            'id': self.id,
            'vestibular': self.vestibular,
            'ano': self.ano,
            'etapa': self.etapa,
            'numero': self.numero,
            'materia': self.materia,
            'assunto': self.assunto,
            'enunciado': self.enunciado,
            'alternativas': json.loads(self.alternativas) if self.alternativas else [],
            'alternativas_numeracao': json.loads(self.alternativas_numeracao) if self.alternativas_numeracao else [],
            'resposta_correta': self.resposta_correta,
            'alternativas_corretas': json.loads(self.alternativas_corretas) if self.alternativas_corretas else [],
            'explicacao': self.explicacao,
            'dificuldade': self.dificuldade,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

