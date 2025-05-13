# -*- coding: utf-8 -*-
# interface_mochila.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import mochila_genetico # importando o módulo do algoritmo genético
import random

# --- configuração da interface estilo anos 80 (synthwave/outrun) ---
COR_FUNDO_PRINCIPAL = "#0D0221" # Roxo espacial / Azul muito escuro
COR_FUNDO_SECUNDARIO = "#2A1B3D" # Roxo escuro um pouco mais claro
COR_CONTORNO_FRAMES = "#FF00FF" # Magenta Neon
COR_TEXTO_PRINCIPAL = "#00FFFF" # Ciano Neon
COR_TEXTO_DESTAQUE = "#FFFF00" # Amarelo Neon
COR_BOTAO_FUNDO = "#4A4063" # Roxo acinzentado escuro
COR_BOTAO_TEXTO = "#00FFFF" # Ciano Neon
COR_BOTAO_HOVER_FUNDO = "#FF00FF" # Magenta Neon
COR_BOTAO_HOVER_TEXTO = "#0D0221" # Fundo Principal (para contraste)
COR_ENTRADA_FUNDO = "#1A102E" # Roxo bem escuro
COR_ENTRADA_TEXTO = "#00FFFF" # Ciano Neon
COR_CANVAS_FUNDO = "#000033" # Azul noite escuro
CORES_ITENS_MOCHILA = ["#FF69B4", "#39FF14", "#FFA500", "#7FFF00", "#F4D03F", "#00E5EE"]

FONTE_PRINCIPAL_80S = ("Courier New", 10)
FONTE_TITULO_80S = ("Courier New", 11, "bold") # Levemente menor para caber melhor como título de frame
FONTE_LABEL_ENTRADA_80S = ("Courier New", 9) # Fonte para labels dos campos de entrada
FONTE_BOTAO_80S = ("Courier New", 10, "bold")
FONTE_TEXTO_AREA_80S = ("Courier New", 10)

class AplicacaoMochila:
    def __init__(self, master):
        self.master = master
        master.title("MOCHILA RADICAL 80s - GENETIC ALGORITHM")
        master.configure(bg=COR_FUNDO_PRINCIPAL)
        master.geometry("950x800") # Aumentado um pouco mais para garantir espaço
        master.minsize(900, 750)

        self.itens_para_algoritmo = []
        self.canvas_itens_mochila = None
        self.id_animacao_atual = None
        self.label_geracao_atual = None 

        style = ttk.Style()
        style.theme_use("default") 

        style.configure("TFrame", background=COR_FUNDO_SECUNDARIO)
        style.configure("TLabel", background=COR_FUNDO_SECUNDARIO, foreground=COR_TEXTO_PRINCIPAL, font=FONTE_LABEL_ENTRADA_80S) # Usar fonte específica para labels de entrada
        style.configure("Title.TLabel", background=COR_FUNDO_SECUNDARIO, foreground=COR_TEXTO_DESTAQUE, font=FONTE_TITULO_80S) # Para títulos de seção internos, se necessário
        style.configure("TButton", font=FONTE_BOTAO_80S, foreground=COR_BOTAO_TEXTO, background=COR_BOTAO_FUNDO,
                        relief="raised", borderwidth=2, bordercolor=COR_CONTORNO_FRAMES)
        style.map("TButton",
            background=[("active", COR_BOTAO_HOVER_FUNDO), ("pressed", COR_BOTAO_HOVER_FUNDO), ("hover", COR_BOTAO_HOVER_FUNDO)],
            foreground=[("active", COR_BOTAO_HOVER_TEXTO), ("pressed", COR_BOTAO_HOVER_TEXTO), ("hover", COR_BOTAO_HOVER_TEXTO)],
            relief=[("pressed", "sunken"), ("hover", "raised")]
        )
        style.configure("TEntry", fieldbackground=COR_ENTRADA_FUNDO, foreground=COR_ENTRADA_TEXTO, font=FONTE_PRINCIPAL_80S,
                        insertbackground=COR_TEXTO_PRINCIPAL, borderwidth=2, relief="sunken")

        main_outer_frame = tk.Frame(master, bg=COR_CONTORNO_FRAMES, bd=3, relief="solid")
        main_outer_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_inner_frame = tk.Frame(main_outer_frame, bg=COR_FUNDO_PRINCIPAL, bd=0)
        main_inner_frame.pack(fill="both", expand=True, padx=2, pady=2)

        top_frame = ttk.Frame(main_inner_frame, style="TFrame", padding="10 10 10 10")
        top_frame.pack(pady=10, padx=10, fill="x")

        left_column_frame = ttk.Frame(top_frame, style="TFrame", width=380) # Aumentar largura da coluna esquerda
        left_column_frame.pack(side="left", fill="y", padx=(0,15), anchor="n") # Aumentar padx
        left_column_frame.pack_propagate(False)

        def criar_retro_labelframe(parent, texto):
            # Usar tk.Frame para simular LabelFrame com mais controle de estilo no título
            container = tk.Frame(parent, bg=COR_FUNDO_SECUNDARIO, bd=2, relief="solid", highlightbackground=COR_CONTORNO_FRAMES, highlightcolor=COR_CONTORNO_FRAMES, highlightthickness=2)
            
            title_label = tk.Label(container, text=f" {texto} ", font=FONTE_TITULO_80S, 
                                   fg=COR_TEXTO_DESTAQUE, bg=COR_FUNDO_SECUNDARIO, anchor="w")
            title_label.pack(fill="x", padx=5, pady=(2,5)) # pady para dar espaço ao redor do título
            
            # Linha decorativa abaixo do título
            # separator = tk.Frame(container, height=2, bg=COR_CONTORNO_FRAMES)
            # separator.pack(fill='x', padx=5, pady=(0,5))
            return container

        frame_itens_container = criar_retro_labelframe(left_column_frame, "ADICIONAR ITEM")
        frame_itens_container.pack(pady=10, padx=5, fill="x")
        # Frame interno para o grid, para não afetar o título do LabelFrame simulado
        frame_itens = ttk.Frame(frame_itens_container, style="TFrame", padding=(10,5,10,10))
        frame_itens.pack(fill="x")
        frame_itens.columnconfigure(1, weight=1)

        ttk.Label(frame_itens, text="NOME:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome_item = ttk.Entry(frame_itens, width=25, style="TEntry")
        self.entry_nome_item.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_nome_item.insert(0, "RAD_ITEM")
        ttk.Label(frame_itens, text="PESO:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_peso_item = ttk.Entry(frame_itens, width=12, style="TEntry")
        self.entry_peso_item.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(frame_itens, text="VALOR:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_valor_item = ttk.Entry(frame_itens, width=12, style="TEntry")
        self.entry_valor_item.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.btn_adicionar_item = ttk.Button(frame_itens, text="ADD ITEM", command=self.adicionar_item_lista, style="TButton")
        self.btn_adicionar_item.grid(row=3, column=0, columnspan=2, pady=10)

        frame_geradores_container = criar_retro_labelframe(left_column_frame, "GERAR ITENS")
        frame_geradores_container.pack(pady=10, padx=5, fill="x")
        frame_geradores = ttk.Frame(frame_geradores_container, style="TFrame", padding=(10,5,10,10))
        frame_geradores.pack(fill="x")
        frame_geradores.columnconfigure(1, weight=1) # Add for entry to expand if needed
        self.btn_gerar_padrao = ttk.Button(frame_geradores, text="LOAD TEST SET (10)", command=self.gerar_itens_padrao, style="TButton")
        self.btn_gerar_padrao.pack(pady=5, fill="x", padx=5)

        # New: Label and Entry for number of random items
        frame_qtd_random = ttk.Frame(frame_geradores, style="TFrame") # A sub-frame for label and entry
        frame_qtd_random.pack(fill="x", pady=(5,0), padx=5) # Pack it before the button
        
        lbl_qtd_aleatorios = ttk.Label(frame_qtd_random, text="QTD ITENS RAND:")
        lbl_qtd_aleatorios.pack(side="left", padx=(0,5))

        self.entry_qtd_aleatorios = ttk.Entry(frame_qtd_random, width=5, style="TEntry") # width 5 should be enough
        self.entry_qtd_aleatorios.pack(side="left", fill="x", expand=True)
        self.entry_qtd_aleatorios.insert(0, "5") # Default value

        # Modified button: text changed, command remains the same, but the method will be modified
        self.btn_gerar_aleatorios = ttk.Button(frame_geradores, text="ADD RANDOM ITEMS", command=self.gerar_itens_aleatorios, style="TButton")
        self.btn_gerar_aleatorios.pack(pady=5, fill="x", padx=5)

        frame_parametros_container = criar_retro_labelframe(left_column_frame, "ALGORITHM SETUP")
        frame_parametros_container.pack(pady=10, padx=5, fill="x")
        frame_parametros = ttk.Frame(frame_parametros_container, style="TFrame", padding=(10,5,10,10))
        frame_parametros.pack(fill="x")
        frame_parametros.columnconfigure(1, weight=1)
        param_labels_keys = [
            ("CAPACIDADE:", "capacidade_mochila"),
            ("POPULACAO:", "tam_populacao"),
            ("GERACOES:", "n_geracoes"),
            ("MUTACAO (0-1):", "taxa_mutacao_0-1"),
            ("TORNEIO:", "tam_torneio")
        ]
        param_defaults = ["100", "50", "100", "0.02", "5"]
        self.param_entries = {}
        for i, (label_text, key) in enumerate(param_labels_keys):
            lbl = ttk.Label(frame_parametros, text=label_text)
            lbl.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(frame_parametros, width=12, style="TEntry")
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entry.insert(0, param_defaults[i])
            self.param_entries[key] = entry

        right_column_frame = ttk.Frame(top_frame, style="TFrame")
        right_column_frame.pack(side="left", fill="both", expand=True)

        frame_lista_itens_container = criar_retro_labelframe(right_column_frame, "ITENS DISPONIVEIS")
        frame_lista_itens_container.pack(pady=10, padx=5, fill="both", expand=True)
        frame_lista_itens = ttk.Frame(frame_lista_itens_container, style="TFrame", padding=(10,5,10,10))
        frame_lista_itens.pack(fill="both", expand=True)
        self.texto_itens_adicionados = scrolledtext.ScrolledText(frame_lista_itens, width=45, height=10, 
                                                               font=FONTE_TEXTO_AREA_80S, 
                                                               bg=COR_ENTRADA_FUNDO, fg=COR_TEXTO_PRINCIPAL,
                                                               relief="solid", borderwidth=2,
                                                               highlightbackground=COR_CONTORNO_FRAMES, highlightcolor=COR_CONTORNO_FRAMES)
        self.texto_itens_adicionados.pack(pady=5, padx=5, fill="both", expand=True)
        self.texto_itens_adicionados.configure(state="disabled", insertbackground=COR_TEXTO_PRINCIPAL)
        self.btn_limpar_itens = ttk.Button(frame_lista_itens, text="CLEAR LIST", command=self.limpar_lista_itens, style="TButton")
        self.btn_limpar_itens.pack(pady=10)

        frame_mochila_grafica_container = criar_retro_labelframe(right_column_frame, "MOCHILA CONTEUDO (GRAFICO)")
        frame_mochila_grafica_container.pack(pady=10, padx=5, fill="both", expand=True)
        frame_mochila_grafica = ttk.Frame(frame_mochila_grafica_container, style="TFrame", padding=(5,5,5,5))
        frame_mochila_grafica.pack(fill="both", expand=True)
        self.canvas_itens_mochila = tk.Canvas(frame_mochila_grafica, bg=COR_CANVAS_FUNDO, 
                                              relief="solid", borderwidth=2, highlightthickness=0)
        self.canvas_itens_mochila.pack(fill="both", expand=True, padx=5, pady=5)
        self.master.after(50, self.desenhar_mochila_vazia)

        self.label_geracao_atual = ttk.Label(frame_mochila_grafica, text="GERACAO: 0", style="Title.TLabel", foreground=COR_TEXTO_DESTAQUE)
        self.label_geracao_atual.pack(pady=(5,2)) # Adicionado pady para espaço

        bottom_frame = ttk.Frame(main_inner_frame, style="TFrame", padding="10 10 10 10")
        bottom_frame.pack(pady=10, padx=10, fill="x")
        self.btn_executar_ag = ttk.Button(bottom_frame, text=">>> RUN GENETIC ALGORITHM <<<", command=self.executar_algoritmo_genetico, style="TButton")
        self.btn_executar_ag.pack(pady=10, ipady=8, ipadx=15)

        frame_resultado_container = criar_retro_labelframe(bottom_frame, "RESULTADO DA OTIMIZACAO")
        frame_resultado_container.pack(pady=10, fill="x", expand=True)
        frame_resultado = ttk.Frame(frame_resultado_container, style="TFrame", padding=(10,5,10,10))
        frame_resultado.pack(fill="x", expand=True)
        self.texto_resultado = scrolledtext.ScrolledText(frame_resultado, width=70, height=6, 
                                                       font=FONTE_TEXTO_AREA_80S, 
                                                       bg=COR_ENTRADA_FUNDO, fg=COR_TEXTO_DESTAQUE, 
                                                       relief="solid", borderwidth=2,
                                                       highlightbackground=COR_CONTORNO_FRAMES, highlightcolor=COR_CONTORNO_FRAMES)
        self.texto_resultado.pack(pady=5, padx=5, fill="x", expand=True)
        self.texto_resultado.configure(state="disabled", insertbackground=COR_TEXTO_PRINCIPAL)
        
        self.carregar_itens_exemplo()

    def feedback_geracao(self, geracao_num, melhor_fitness_geracao):
        self.label_geracao_atual.config(text=f"GER: {geracao_num} | BEST: {melhor_fitness_geracao:.2f}")
        original_color = self.canvas_itens_mochila.cget("bg")
        self.canvas_itens_mochila.config(bg=COR_TEXTO_DESTAQUE)
        self.master.update_idletasks() 
        self.master.after(50, lambda: self.canvas_itens_mochila.config(bg=original_color))
        self.master.update_idletasks()

    def gerar_itens_padrao(self):
        self.limpar_lista_itens(confirmar=False)
        itens_padrao = [
            {"nome": "VINYL_LP", "peso": 4, "valor": 50, "cor": CORES_ITENS_MOCHILA[0]},
            {"nome": "KEYTAR", "peso": 2, "valor": 65, "cor": CORES_ITENS_MOCHILA[1]},
            {"nome": "ARCADE_JOY", "peso": 3, "valor": 40, "cor": CORES_ITENS_MOCHILA[2]},
            {"nome": "CASSETTE", "peso": 5, "valor": 70, "cor": CORES_ITENS_MOCHILA[3]},
            {"nome": "BOOMBOX", "peso": 1, "valor": 25, "cor": CORES_ITENS_MOCHILA[4]},
            {"nome": "GAME_CART", "peso": 2, "valor": 30, "cor": CORES_ITENS_MOCHILA[5]},
            {"nome": "NEON_SIGN", "peso": 1, "valor": 15, "cor": CORES_ITENS_MOCHILA[0]},
            {"nome": "ROBO_TOY", "peso": 6, "valor": 60, "cor": CORES_ITENS_MOCHILA[1]},
            {"nome": "VHS_TAPE", "peso": 1, "valor": 35, "cor": CORES_ITENS_MOCHILA[2]},
            {"nome": "SYNTH_MOD", "peso": 3, "valor": 55, "cor": CORES_ITENS_MOCHILA[3]}
        ]
        self.itens_para_algoritmo = itens_padrao
        self.atualizar_display_itens()
        messagebox.showinfo("ITENS GERADOS", "10 ITENS DE TESTE PADRAO CARREGADOS!", parent=self.master, 
                            icon="info", title="INFO SYS")

    def gerar_itens_aleatorios(self):
        try:
            quantidade_str = self.entry_qtd_aleatorios.get().strip()
            if not quantidade_str:
                messagebox.showerror("ERRO DE ENTRADA", "QUANTIDADE DE ITENS ALEATORIOS E OBRIGATORIA.", parent=self.master, icon="error", title="SYSTEM ERROR")
                return
            quantidade = int(quantidade_str)
            if quantidade <= 0:
                messagebox.showerror("ERRO DE ENTRADA", "QUANTIDADE DEVE SER UM NUMERO POSITIVO.", parent=self.master, icon="error", title="SYSTEM ERROR")
                return
        except ValueError:
            messagebox.showerror("ERRO DE ENTRADA", "QUANTIDADE INVALIDA. INSIRA UM NUMERO INTEIRO.", parent=self.master, icon="error", title="SYSTEM ERROR")
            return

        self.limpar_lista_itens(confirmar=False)
        novos_itens = []
        for i in range(quantidade):
            nome = f"RAND_OBJ_{i+1}"
            peso = random.randint(1, 10)
            valor = random.randint(10, 100)
            cor = random.choice(CORES_ITENS_MOCHILA)
            novos_itens.append({"nome": nome, "peso": peso, "valor": valor, "cor": cor})
        self.itens_para_algoritmo = novos_itens
        self.atualizar_display_itens()
        messagebox.showinfo("ITENS GERADOS", f"{quantidade} ITENS ALEATORIOS CARREGADOS!", parent=self.master,
                            icon="info", title="INFO SYS")

    def desenhar_mochila_vazia(self):
        self.canvas_itens_mochila.delete("all")
        self.canvas_itens_mochila.update_idletasks()
        w = self.canvas_itens_mochila.winfo_width()
        h = self.canvas_itens_mochila.winfo_height()
        if w <= 1 or h <= 1: 
            self.master.after(100, self.desenhar_mochila_vazia)
            return
        self.canvas_itens_mochila.create_rectangle(10, 10, w-10, h-10, outline=COR_CONTORNO_FRAMES, width=2, dash=(4, 4), tags="mochila_outline")
        self.canvas_itens_mochila.create_text(w/2, h/2, text="MOCHILA VAZIA", font=FONTE_PRINCIPAL_80S, fill=COR_TEXTO_PRINCIPAL, tags="mochila_texto_vazia")

    def carregar_itens_exemplo(self):
        self.itens_para_algoritmo = [] 
        self.atualizar_display_itens()

    def adicionar_item_lista(self):
        nome = self.entry_nome_item.get().strip().upper()
        peso_str = self.entry_peso_item.get().strip()
        valor_str = self.entry_valor_item.get().strip()
        if not nome or not peso_str or not valor_str:
            messagebox.showerror("ERRO DE ENTRADA", "NOME, PESO E VALOR SAO OBRIGATORIOS.", parent=self.master, icon="error", title="SYSTEM ERROR")
            return
        try:
            peso = int(peso_str); valor = int(valor_str)
            if peso <= 0 or valor <= 0: raise ValueError("PESO E VALOR DEVEM SER POSITIVOS.")
        except ValueError as e:
            messagebox.showerror("ERRO DE ENTRADA", f"DADOS INVALIDOS: {e}", parent=self.master, icon="error", title="SYSTEM ERROR")
            return
        cor_item = random.choice(CORES_ITENS_MOCHILA)
        self.itens_para_algoritmo.append({"nome": nome, "peso": peso, "valor": valor, "cor": cor_item})
        self.atualizar_display_itens()
        self.entry_nome_item.delete(0, tk.END); self.entry_nome_item.insert(0, f"RAD_ITEM_{len(self.itens_para_algoritmo)+1}")
        self.entry_peso_item.delete(0, tk.END); self.entry_valor_item.delete(0, tk.END)
        self.entry_nome_item.focus()

    def limpar_lista_itens(self, confirmar=True):
        if confirmar and not messagebox.askyesno("CONFIRMAR LIMPEZA", "TEM CERTEZA QUE DESEJA REMOVER TODOS OS ITENS DA LISTA?", parent=self.master, icon="question", title="CONFIRM ACTION"):
            return
        self.itens_para_algoritmo = []
        self.atualizar_display_itens()
        self.desenhar_mochila_vazia()

    def atualizar_display_itens(self):
        self.texto_itens_adicionados.configure(state="normal")
        self.texto_itens_adicionados.delete(1.0, tk.END)
        if not self.itens_para_algoritmo: self.texto_itens_adicionados.insert(tk.END, "NENHUM ITEM ADICIONADO.")
        else:
            for i, item in enumerate(self.itens_para_algoritmo):
                self.texto_itens_adicionados.insert(tk.END, f"{i+1}. {item['nome']} (P:{item['peso']}, V:{item['valor']})\n")
        self.texto_itens_adicionados.configure(state="disabled")

    def executar_algoritmo_genetico(self):
        try:
            capacidade = int(self.param_entries["capacidade_mochila"].get())
            tam_pop = int(self.param_entries["tam_populacao"].get())
            num_ger = int(self.param_entries["n_geracoes"].get())
            taxa_mut = float(self.param_entries["taxa_mutacao_0-1"].get())
            tam_torneio = int(self.param_entries["tam_torneio"].get())
            if not (capacidade > 0 and tam_pop > 0 and num_ger > 0 and 0 <= taxa_mut <= 1 and tam_torneio > 0):
                raise ValueError("VALORES DOS PARAMETROS SAO INVALIDOS.")
        except Exception as e:
            messagebox.showerror("ERRO DE PARAMETRO", f"PARAMETROS INVALIDOS: {e}. VERIFIQUE OS VALORES.", parent=self.master, icon="error", title="SYSTEM ERROR")
            return
        if not self.itens_para_algoritmo: messagebox.showwarning("NENHUM ITEM", "ADICIONE ITENS ANTES DE EXECUTAR.", parent=self.master, icon="warning", title="SYSTEM WARNING"); return

        self.btn_executar_ag.config(state="disabled")
        self.master.update_idletasks()
        self.texto_resultado.configure(state="normal"); self.texto_resultado.delete(1.0, tk.END)
        self.texto_resultado.insert(tk.END, f">>> OTIMIZANDO MOCHILA 80S...\n>>> ITENS: {len(self.itens_para_algoritmo)}, CAP: {capacidade}, POP: {tam_pop}, GER: {num_ger}, MUT: {taxa_mut}, TORN: {tam_torneio}\n\n")
        self.texto_resultado.configure(state="disabled"); self.master.update_idletasks()
        self.desenhar_mochila_vazia()
        self.label_geracao_atual.config(text="GERACAO: 0")

        try:
            itens_para_ag = [{k: v for k, v in item.items() if k != "cor"} for item in self.itens_para_algoritmo]
            melhor_solucao, melhor_valor, peso_final, _ = mochila_genetico.algoritmo_genetico_mochila(
                itens_para_ag, capacidade, tam_pop, num_ger, taxa_mut, tam_torneio, callback_geracao=self.feedback_geracao)
            
            self.texto_resultado.configure(state="normal")
            self.texto_resultado.insert(tk.END, "--- MELHOR COMBINACAO ENCONTRADA ---\n")
            itens_selecionados_nomes = []
            itens_selecionados_para_desenho = []
            if melhor_solucao:
                for i, sel in enumerate(melhor_solucao):
                    if sel: itens_selecionados_nomes.append(self.itens_para_algoritmo[i]["nome"]); itens_selecionados_para_desenho.append(self.itens_para_algoritmo[i])
            itens_formatados = ", ".join(itens_selecionados_nomes) if itens_selecionados_nomes else "NENHUM ITEM SELECIONADO!"
            self.texto_resultado.insert(tk.END, f"ITENS NA MOCHILA: {itens_formatados}\n")
            self.texto_resultado.insert(tk.END, f"VALOR TOTAL: {melhor_valor}\nPESO TOTAL: {peso_final} (CAP: {capacidade})\n")
            self.texto_resultado.configure(state="disabled")
            self.animar_itens_na_mochila_sequencial(itens_selecionados_para_desenho, capacidade)
        except Exception as e:
            messagebox.showerror("ERRO NA EXECUCAO", f"OCORREU UM ERRO: {e}", parent=self.master, icon="error", title="CRITICAL SYSTEM FAILURE")
            self.texto_resultado.configure(state="normal"); self.texto_resultado.insert(tk.END, f"\nERRO FATAL: {e}"); self.texto_resultado.configure(state="disabled")
        finally: self.btn_executar_ag.config(state="normal")

    def animar_itens_na_mochila_sequencial(self, itens_selecionados, capacidade_total_mochila, item_index=0, current_x=15, current_y=15, max_h_linha=0):
        self.canvas_itens_mochila.update_idletasks()
        w_canvas = self.canvas_itens_mochila.winfo_width()
        h_canvas = self.canvas_itens_mochila.winfo_height()
        padding = 5
        item_altura_canvas = 35 
        velocidade_animacao_ms = 25

        if item_index == 0:
            self.canvas_itens_mochila.delete("all")
            self.canvas_itens_mochila.create_rectangle(10, 10, w_canvas-10, h_canvas-10, outline=COR_CONTORNO_FRAMES, width=2, dash=(4,4), tags="mochila_outline")
            if not itens_selecionados:
                self.canvas_itens_mochila.create_text(w_canvas/2, h_canvas/2, text="MOCHILA VAZIA", font=FONTE_PRINCIPAL_80S, fill=COR_TEXTO_PRINCIPAL)
                return

        if item_index < len(itens_selecionados):
            item_atual = itens_selecionados[item_index]
            item_largura_canvas = max(30, min( (item_atual["peso"] / capacidade_total_mochila) * (w_canvas - 40) * 0.8, w_canvas * 0.3 ))
            item_largura_canvas = min(item_largura_canvas, w_canvas - 40) 

            final_x, final_y = current_x, current_y
            if current_x + item_largura_canvas + padding > w_canvas - 15:
                final_x = 15
                final_y = current_y + max_h_linha + padding
                max_h_linha = 0
            
            if final_y + item_altura_canvas > h_canvas - 15:
                print(f"Item {item_atual['nome']} nao cabe visualmente, pulando animacao restante.")
                self.master.after(velocidade_animacao_ms, lambda: self.animar_itens_na_mochila_sequencial(itens_selecionados, capacidade_total_mochila, len(itens_selecionados), final_x, final_y, max_h_linha))
                return

            start_x = final_x + item_largura_canvas / 2 
            start_y = -item_altura_canvas - 20 
            item_rect_id = self.canvas_itens_mochila.create_rectangle(start_x - item_largura_canvas/2, start_y, start_x + item_largura_canvas/2, start_y + item_altura_canvas, 
                                                                    fill=item_atual.get("cor", "#888888"), outline=COR_TEXTO_DESTAQUE, width=2, tags=f"item_anim_{item_index}")
            item_text_id = self.canvas_itens_mochila.create_text(start_x, start_y + item_altura_canvas/2, 
                                                                 text=item_atual["nome"][:10].upper(), font=("Courier New", 8, "bold"), 
                                                                 fill=COR_FUNDO_PRINCIPAL, state=tk.HIDDEN, tags=f"item_anim_text_{item_index}")
            
            next_current_x = final_x + item_largura_canvas + padding
            next_max_h_linha = max(max_h_linha, item_altura_canvas)
            next_current_y = final_y

            if next_current_x + padding > w_canvas - 15: 
                next_current_y = final_y + next_max_h_linha + padding 
                next_current_x = 15 
                next_max_h_linha = 0 

            self._animate_single_item_drop(item_rect_id, item_text_id, final_x, final_y, item_largura_canvas, item_altura_canvas, velocidade_animacao_ms, 
                lambda: self.animar_itens_na_mochila_sequencial(itens_selecionados, capacidade_total_mochila, item_index + 1, 
                                                                next_current_x, 
                                                                next_current_y,
                                                                next_max_h_linha
                                                                )
            )
        else:
            pass 

    def _animate_single_item_drop(self, rect_id, text_id, target_x_rect_start, target_y_rect_start, item_w, item_h, speed_ms, callback_on_finish):
        current_coords_rect = self.canvas_itens_mochila.coords(rect_id)
        current_y_rect = current_coords_rect[1]
        move_step = 8 

        if current_y_rect < target_y_rect_start:
            next_y_rect = min(current_y_rect + move_step, target_y_rect_start)
            delta_y = next_y_rect - current_y_rect
            self.canvas_itens_mochila.move(rect_id, 0, delta_y)
            self.canvas_itens_mochila.move(text_id, 0, delta_y)
            self.id_animacao_atual = self.master.after(speed_ms, lambda: self._animate_single_item_drop(rect_id, text_id, target_x_rect_start, target_y_rect_start, item_w, item_h, speed_ms, callback_on_finish))
        else:
            self.canvas_itens_mochila.coords(rect_id, target_x_rect_start, target_y_rect_start, target_x_rect_start + item_w, target_y_rect_start + item_h)
            self.canvas_itens_mochila.coords(text_id, target_x_rect_start + item_w/2, target_y_rect_start + item_h/2)
            self.canvas_itens_mochila.itemconfig(text_id, state=tk.NORMAL)
            if callback_on_finish:
                callback_on_finish()

def main():
    root = tk.Tk()
    app = AplicacaoMochila(root)
    root.mainloop()

if __name__ == "__main__":
    main()

print("Interface gráfica atualizada para o estilo Anos 80. Layout de títulos ajustado.")

