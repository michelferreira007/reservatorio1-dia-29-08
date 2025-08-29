from src.models.user import db
from datetime import datetime
import json

class Questao(db.Model):
    __tablename__ = 'questoes'
    
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer, nullable=False)
    vestibular = db.Column(db.String(50), nullable=False)
    dia = db.Column(db.Integer, nullable=True)
    caderno = db.Column(db.String(20), nullable=True)
    numero = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    assunto = db.Column(db.String(100), nullable=True)
    enunciado = db.Column(db.Text, nullable=False)
    alternativas = db.Column(db.Text, nullable=False)  # JSON string
    resposta_correta = db.Column(db.String(1), nullable=False)
    explicacao = db.Column(db.Text, nullable=True)
    dificuldade = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, ano, vestibular, numero, materia, enunciado, alternativas, resposta_correta, 
                 dia=None, caderno=None, assunto=None, explicacao=None, dificuldade=None):
        self.ano = ano
        self.vestibular = vestibular
        self.dia = dia
        self.caderno = caderno
        self.numero = numero
        self.materia = materia
        self.assunto = assunto
        self.enunciado = enunciado
        self.alternativas = json.dumps(alternativas) if isinstance(alternativas, list) else alternativas
        self.resposta_correta = resposta_correta
        self.explicacao = explicacao
        self.dificuldade = dificuldade
    
    def to_dict(self):
        return {
            'id': self.id,
            'ano': self.ano,
            'vestibular': self.vestibular,
            'dia': self.dia,
            'caderno': self.caderno,
            'numero': self.numero,
            'materia': self.materia,
            'assunto': self.assunto,
            'enunciado': self.enunciado,
            'alternativas': json.loads(self.alternativas) if self.alternativas else [],
            'resposta_correta': self.resposta_correta,
            'explicacao': self.explicacao,
            'dificuldade': self.dificuldade,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Simulado(db.Model):
    __tablename__ = 'simulados'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    questoes_ids = db.Column(db.Text, nullable=False)  # JSON string com IDs das questões
    tempo_limite = db.Column(db.Integer, nullable=True)  # em minutos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, nome, questoes_ids, descricao=None, tempo_limite=None):
        self.nome = nome
        self.descricao = descricao
        self.questoes_ids = json.dumps(questoes_ids) if isinstance(questoes_ids, list) else questoes_ids
        self.tempo_limite = tempo_limite
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'questoes_ids': json.loads(self.questoes_ids) if self.questoes_ids else [],
            'tempo_limite': self.tempo_limite,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ResultadoSimulado(db.Model):
    __tablename__ = 'resultados_simulados'
    
    id = db.Column(db.Integer, primary_key=True)
    simulado_id = db.Column(db.Integer, db.ForeignKey('simulados.id'), nullable=False)
    usuario_nome = db.Column(db.String(100), nullable=False)
    respostas = db.Column(db.Text, nullable=False)  # JSON string com respostas
    pontuacao = db.Column(db.Integer, nullable=False)
    total_questoes = db.Column(db.Integer, nullable=False)
    tempo_gasto = db.Column(db.Integer, nullable=True)  # em segundos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    simulado = db.relationship('Simulado', backref=db.backref('resultados', lazy=True))
    
    def __init__(self, simulado_id, usuario_nome, respostas, pontuacao, total_questoes, tempo_gasto=None):
        self.simulado_id = simulado_id
        self.usuario_nome = usuario_nome
        self.respostas = json.dumps(respostas) if isinstance(respostas, dict) else respostas
        self.pontuacao = pontuacao
        self.total_questoes = total_questoes
        self.tempo_gasto = tempo_gasto
    
    def to_dict(self):
        return {
            'id': self.id,
            'simulado_id': self.simulado_id,
            'usuario_nome': self.usuario_nome,
            'respostas': json.loads(self.respostas) if self.respostas else {},
            'pontuacao': self.pontuacao,
            'total_questoes': self.total_questoes,
            'percentual': round((self.pontuacao / self.total_questoes) * 100, 2) if self.total_questoes > 0 else 0,
            'tempo_gasto': self.tempo_gasto,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

