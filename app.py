#app.py
from decimal import Decimal 
from models import create_session, Cliente, Produto, Pedido, ItemPedido

DB_URL = "sqlite:///loja_jogos.db"
session = create_session(DB_URL)

def cadastrar_cliente():
    nome = input("Nome do Cliente: ").strip()
    email = input("Email do Cliente: ").strip()
    telefone = input("Telefone do Cliente: ").strip() or None 
    
    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    session.add(cliente)
    session.commit()
    print(f"Cliente Cadastrado: {cliente}")
    
def cadastrar_produto():
    nome_produto = input("Nome do produto: ").string()
    preco = Decimal(input("Preço do Produto (ex: 199.99): ")).replace(",", ".")
    estoque = int(input("Estoque: "))
    
    produto = Produto(nome_produto=nome_produto, preco=preco, estoque=estoque)
    session.add(produto)
    session.commit()
    print(f"Produto Cadastrado: {nome_produto}")
    
def criar_pedido():
    cliente_id = int(input("Digite o ID do cliente: "))
    pedido = Pedido(cliente_id=cliente_id)
    session.add(pedido)
    session.flush() # garante o ID do pedido antes de inserir itens
    
    print("Adicione itens (Enter em produtos_ID para finalizar). ")
    while True:
        val = input("Produto ID(Enter para sair): ").strip()
        if not val:
            break
        produto_id = int(val)
        quantidade = int(input("Quantidade: "))
        
        # Buscar produto para pegar preço e validar o estoque
        produto = session.get(Produto, produto_id)
        if produto is None:
            print("Produto não encontrado.")
            continue
        
        if produto.estoque < quantidade:
            print(f"Estoque insuficiente. Quantidade Disponível: {produto.estoque}")
            
        # Debita do estoque 
        produto.estoque -= quantidade 
        
        item = ItemPedido(
            pedido_id = pedido.id,
            produto_id = produto_id,
            quantidade = quantidade,
            preco_unit = produto.preco 
        )
        session.add(item)
    
    session.commit()
    
    