# models.py
# MIKAEL RODRIGUES NAVARROS
# SESI UNIVERSITARIO

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Enum, Boolean, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# ===== MODELOS PRINCIPAIS =====

class Chamado(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True)
    categoria = Column(String(100), nullable=False)  # Ex: Sem Internet, VLAN, Wi-Fi...
    prioridade = Column(String(50), nullable=False)  # Ex: Alta, Média, Baixa
    status = Column(String(50), default="Aberto")    # Ex: Aberto, Fechado, Em atendimento
    descricao = Column(String(255))
    data_abertura = Column(DateTime, default=datetime.now)
    data_fechamento = Column(DateTime, nullable=True)

    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"))
    tecnico = relationship("Tecnico", back_populates="chamados")

    def __repr__(self):
        return f"<Chamado id={self.id} categoria={self.categoria} status={self.status}>"

class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)

    chamados = relationship("Chamado", back_populates="tecnico")

    def __repr__(self):
        return f"<Tecnico id={self.id} nome={self.nome}>"

class IP(Base):
    __tablename__ = "ips"

    id = Column(Integer, primary_key=True)
    endereco = Column(String(15), nullable=False, unique=True)
    mac = Column(String(17), nullable=True)
    reservado = Column(Boolean, default=False)
    status = Column(String(20), default="Livre")  # Livre / Alocado

    def __repr__(self):
        return f"<IP {self.endereco} ({self.status})>"

class Ativo(Base):
    __tablename__ = "ativos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    tipo = Column(String(50))  # Ex: Computador, Notebook, Switch, Roteador
    ip_id = Column(Integer, ForeignKey("ips.id"))
    ip = relationship("IP")

    def __repr__(self):
        return f"<Ativo {self.nome} ({self.tipo})>"

# ===== CONEXÃO E SESSÃO =====

def get_engine(db_url="sqlite:///gestao_ti.db"):
    return create_engine(db_url, echo=False, future=True)

def create_session(db_url="sqlite:///gestao_ti.db"):
    engine = get_engine(db_url)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return SessionLocal()