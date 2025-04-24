from tkinter import *
from tkinter import ttk
import sqlite3

janela = Tk()

class Funcs():
    def limpa_label(self):
        self.Matricula_entry.delete(0, END)
        self.Nome_entry.delete(0, END)
        self.Turma_entry.delete(0, END)
        self.Turno_entry.delete(0, END)
        self.Av1_entry.delete(0, END)
        self.Av2_entry.delete(0, END)
        self.Av3_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("alunos.bd")
        self.cursor = self.conn.cursor()
        print("Conectando ao banco de notas")

    def desconecta_bd(self):
        self.conn.close()
        print("Desconectando do banco de notas")

    def montaNotas(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                mat INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_aluno CHAR(40) NOT NULL,
                turma CHAR(1),
                turno CHAR(3),
                av1 REAL,
                av2 REAL,
                av3 REAL,
                situacao CHAR(15)
            );
        """)
        self.conn.commit()
        print("Banco de notas criado")
        self.desconecta_bd()

    def cadastra_notas(self):
        self.Nome = self.Nome_entry.get()
        self.Turma = self.Turma_entry.get()
        self.Turno = self.Turno_entry.get()
        av1 = float(self.Av1_entry.get())
        av2 = float(self.Av2_entry.get())
        av3 = float(self.Av3_entry.get())

        media = (av1 + av2 + av3) / 3

        if media >= 6:
            situacao = "Aprovado"
        elif media <= 5:
            situacao = "Reprovado"
        else:
            situacao = "Recuperacao"

        self.conecta_bd()
        self.cursor.execute("""
            INSERT INTO alunos(nome_aluno, turma, turno, av1, av2, av3, situacao)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (self.Nome, self.Turma, self.Turno, av1, av2, av3, situacao))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_label()

    def select_lista(self):
        self.listaAluno.delete(*self.listaAluno.get_children())
        self.conecta_bd()
        Lista = self.cursor.execute("""
            SELECT mat, nome_aluno, turma, turno, situacao FROM alunos
            ORDER BY nome_aluno ASC; """)
        for i in Lista:
            self.listaAluno.insert("", END, values=i)
        self.desconecta_bd()

    def OnDoubleClick(self, event):
        self.limpa_label()
        self.listaSelecionada = self.listaAluno.focus()
        valores = self.listaAluno.item(self.listaSelecionada, 'values')
        if valores:
            self.Matricula_entry.insert(END, valores[0])
            self.Nome_entry.insert(END, valores[1])
            self.Turma_entry.insert(END, valores[2])
            self.Turno_entry.insert(END, valores[3])

    def deleta_aluno(self):
        self.conecta_bd()
        mat = self.Matricula_entry.get()
        self.cursor.execute("DELETE FROM alunos WHERE mat=?", (mat,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_label()
        self.select_lista()

    def consultar_aluno(self):
        nome = self.codigo_entry.get()
        self.conecta_bd()
        self.cursor.execute("SELECT * FROM alunos WHERE Mat LIKE ?", ('%' + nome + '%',))
        resultado = self.cursor.fetchone()
        self.desconecta_bd()

        if resultado:
            info = f"\nMatricula: {resultado[0]}\nNome: {resultado[1]}\nTurma: {resultado[2]}\nTurno: {resultado[3]}\nAv1: {resultado[4]}\nAv2: {resultado[5]}\nAv3: {resultado[6]}\nSituação: {resultado[7]}"
        else:
            info = "Aluno não encontrado."

        self.resultado_label.config(text=info)

class Application(Funcs):
    def __init__(self):
        self.janela = janela
        self.tela()
        self.frame_de_tela()
        self.criando_botoes()
        self.lista_frame_consulta()
        self.montaNotas()
        self.select_lista()
        self.listaAluno.bind("<Double-1>", self.OnDoubleClick)
        janela.mainloop()

    def tela(self):
        self.janela.title("Cadastro de Alunos")
        self.janela.configure(background='#f5f7fa')
        self.janela.geometry("1200x450")
        self.janela.resizable(False, False)

    def frame_de_tela(self):
        self.frame_cadastro = Frame(self.janela, bd=4, bg='#D6DBDF', highlightthickness=3, highlightbackground='#a9a9a9')
        self.frame_cadastro.place(relx=0.02, rely=0.02, relwidth=0.46, relheight= 0.96)

        self.frame_consulta = Frame(self.janela, bd=4, bg='#D6DBDF', highlightthickness=3, highlightbackground='#a9a9a9')
        self.frame_consulta.place(relx=0.52, rely=0.02, relwidth=0.46, relheight= 0.96)

    def criando_botoes(self):
        self.bt_cadastrar = Button(self.frame_cadastro, text='Cadastrar', bd=3, bg='#10b981', command=self.cadastra_notas)
        self.bt_cadastrar.place(relx= 0.25 , rely=0.45 , relwidth=0.5 , relheight=0.1)

        self.bt_limpar = Button(self.frame_cadastro, text='Limpar', bd=2, bg='#FFFF00', command=self.limpa_label)
        self.bt_limpar.place(relx= 0.65 , rely=0.35 , relwidth=0.19 , relheight=0.05)

        self.bt_consultar = Button(self.frame_cadastro, text='Consultar', bd=3, bg='#f59e0b', command=self.consultar_aluno)
        self.bt_consultar.place(relx= 0.0 , rely=0.6 , relwidth=0.20 , relheight=0.05)

        self.codigo_entry = Entry(self.frame_cadastro)
        self.codigo_entry.place (relx=0.2, rely=0.6, relheight=0.05, relwidth=0.3)

        self.resultado_label = Label(self.frame_cadastro, text='', bg='#D6DBDF', justify=LEFT)
        self.resultado_label.place(relx=0.05, rely=0.7, relwidth=0.9, relheight=0.25)

        self.bt_apagar = Button(self.frame_cadastro, text='Apagar', bd=3, bg='#ef4444', command=self.deleta_aluno)
        self.bt_apagar.place(relx= 0.8 , rely=0.6 , relwidth=0.20 , relheight=0.05)

        self.lb_Matricula = Label(self.frame_cadastro, text='Matricula', bg='#D6DBDF', fg='#34495E')
        self.lb_Matricula.place(relx=0.05 , rely=0.05)

        self.Matricula_entry = Entry(self.frame_cadastro, bg='#ffffff')
        self.Matricula_entry.place (relx=0.05, rely=0.1, relheight=0.05)

        self.lb_Turma = Label(self.frame_cadastro, text='Turma', bg='#D6DBDF', fg='#34495E')
        self.lb_Turma.place(relx=0.65 , rely=0.05)

        self.Turma_entry = Entry(self.frame_cadastro, bg='#ffffff')
        self.Turma_entry.place (relx=0.65, rely=0.1, relheight=0.05, relwidth=0.095)

        self.lb_Nome = Label(self.frame_cadastro, text='Nome', bg='#D6DBDF', fg='#34495E')
        self.lb_Nome.place(relx=0.05 , rely=0.2)

        self.Nome_entry = Entry(self.frame_cadastro, bg='#ffffff')
        self.Nome_entry.place (relx=0.05, rely=0.25, relheight=0.05, relwidth=0.5)

        self.lb_Turno = Label(self.frame_cadastro, text='Turno', bg='#D6DBDF', fg='#34495E')
        self.lb_Turno.place(relx=0.65 , rely=0.2)

        self.Turno_entry = Entry(self.frame_cadastro, bg='#ffffff')
        self.Turno_entry.place (relx=0.65, rely=0.25, relheight=0.05, relwidth=0.3)

        self.lb_av1 = Label(self.frame_cadastro, text='Av1', bg='#D6DBDF', fg='#34495E')
        self.lb_av1.place(relx=0.05 , rely=0.3, relwidth=0.1)

        self.Av1_entry = Entry(self.frame_cadastro, bg='#ffffff')
        self.Av1_entry.place (relx=0.05, rely=0.35, relheight=0.05, relwidth=0.1)

        self.lb_av2 = Label(self.frame_cadastro, text='Av2', bg='#D6DBDF', fg='#34495E')
        self.lb_av2.place(relx=0.25 , rely=0.3, relwidth=0.1)

        self.Av2_entry = Entry(self.frame_cadastro, bg='#ffffff')
        self.Av2_entry.place (relx=0.25, rely=0.35, relheight=0.05, relwidth=0.1)

        self.lb_av3 = Label(self.frame_cadastro, text='Av3', bg='#D6DBDF', fg='#34495E')
        self.lb_av3.place(relx=0.45 , rely=0.3, relwidth=0.1)

        self.Av3_entry = Entry(self.frame_cadastro, bg='#ffffff')
        self.Av3_entry.place (relx=0.45, rely=0.35, relheight=0.05, relwidth=0.1)

    def lista_frame_consulta(self):
        self.listaAluno = ttk.Treeview(self.frame_consulta, height=3, columns=("col1","col2","col3","col4", "col5"))
        self.listaAluno.heading("#0", text="")
        self.listaAluno.heading("#1", text="Matricula")
        self.listaAluno.heading("#2", text="Nome")
        self.listaAluno.heading("#3", text="Turma")
        self.listaAluno.heading("#4", text="Turno")
        self.listaAluno.heading("#5", text="Situação")

        self.listaAluno.column("#0", width=0)
        self.listaAluno.column("#1", width=50)
        self.listaAluno.column("#2", width=150)
        self.listaAluno.column("#3", width=50)
        self.listaAluno.column("#4", width=50)
        self.listaAluno.column("#5", width=100)

        self.listaAluno.place(relx=0.01, rely=0.01, relwidth=0.96, relheight=0.99)

        self.scroolLista = Scrollbar(self.frame_consulta, orient='vertical')
        self.listaAluno.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.01, relwidth=0.04, relheight=0.99)

Application()
