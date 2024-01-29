
import mysql.connector
import os
from random import randint
from datetime import datetime


class Membro:
    def __init__(self, nome, cur):
        self.nome = nome
        self.cur = cur

    codigos = {}

    def cadastrar_membro(self):
        self.num_gerado = randint(1, 100)
        self.mitigar_duplicidade_codigo()
        self.codigos = {f'membro {self.nome}': self.nome, 'codigo': self.num_gerado}
        self.cadastro = 'insert into membros(s_nome_membros, i_codigo_membros) values(%s, %s);'
        self.info = (self.nome, self.num_gerado)
        self.cur.execute(self.cadastro, self.info)

    def mitigar_duplicidade_codigo(self):
        while True:
            self.comando = 'select exists(select i_codigo_membros from membros where i_codigo_membros=%s)'
            self.dados = (self.num_gerado,)
            self.cur.execute(self.comando, self.dados)
            self.existe = self.cur.fetchone()[0]
            if not self.existe:
                break
            else:
                self.num_gerado = randint(1, 100)


class Livro:
    def __init__(self, titulo, autor, genero):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.quantidade = 1


class Biblioteca:
    def __init__(self, crsor):
        self.crsor = crsor

    @staticmethod
    def menu():
        print("""
        1. Cadastrar membro
        2. Cadastrar livro
        3. Excluir cadastro
        4. Emprestar livro
        5. Receber devolução
        6. Sair""")

    def cadastrar_livro(self, livro):
        self.livro = livro
        self.orientacao = ('insert into acervo(s_titulo_acervo, s_autor_acervo, s_genero_acervo, i_quantidade_acervo) '
                           'values(%s, %s, %s, %s);')
        self.informacoes = (self.livro.titulo, self.livro.autor, self.livro.genero, self.livro.quantidade)
        self.crsor.execute(self.orientacao, self.informacoes)

    def emprestar_livro(self, membro):
        self.membro = membro
        self.liv = str(input('Título do livro: ')).strip()
        self.ordem = 'update acervo set s_statuslivro_acervo=%s, s_membroemprestimo_acervo=%s where s_titulo_acervo=%s;'
        self.conteudo = ('Emprestado', self.membro.nome, self.liv)
        self.crsor.execute(self.ordem, self.conteudo)
        self.data_emprestimo = datetime.now()
        self.prescricao = ('update membros set d_dataemprestimo_membros=%s, i_livrosemprestados_membros=%s, '
                           's_nomelivroemprestado=%s where s_nome_membros=%s;')
        self.data = (self.data_emprestimo, 1, self.liv, self.membro.nome)
        self.crsor.execute(self.prescricao, self.data)

    def aceitar_devolucao(self):
        self.membro_ = str(input('Nome do membro: ')).strip()
        self.livro_ = str(input('Título do livro: ')).strip()
        self.comando_1 = ('update membros set d_dataemprestimo_membros=%s , i_livrosemprestados_membros=%s,'
                          's_nomelivroemprestado=%s where s_nome_membros=%s and s_nomelivroemprestado=%s;')
        self.componentes_1 = (None, 0, None, self.membro_, self.livro_)
        self.crsor.execute(self.comando_1, self.componentes_1)
        self.comando_2 = 'update acervo set s_statuslivro_acervo=%s, s_membroemprestimo_acervo=%s where s_titulo_acervo=%s;'
        self.componente_2 = ('Disponível', None, self.livro_)
        self.crsor.execute(self.comando_2, self.componente_2)

    def excluir_livro(self, livro):
        while True:
            try:
                self.livrx = livro
                self.command = 'delete from acervo where s_titulo_acervo=%s and i_id_acervo=%s;'
                self.IDlivro = int(input('ID do livro: '))
                self.componente = (self.livrx.titulo, self.IDlivro)
                self.crsor.execute(self.command, self.componente)
            except ValueError:
                print('ID inválido!')
            else:
                break

    def excluir_membro(self, membro):
        while True:
            try:
                self.mmbro = membro
                self.order = 'delete from membros where s_nome_membros=%s and id_membro_membros=%s;'
                self.IDmembro = int(input('ID do membro: '))
                self.dadxs = (self.mmbro.nome, self.IDmembro)
                self.crsor.execute(self.order, self.dadxs)
            except ValueError:
                print('ID inválido!')
            else:
                break

    def consultar_acervo(self):
        while True:
            print("""Filtrar por:
[1] Titulo
[2] Autor
[3] Gênero
[4] Encerrar consulta""")
            try:
                self.alternativa = int(input('opção: '))
            except ValueError:
                print('opção inválida')
            else:
                match self.alternativa:
                    case 1:
                        self.consulta = 'select * from acervo where s_titulo_acervo=%s;'
                        self.title = (str(input('Título do livro: ')).strip(),)
                        self.crsor.execute(self.consulta, self.title)
                        self.result = self.crsor.fetchall()
                        print("|ID| Título | Autor | Gênero | Status | Quantidade | membro")
                        print()
                        for campo in self.result:
                            ide, titulo, autor, genero, status, quantidade, membro = campo
                            print(ide, titulo, autor, genero, status, quantidade, membro)
                    case 2:
                        self.pesquisa = 'select * from acervo where s_autor_acervo=%s;'
                        self.author = (str(input('Autor do livro')).strip(),)
                        self.crsor.execute(self.pesquisa, self.author)
                        self.result = self.crsor.fetchall()
                        print("|ID| Título | Autor | Gênero | Status | Quantidade | membro")
                        print()
                        for campo in self.result:
                            ide, titulo, autor, genero, status, quantidade, membro = campo
                            print(ide, titulo, autor, genero, status, quantidade, membro)
                    case 3:
                        self.procura = 'select * from acervo where s_genero_acervo=%s;'
                        self.genre = (str(input('Gênero do livro: ')).strip(),)
                        self.crsor.execute(self.procura, self.genre)
                        self.result = self.crsor.fetchall()
                        print("|ID| Título | Autor | Gênero | Status | Quantidade | membro")
                        print()
                        for campo in self.result:
                            ide, titulo, autor, genero, status, quantidade, membro = campo
                            print(ide, titulo, autor, genero, status, quantidade, membro)
                    case 4:
                        break

    def consultar_membros(self):
        while True:
            print("""Filtrar por:
[1] Nome
[2] Código
[3] Encerrar consulta""")
            try:
                self.optacao = int(input('opção: '))
            except ValueError:
                print('opção inválida')
            else:
                match self.optacao:
                    case 1:
                        self.pesquisa = 'select * from membros where s_nome_membros=%s;'
                        self.nome = (str(input('Nome do membro: ')).strip(),)
                        self.crsor.execute(self.pesquisa, self.nome)
                        self.result = self.crsor.fetchall()
                        print(
                            "|ID| Nome | Código | livros emprestados | Data do empréstimo | Nome do livro emprestado |")
                        print()
                        for campo in self.result:
                            ide, nome, codigo, livro_emprestado, data_emprestimo, nome_livro_emprestado = campo
                            print(ide, nome, codigo, livro_emprestado, data_emprestimo, nome_livro_emprestado)
                    case 2:
                        self.pesquisa = 'select * from membros where i_codigo_membros=%s;'
                        self.code = (str(input('Código do membro: ')).strip(),)
                        self.crsor.execute(self.pesquisa, self.code)
                        self.result = self.crsor.fetchall()
                        print(
                            "|ID| Nome | Código | livros emprestados | Data do empréstimo | Nome do livro emprestado |")
                        print()
                        for campo in self.result:
                            ide, nome, codigo, livro_emprestado, data_emprestimo, nome_livro_emprestado = campo
                            print(ide, nome, codigo, livro_emprestado, data_emprestimo, nome_livro_emprestado)
                    case 3:
                        break


# Main Program

conex = mysql.connector.connect(
    host='localhost',
    user='root',
    password=os.getenv('senha'),
    database='meusql'
)

cursor = conex.cursor()

horario_atual = datetime.now().time()
horario_abertura = datetime.now().strptime('7:00', '%H:%M').time()
horario_fechamento = datetime.strptime('3:00', '%H:%M').time()

while datetime.strptime('7:00', '%H:%M').time() <= datetime.now().time() <= datetime.strptime('23:00', '%H:%M').time():
    biblioteca = Biblioteca(cursor)
    biblioteca.menu()
    try:
        opcao = int(input('opção: '))
    except ValueError:
        print('Insira somente números inteiros')
    else:
        match opcao:
            case 1:
                name = str(input('Nome do membro: ')).strip()
                member = Membro(name, cursor)
                member.cadastrar_membro()
                conex.commit()
            case 2:
                Titulo = str(input('Título do livro: ')).strip()
                Autor = str(input('Autor: ')).strip()
                Genero = str(input('Gênero: ')).strip()
                livreto = Livro(Titulo, Autor, Genero)
                biblioteca.cadastrar_livro(livreto)
                conex.commit()
            case 3:
                while True:
                    print("""
                    1. Excluir livro
                    2. Excluir membro
                    """)
                    escolha = str(input('Opção: ')).strip()
                    if escolha in '1':
                        print('Consulte o livro que deseja deletar o cadastro.')
                        biblioteca.consultar_acervo()
                        titulx = str(input('Título do livro: ')).strip()
                        autxr = str(input('Autor: ')).strip()
                        generx = str(input('Gênero: ')).strip()
                        book = Livro(titulx, autxr, generx)
                        biblioteca.excluir_livro(book)
                        conex.commit()
                        break
                    elif escolha in '2':
                        print('Consulte o membro que deseja deletar o cadastro.')
                        biblioteca.consultar_membros()
                        nxme = str(input('Nome do membro: ')).strip()
                        membrx = Membro(nxme, cursor)
                        biblioteca.excluir_membro(membrx)
                        conex.commit()
                        break
                    else:
                        print('opção inválida')
            case 4:
                nume = str(input('Nome do membro: ')).strip()
                mebro = Membro(nume, cursor)
                biblioteca.emprestar_livro(mebro)
                conex.commit()
            case 5:
                biblioteca.consultar_acervo()
                biblioteca.aceitar_devolucao()
                conex.commit()
            case 6:
                break
