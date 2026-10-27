
import tkinter as tk
from tkinter import messagebox
import random

USUARIO = "aluno"
SENHA = "1234"

tema_escuro = True
historico = []

CORES = {
    "escuro": {
        "fundo": "#202330",
        "texto": "#f1f3f9",
        "secundario": "#a4abc0",
        "usuario": "#343b55",
        "ia": "#303441",
        "entrada": "#303545",
        "botao": "#6658d3"
    },
    "claro": {
        "fundo": "#f2f3f8",
        "texto": "#222536",
        "secundario": "#686d80",
        "usuario": "#e0e3ff",
        "ia": "#ffffff",
        "entrada": "#ffffff",
        "botao": "#6658d3"
    }
}

def responder(pergunta):
    pergunta = pergunta.lower()

    if "python" in pergunta:
        return "Python é uma linguagem de programação usada em automação, sites e inteligência artificial."
    elif "java" in pergunta:
        return "Java é uma linguagem orientada a objetos, usada em sistemas e aplicações."
    elif "html" in pergunta:
        return "HTML define a estrutura das páginas web, como títulos, textos, imagens e links."
    elif "css" in pergunta:
        return "CSS é usado para definir cores, fontes, espaçamentos e layouts de páginas web."
    elif "javascript" in pergunta:
        return "JavaScript adiciona interatividade aos sites, como menus, botões e validações."
    elif "banco de dados" in pergunta or "mysql" in pergunta or "sql" in pergunta:
        return "Bancos de dados armazenam informações. SQL permite consultar e modificar dados em bancos relacionais."
    elif "php" in pergunta:
        return "PHP é uma linguagem usada no desenvolvimento web, principalmente no lado do servidor."
    elif "api" in pergunta:
        return "Uma API permite que diferentes sistemas se comuniquem e troquem informações."
    elif "algoritmo" in pergunta:
        return "Um algoritmo é uma sequência de instruções para resolver um problema."
    elif "variável" in pergunta or "variavel" in pergunta:
        return "Uma variável armazena um valor. Em Python, por exemplo: idade = 16."
    elif "oi" in pergunta or "olá" in pergunta or "ola" in pergunta:
        return "Olá! Sou o TechIA. Pode perguntar sobre programação e tecnologia."
    elif "obrigado" in pergunta or "obrigada" in pergunta:
        return "Por nada! Pode enviar sua próxima dúvida de TI."
    else:
        return "Ainda não tenho uma resposta programada para isso. Tente perguntar sobre Python, Java, HTML, CSS, SQL ou APIs."

def login():
    if campo_usuario.get().strip() == USUARIO and campo_senha.get() == SENHA:
        janela.destroy()
        abrir_chat()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def abrir_chat():
    global tema_escuro, historico

    chat = tk.Tk()
    chat.title("TechIA")
    chat.geometry("900x620")
    chat.minsize(650, 450)

    topo = tk.Frame(chat, padx=18, pady=14)
    topo.pack(fill="x")

    titulo = tk.Label(topo, text="TechIA", font=("Arial", 20, "bold"))
    titulo.pack(side="left")

    subtitulo = tk.Label(topo, text="Assistente de tecnologia")
    subtitulo.pack(side="left", padx=12, pady=6)

    botoes = tk.Frame(topo)
    botoes.pack(side="right")

    area = tk.Frame(chat, padx=18, pady=10)
    area.pack(fill="both", expand=True)

    canvas = tk.Canvas(area, highlightthickness=0)
    barra = tk.Scrollbar(area, command=canvas.yview)
    mensagens = tk.Frame(canvas)

    janela_mensagens = canvas.create_window(
        (0, 0), window=mensagens, anchor="nw"
    )

    canvas.configure(yscrollcommand=barra.set)
    canvas.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")

    def atualizar_area(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfigure(janela_mensagens, width=canvas.winfo_width())

    mensagens.bind("<Configure>", atualizar_area)
    canvas.bind("<Configure>", atualizar_area)

    rodape = tk.Frame(chat, padx=18, pady=14)
    rodape.pack(fill="x")

    entrada = tk.Entry(rodape, font=("Arial", 12), relief="flat")
    entrada.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))

    def mostrar(nome, icone, mensagem, tipo):
        c = CORES["escuro"] if tema_escuro else CORES["claro"]

        linha = tk.Frame(mensagens, bg=c["fundo"], pady=7)
        linha.pack(fill="x")

        cor = c["usuario"] if tipo == "usuario" else c["ia"]
        lado = "e" if tipo == "usuario" else "w"

        bloco = tk.Frame(linha, bg=cor, padx=12, pady=9)
        bloco.pack(anchor=lado, padx=(60, 0) if tipo == "usuario" else (0, 60))

        tk.Label(
            bloco,
            text=f"{icone}  {nome}",
            font=("Arial", 10, "bold"),
            bg=cor,
            fg=c["texto"]
        ).pack(anchor="w")

        tk.Label(
            bloco,
            text=mensagem,
            font=("Arial", 11),
            bg=cor,
            fg=c["texto"],
            wraplength=600,
            justify="left",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))

        canvas.after(50, lambda: canvas.yview_moveto(1))

    def reconstruir():
        for item in mensagens.winfo_children():
            item.destroy()

        for nome, icone, mensagem, tipo in historico:
            mostrar(nome, icone, mensagem, tipo)

    def enviar(event=None):
        pergunta = entrada.get().strip()

        if not pergunta or botao_enviar["state"] == "disabled":
            return

        entrada.delete(0, "end")
        historico.append(("Você", "U", pergunta, "usuario"))
        reconstruir()

        botao_enviar.configure(state="disabled")
        entrada.configure(state="disabled")
        status.configure(text="TechIA está preparando uma resposta...")

        def responder_depois():
            historico.append(("TechIA", "T", responder(pergunta), "ia"))
            reconstruir()
            botao_enviar.configure(state="normal")
            entrada.configure(state="normal")
            entrada.focus_set()
            status.configure(text="Assistente de tecnologia")

        chat.after(random.randint(600, 1000), responder_depois)

    def limpar():
        historico.clear()
        reconstruir()
        status.configure(text="Conversa limpa.")
        entrada.focus_set()

    def alternar_tema():
        global tema_escuro
        tema_escuro = not tema_escuro
        aplicar_tema()

    def aplicar_tema():
        c = CORES["escuro"] if tema_escuro else CORES["claro"]
        chat.configure(bg=c["fundo"])

        for frame in (topo, botoes, area, rodape, mensagens):
            frame.configure(bg=c["fundo"])

        titulo.configure(bg=c["fundo"], fg=c["texto"])
        subtitulo.configure(bg=c["fundo"], fg=c["secundario"])
        canvas.configure(bg=c["fundo"])
        entrada.configure(
            bg=c["entrada"],
            fg=c["texto"],
            insertbackground=c["texto"]
        )
        status.configure(bg=c["fundo"], fg=c["secundario"])

        botao_limpar.configure(
            bg=c["ia"], fg=c["texto"],
            activebackground=c["usuario"]
        )
        botao_tema.configure(
            bg=c["ia"], fg=c["texto"],
            activebackground=c["usuario"],
            text="Modo claro" if tema_escuro else "Modo escuro"
        )
        botao_enviar.configure(
            bg=c["botao"], fg="white",
            activebackground="#5143b5"
        )

        reconstruir()

    botao_limpar = tk.Button(
        botoes, text="Limpar", relief="flat",
        padx=12, pady=7, command=limpar
    )
    botao_limpar.pack(side="left", padx=4)

    botao_tema = tk.Button(
        botoes, text="Modo claro", relief="flat",
        padx=12, pady=7, command=alternar_tema
    )
    botao_tema.pack(side="left", padx=4)

    botao_enviar = tk.Button(
        rodape, text="Enviar", relief="flat",
        padx=20, pady=9, command=enviar
    )
    botao_enviar.pack(side="right")

    status = tk.Label(rodape, text="Assistente de tecnologia")
    status.pack(side="bottom", anchor="w", pady=(8, 0))

    entrada.bind("<Return>", enviar)

    historico.append((
        "TechIA", "T",
        "Olá! Sou o TechIA. Faça uma pergunta sobre programação ou tecnologia.",
        "ia"
    ))

    aplicar_tema()
    entrada.focus_set()
    chat.mainloop()

janela = tk.Tk()
janela.title("TechIA - Login")
janela.geometry("350x300")
janela.resizable(False, False)
janela.configure(bg="#202330")

tk.Label(
    janela, text="TechIA",
    font=("Arial", 24, "bold"),
    bg="#202330", fg="#f1f3f9"
).pack(pady=20)

tk.Label(
    janela, text="Usuário",
    bg="#202330", fg="#f1f3f9"
).pack()

campo_usuario = tk.Entry(janela)
campo_usuario.pack(pady=5)

tk.Label(
    janela, text="Senha",
    bg="#202330", fg="#f1f3f9"
).pack()

campo_senha = tk.Entry(janela, show="*")
campo_senha.pack(pady=5)

tk.Button(
    janela, text="Entrar",
    command=login, width=20
).pack(pady=20)

janela.bind("<Return>", lambda event: login())
janela.mainloop()
