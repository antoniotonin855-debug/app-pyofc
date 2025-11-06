# app.py
# Sistema de Gestão de TI
# ANTONIO FERREIRA TAVARES

from models import create_session, Chamado, Tecnico, IP, Ativo
from datetime import datetime

session = create_session()

# === CADASTROS ===

def cadastrar_tecnico():
    nome = input("Nome do técnico: ").strip()
    email = input("Email do técnico: ").strip()
    tecnico = Tecnico(nome=nome, email=email)
    session.add(tecnico)
    session.commit()
    print("Técnico cadastrado com sucesso!")

def cadastrar_chamado():
    categoria = input("Categoria (Sem Internet, VLAN, Wi-Fi...): ").strip()
    prioridade = input("Prioridade (Alta, Média, Baixa): ").strip()
    descricao = input("Descrição do problema: ").strip()
    chamado = Chamado(categoria=categoria, prioridade=prioridade, descricao=descricao)
    session.add(chamado)
    session.commit()
    print(f"Chamado aberto: {chamado}")

def listar_chamados():
    chamados = session.query(Chamado).all()
    for c in chamados:
        print(f"[{c.id}] {c.categoria} - {c.status} - {c.prioridade}")

def atualizar_status():
    listar_chamados()
    id_chamado = int(input("Digite o ID do chamado: "))
    novo_status = input("Novo status (Aberto, Em atendimento, Fechado): ").strip()
    chamado = session.get(Chamado, id_chamado)
    if chamado:
        chamado.status = novo_status
        if novo_status.lower() == "fechado":
            chamado.data_fechamento = datetime.now()
        session.commit()
        print("Status atualizado com sucesso!")
    else:
        print("Chamado não encontrado.")

def cadastrar_ip():
    endereco = input("Endereço IP: ").strip()
    mac = input("MAC (opcional): ").strip() or None
    reservado = input("Está reservado? (s/n): ").strip().lower() == "s"
    ip = IP(endereco=endereco, mac=mac, reservado=reservado, status="Alocado" if reservado else "Livre")
    session.add(ip)
    session.commit()
    print("IP cadastrado!")

def cadastrar_ativo():
    nome = input("Nome do ativo: ").strip()
    tipo = input("Tipo (Computador, Notebook, Switch, Roteador): ").strip()
    listar_ips()
    ip_id = int(input("ID do IP a vincular: "))
    ativo = Ativo(nome=nome, tipo=tipo, ip_id=ip_id)
    session.add(ativo)
    session.commit()
    print("Ativo cadastrado!")

def listar_ips():
    ips = session.query(IP).all()
    for i in ips:
        print(f"[{i.id}] {i.endereco} - {i.status}")

# === MENU PRINCIPAL ===
def menu():
    while True:
        print("""
===== GESTÃO DE TI =====
1. Cadastrar Técnico
2. Abrir Chamado
3. Listar Chamados
4. Atualizar Status de Chamado
5. Cadastrar IP
6. Cadastrar Ativo
0. Sair
""")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_tecnico()
        elif opcao == "2":
            cadastrar_chamado()
        elif opcao == "3":
            listar_chamados()
        elif opcao == "4":
            atualizar_status()
        elif opcao == "5":
            cadastrar_ip()
        elif opcao == "6":
            cadastrar_ativo()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
