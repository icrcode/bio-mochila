# -*- coding: utf-8 -*-
# interface_mochila.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import mochila_genetico # importando o módulo do algoritmo genético
import random # para cores e, potencialmente, animação

# --- configuração da interface estilo windows xp / emily is away ---

COR_XP_AZUL_BARRA_TITULO = "#245DDA"
COR_XP_AZUL_FUNDO_JANELA = "#D6E8FF"
COR_XP_CINZA_FUNDO_ELEMENTOS = "#ECE9D8"
COR_XP_TEXTO_PRETO = "#000000"
COR_XP_TEXTO_BOTAO = "#000000"
COR_XP_AZUL_DESTAQUE_BOTAO = "#485FEA"
COR_XP_BRANCO_ENTRADA = "#FFFFFF"
COR_XP_VERDE_RESULTADO_TEXTO = "#3A772A"
COR_XP_AZUL_TITULO_FRAME = "#0A246A"

FONTE_PRINCIPAL_XP = ("Tahoma", 8)
FONTE_TITULO_XP = ("Trebuchet MS", 9, "bold") # Ajustado para caber melhor
FONTE_BOTAO_XP = ("Tahoma", 8, "bold")
FONTE_TEXTO_AREA_XP = ("Lucida Console", 9)

class AplicacaoMochila:
    def __init__(self, master):
        self.master = master
        master.title("Mochila Mágica XP - Algoritmo Genético")
        master.configure(bg=COR_XP_CINZA_FUNDO_ELEMENTOS)
        master.geometry("850x780") # Aumentado para melhor layout
        master.minsize(820, 720)

        self.itens_para_algoritmo = []
        self.canvas_itens_mochila = None
        self.id_animacao_atual = None

        style = ttk.Style()
        try:
            style.theme_use("default")
        except tk.TclError:
            style.theme_use("clam")

        style.configure("TFrame", background=COR_XP_CINZA_FUNDO_ELEMENTOS)
        style.configure("TLabel", background=COR_XP_CINZA_FUNDO_ELEMENTOS, foreground=COR_XP_TEXTO_PRETO, font=FONTE_PRINCIPAL_XP)
        style.configure("TButton", font=FONTE_BOTAO_XP, foreground=COR_XP_TEXTO_BOTAO, background=COR_XP_CINZA_FUNDO_ELEMENTOS, borderwidth=1, relief="raised")
        style.map("TButton",
            background=[("active", COR_XP_AZUL_DESTAQUE_BOTAO), ("pressed", COR_XP_AZUL_DESTAQUE_BOTAO), ("hover", COR_XP_AZUL_FUNDO_JANELA)],
            foreground=[("active", COR_XP_BRANCO_ENTRADA), ("pressed", COR_XP_BRANCO_ENTRADA)]
        )
        style.configure("TEntry", fieldbackground=COR_XP_BRANCO_ENTRADA, foreground=COR_XP_TEXTO_PRETO, font=FONTE_PRINCIPAL_XP, borderwidth=1, relief="sunken")
        style.configure("Titulo.TLabel", background=COR_XP_CINZA_FUNDO_ELEMENTOS, foreground=COR_XP_AZUL_TITULO_FRAME, font=FONTE_TITULO_XP)
        style.configure("Resultado.TLabel", background=COR_XP_CINZA_FUNDO_ELEMENTOS, foreground=COR_XP_VERDE_RESULTADO_TEXTO, font=FONTE_TITULO_XP)

        main_outer_frame = tk.Frame(master, bg=COR_XP_AZUL_BARRA_TITULO, bd=3, relief="raised")
        main_outer_frame.pack(fill="both", expand=True, padx=5, pady=5)
        main_inner_frame = tk.Frame(main_outer_frame, bg=COR_XP_CINZA_FUNDO_ELEMENTOS, bd=2, relief="sunken")
        main_inner_frame.pack(fill="both", expand=True, padx=2, pady=2)

        top_frame = ttk.Frame(main_inner_frame, padding="10 10 10 10")
        top_frame.pack(pady=10, padx=10, fill="x")

        # Coluna da esquerda: Adicionar Item, Geradores de Itens, Parâmetros
        left_column_frame = ttk.Frame(top_frame, width=300) # Definir uma largura para a coluna da esquerda
        left_column_frame.pack(side="left", fill="y", padx=(0,10), anchor="n")
        left_column_frame.pack_propagate(False) # Impedir que a coluna encolha

        frame_itens = ttk.LabelFrame(left_column_frame, text=" Adicionar Item ", style="Titulo.TLabel", relief="groove", borderwidth=2, padding="10 10 10 10")
        frame_itens.pack(pady=5, padx=5, fill="x")
        frame_itens.columnconfigure(1, weight=1) # Permitir que a coluna de entrada expanda

        ttk.Label(frame_itens, text="Nome:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.entry_nome_item = ttk.Entry(frame_itens, width=25, font=FONTE_PRINCIPAL_XP)
        self.entry_nome_item.grid(row=0, column=1, padx=5, pady=3, sticky="ew")
        self.entry_nome_item.insert(0, "ItemXP")
        ttk.Label(frame_itens, text="Peso:").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        self.entry_peso_item = ttk.Entry(frame_itens, width=12, font=FONTE_PRINCIPAL_XP)
        self.entry_peso_item.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        ttk.Label(frame_itens, text="Valor:").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.entry_valor_item = ttk.Entry(frame_itens, width=12, font=FONTE_PRINCIPAL_XP)
        self.entry_valor_item.grid(row=2, column=1, padx=5, pady=3, sticky="w")
        self.btn_adicionar_item = ttk.Button(frame_itens, text="Adicionar Item", command=self.adicionar_item_lista)
        self.btn_adicionar_item.grid(row=3, column=0, columnspan=2, pady=8)

        # Frame para botões geradores de itens
        frame_geradores = ttk.LabelFrame(left_column_frame, text=" Gerar Itens ", style="Titulo.TLabel", relief="groove", borderwidth=2, padding="10 10 10 10")
        frame_geradores.pack(pady=10, padx=5, fill="x")
        self.btn_gerar_padrao = ttk.Button(frame_geradores, text="Gerar Teste Padrão (10 Itens)", command=self.gerar_itens_padrao)
        self.btn_gerar_padrao.pack(pady=3, fill="x")
        self.btn_gerar_aleatorios = ttk.Button(frame_geradores, text="Gerar 5 Itens Aleatórios", command=self.gerar_itens_aleatorios)
        self.btn_gerar_aleatorios.pack(pady=3, fill="x")

        frame_parametros = ttk.LabelFrame(left_column_frame, text=" Configurações do Algoritmo ", style="Titulo.TLabel", relief="groove", borderwidth=2, padding="10 10 10 10")
        frame_parametros.pack(pady=10, padx=5, fill="x")
        frame_parametros.columnconfigure(1, weight=1)
        param_labels_keys = [
            ("Capacidade Mochila:", "capacidade_mochila"),
            ("Tam. População:", "tam_populacao"),
            ("Nº Gerações:", "n_geracoes"),
            ("Taxa Mutação (0-1):", "taxa_mutacao_0-1"),
            ("Tam. Torneio:", "tam_torneio")
        ]
        param_defaults = ["10", "50", "100", "0.02", "5"]
        self.param_entries = {}
        for i, (label_text, key) in enumerate(param_labels_keys):
            lbl = ttk.Label(frame_parametros, text=label_text)
            lbl.grid(row=i, column=0, padx=5, pady=3, sticky="w")
            entry = ttk.Entry(frame_parametros, width=12, font=FONTE_PRINCIPAL_XP)
            entry.grid(row=i, column=1, padx=5, pady=3, sticky="ew")
            entry.insert(0, param_defaults[i])
            self.param_entries[key] = entry

        right_column_frame = ttk.Frame(top_frame)
        right_column_frame.pack(side="left", fill="both", expand=True)

        frame_lista_itens = ttk.LabelFrame(right_column_frame, text=" Itens Disponíveis ", style="Titulo.TLabel", relief="groove", borderwidth=2, padding="10 10 10 10")
        frame_lista_itens.pack(pady=5, padx=5, fill="both", expand=True)
        self.texto_itens_adicionados = scrolledtext.ScrolledText(frame_lista_itens, width=45, height=10, font=FONTE_TEXTO_AREA_XP, bg=COR_XP_BRANCO_ENTRADA, fg=COR_XP_TEXTO_PRETO, relief="sunken", borderwidth=1)
        self.texto_itens_adicionados.pack(pady=5, fill="both", expand=True)
        self.texto_itens_adicionados.configure(state="disabled")
        self.btn_limpar_itens = ttk.Button(frame_lista_itens, text="Limpar Lista de Itens", command=self.limpar_lista_itens)
        self.btn_limpar_itens.pack(pady=5)

        frame_mochila_grafica = ttk.LabelFrame(right_column_frame, text=" Conteúdo da Mochila (Gráfico) ", style="Titulo.TLabel", relief="groove", borderwidth=2, padding="10 10 10 10")
        frame_mochila_grafica.pack(pady=10, padx=5, fill="both", expand=True)
        self.canvas_itens_mochila = tk.Canvas(frame_mochila_grafica, bg=COR_XP_AZUL_FUNDO_JANELA, relief="sunken", borderwidth=1)
        self.canvas_itens_mochila.pack(fill="both", expand=True)
        self.master.after(50, self.desenhar_mochila_vazia)

        bottom_frame = ttk.Frame(main_inner_frame, padding="10 10 10 10")
        bottom_frame.pack(pady=10, padx=10, fill="x")
        self.btn_executar_ag = ttk.Button(bottom_frame, text="> Iniciar Otimização da Mochila! <", command=self.executar_algoritmo_genetico)
        self.btn_executar_ag.pack(pady=10, ipady=5, ipadx=10)

        frame_resultado = ttk.LabelFrame(bottom_frame, text=" Resultado da Otimização ", style="Resultado.TLabel", relief="groove", borderwidth=2, padding="10 10 10 10")
        frame_resultado.pack(pady=5, fill="x", expand=True)
        self.texto_resultado = scrolledtext.ScrolledText(frame_resultado, width=70, height=5, font=FONTE_TEXTO_AREA_XP, bg=COR_XP_BRANCO_ENTRADA, fg=COR_XP_VERDE_RESULTADO_TEXTO, relief="sunken", borderwidth=1)
        self.texto_resultado.pack(pady=5, fill="x", expand=True)
        self.texto_resultado.configure(state="disabled")
        
        self.carregar_itens_exemplo() # Carrega 5 itens de exemplo iniciais

    def gerar_itens_padrao(self):
        self.limpar_lista_itens(confirmar=False)
        itens_padrao = [
            {"nome": "Tesouro1", "peso": 4, "valor": 50, "cor": "#FFD700"}, # Gold
            {"nome": "JoiaRara", "peso": 2, "valor": 65, "cor": "#E0115F"}, # Ruby
            {"nome": "Artefato", "peso": 3, "valor": 40, "cor": "#008080"}, # Teal
            {"nome": "Relíquia", "peso": 5, "valor": 70, "cor": "#C0C0C0"}, # Silver
            {"nome": "Pergaminho", "peso": 1, "valor": 25, "cor": "#F5DEB3"}, # Wheat
            {"nome": "CáliceXP", "peso": 2, "valor": 30, "cor": "#DAA520"}, # Goldenrod
            {"nome": "Adorno", "peso": 1, "valor": 15, "cor": "#FFC0CB"}, # Pink
            {"nome": "EstátuaP", "peso": 6, "valor": 60, "cor": "#800000"}, # Maroon
            {"nome": "MoedaAntiga", "peso": 1, "valor": 35, "cor": "#B8860B"}, # DarkGoldenrod
            {"nome": "Cristal", "peso": 3, "valor": 55, "cor": "#AFEEEE"}  # PaleTurquoise
        ]
        self.itens_para_algoritmo = itens_padrao
        self.atualizar_display_itens()
        messagebox.showinfo("Itens Gerados", "10 itens de teste padrão foram carregados!", parent=self.master)

    def gerar_itens_aleatorios(self, quantidade=5):
        self.limpar_lista_itens(confirmar=False)
        novos_itens = []
        cores_possiveis = ["#FFB347", "#A1CAF1", "#C1E1C1", "#FDFD96", "#FF6961", "#B28DD0", "#FFDAB9", "#E6E6FA"]
        for i in range(quantidade):
            nome = f"RandItem{i+1}"
            peso = random.randint(1, 10)
            valor = random.randint(10, 100)
            cor = random.choice(cores_possiveis)
            novos_itens.append({"nome": nome, "peso": peso, "valor": valor, "cor": cor})
        self.itens_para_algoritmo = novos_itens
        self.atualizar_display_itens()
        messagebox.showinfo("Itens Gerados", f"{quantidade} itens aleatórios foram carregados!", parent=self.master)

    def desenhar_mochila_vazia(self):
        self.canvas_itens_mochila.delete("all")
        self.canvas_itens_mochila.update_idletasks()
        w = self.canvas_itens_mochila.winfo_width()
        h = self.canvas_itens_mochila.winfo_height()
        if w <= 1 or h <= 1: 
            self.master.after(100, self.desenhar_mochila_vazia)
            return
        self.canvas_itens_mochila.create_rectangle(10, 10, w-10, h-10, outline=COR_XP_AZUL_TITULO_FRAME, width=2, dash=(4, 2), tags="mochila_outline")
        self.canvas_itens_mochila.create_text(w/2, h/2, text="Mochila Vazia", font=FONTE_PRINCIPAL_XP, fill=COR_XP_AZUL_TITULO_FRAME, tags="mochila_texto_vazia")

    def carregar_itens_exemplo(self):
        # Chamado no init, agora substituído por botões ou começa vazio
        # self.gerar_itens_padrao() # Ou começa com os 10 itens padrão
        self.itens_para_algoritmo = [] # Começa vazio por padrão
        self.atualizar_display_itens()

    def adicionar_item_lista(self):
        nome = self.entry_nome_item.get().strip()
        peso_str = self.entry_peso_item.get().strip()
        valor_str = self.entry_valor_item.get().strip()
        if not nome or not peso_str or not valor_str:
            messagebox.showerror("Erro de Entrada", "Nome, Peso e Valor são obrigatórios.", parent=self.master)
            return
        try:
            peso = int(peso_str); valor = int(valor_str)
            if peso <= 0 or valor <= 0: raise ValueError("Peso e valor devem ser positivos.")
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Peso e Valor devem ser números inteiros positivos. Erro: {e}", parent=self.master)
            return
        cores_possiveis = ["#FFB347", "#A1CAF1", "#C1E1C1", "#FDFD96", "#FF6961", "#B28DD0", "#FFDAB9", "#E6E6FA"]
        cor_item = random.choice(cores_possiveis)
        self.itens_para_algoritmo.append({"nome": nome, "peso": peso, "valor": valor, "cor": cor_item})
        self.atualizar_display_itens()
        self.entry_nome_item.delete(0, tk.END); self.entry_nome_item.insert(0, f"Item{len(self.itens_para_algoritmo)+1}")
        self.entry_peso_item.delete(0, tk.END); self.entry_valor_item.delete(0, tk.END)
        self.entry_nome_item.focus()

    def limpar_lista_itens(self, confirmar=True):
        if confirmar and not messagebox.askyesno("Confirmar Limpeza", "Tem certeza que deseja remover todos os itens da lista?", parent=self.master):
            return
        self.itens_para_algoritmo = []
        self.atualizar_display_itens()
        self.desenhar_mochila_vazia()

    def atualizar_display_itens(self):
        self.texto_itens_adicionados.configure(state="normal")
        self.texto_itens_adicionados.delete(1.0, tk.END)
        if not self.itens_para_algoritmo: self.texto_itens_adicionados.insert(tk.END, "Nenhum item adicionado.")
        else:
            for i, item in enumerate(self.itens_para_algoritmo):
                self.texto_itens_adicionados.insert(tk.END, f"{i+1}. {item["nome"]} (P: {item["peso"]}, V: {item["valor"]})\n")
        self.texto_itens_adicionados.configure(state="disabled")

    def executar_algoritmo_genetico(self):
        try:
            # Corrigido para usar as chaves corretas definidas em param_labels_keys
            capacidade = int(self.param_entries["capacidade_mochila"].get())
            tam_pop = int(self.param_entries["tam_populacao"].get())
            num_ger = int(self.param_entries["n_geracoes"].get())
            taxa_mut = float(self.param_entries["taxa_mutacao_0-1"].get())
            tam_torneio = int(self.param_entries["tam_torneio"].get())
            if not (capacidade > 0 and tam_pop > 0 and num_ger > 0 and 0 <= taxa_mut <= 1 and tam_torneio > 0):
                raise ValueError("Valores dos parâmetros são inválidos.")
        except Exception as e:
            messagebox.showerror("Erro de Parâmetro", f"Parâmetros inválidos: {e}. Verifique os valores.", parent=self.master)
            return
        if not self.itens_para_algoritmo: messagebox.showwarning("Nenhum Item", "Adicione itens antes.", parent=self.master); return

        self.btn_executar_ag.config(state="disabled")
        self.master.update_idletasks()
        self.texto_resultado.configure(state="normal"); self.texto_resultado.delete(1.0, tk.END)
        self.texto_resultado.insert(tk.END, f"Otimizando mochila XP...\nItens: {len(self.itens_para_algoritmo)}, Cap: {capacidade}, Pop: {tam_pop}, Ger: {num_ger}, Mut: {taxa_mut}, Torn: {tam_torneio}\n\n")
        self.texto_resultado.configure(state="disabled"); self.master.update_idletasks()
        self.desenhar_mochila_vazia()

        try:
            itens_para_ag = [{k: v for k, v in item.items() if k != "cor"} for item in self.itens_para_algoritmo]
            melhor_solucao, melhor_valor, peso_final, _ = mochila_genetico.algoritmo_genetico_mochila(
                itens_para_ag, capacidade, tam_pop, num_ger, taxa_mut, tam_torneio)
            self.texto_resultado.configure(state="normal")
            self.texto_resultado.insert(tk.END, "--- MELHOR COMBINAÇÃO ---\n")
            itens_selecionados_nomes = []
            itens_selecionados_para_desenho = []
            if melhor_solucao:
                for i, sel in enumerate(melhor_solucao):
                    if sel: itens_selecionados_nomes.append(self.itens_para_algoritmo[i]["nome"]); itens_selecionados_para_desenho.append(self.itens_para_algoritmo[i])
            self.texto_resultado.insert(tk.END, f"Itens na Mochila: {", ".join(itens_selecionados_nomes) if itens_selecionados_nomes else "Nenhum item selecionado!"}\n")
            self.texto_resultado.insert(tk.END, f"Valor Total: {melhor_valor}\nPeso Total: {peso_final} (Cap: {capacidade})\n")
            self.texto_resultado.configure(state="disabled")
            self.animar_itens_na_mochila_sequencial(itens_selecionados_para_desenho, capacidade)
        except Exception as e:
            messagebox.showerror("Erro na Execução", f"Ocorreu um erro: {e}", parent=self.master)
            self.texto_resultado.configure(state="normal"); self.texto_resultado.insert(tk.END, f"\nERRO: {e}"); self.texto_resultado.configure(state="disabled")
        finally: self.btn_executar_ag.config(state="normal")

    def animar_itens_na_mochila_sequencial(self, itens_selecionados, capacidade_total_mochila, item_index=0, current_x=15, current_y=15, max_h_linha=0):
        self.canvas_itens_mochila.update_idletasks()
        w_canvas = self.canvas_itens_mochila.winfo_width()
        h_canvas = self.canvas_itens_mochila.winfo_height()
        padding = 5
        item_altura_canvas = 30 
        velocidade_animacao_ms = 30

        if item_index == 0:
            self.canvas_itens_mochila.delete("all")
            self.canvas_itens_mochila.create_rectangle(10, 10, w_canvas-10, h_canvas-10, outline=COR_XP_AZUL_TITULO_FRAME, width=2, dash=(4,2), tags="mochila_outline")
            if not itens_selecionados:
                self.canvas_itens_mochila.create_text(w_canvas/2, h_canvas/2, text="Mochila Vazia", font=FONTE_PRINCIPAL_XP, fill=COR_XP_AZUL_TITULO_FRAME)
                return

        if item_index < len(itens_selecionados):
            item_atual = itens_selecionados[item_index]
            item_largura_canvas = max(20, (item_atual["peso"] / capacidade_total_mochila) * (w_canvas - 30) * 0.7)
            item_largura_canvas = min(item_largura_canvas, w_canvas - 40) # Ajuste para não cortar

            final_x, final_y = current_x, current_y
            if current_x + item_largura_canvas + padding > w_canvas - 15:
                final_x = 15
                final_y = current_y + max_h_linha + padding
                max_h_linha = 0
            
            if final_y + item_altura_canvas > h_canvas - 15:
                print(f"Item {item_atual["nome"]} não cabe visualmente, pulando animação restante.")
                self.master.after(velocidade_animacao_ms, lambda: self.animar_itens_na_mochila_sequencial(itens_selecionados, capacidade_total_mochila, len(itens_selecionados), final_x, final_y, max_h_linha))
                return

            start_x = final_x
            start_y = -item_altura_canvas - 10
            item_rect_id = self.canvas_itens_mochila.create_rectangle(start_x, start_y, start_x + item_largura_canvas, start_y + item_altura_canvas, fill=item_atual.get("cor", "#CCCCCC"), outline=COR_XP_TEXTO_PRETO, width=1)
            item_text_id = self.canvas_itens_mochila.create_text(start_x + item_largura_canvas/2, start_y + item_altura_canvas/2, text=item_atual["nome"][:10], font=("Tahoma", 7), fill=COR_XP_TEXTO_PRETO, state=tk.HIDDEN)
            
            next_current_x = final_x + item_largura_canvas + padding
            next_max_h_linha = max(max_h_linha, item_altura_canvas)
            next_current_y = final_y

            if next_current_x > w_canvas - 15: # Se o próximo item for para nova linha
                next_current_y = final_y + next_max_h_linha + padding # y da próxima linha
                next_current_x = 15 # x da próxima linha
                next_max_h_linha = 0 # reseta altura da linha

            self._animate_single_item_drop(item_rect_id, item_text_id, final_y, velocidade_animacao_ms, 
                lambda: self.animar_itens_na_mochila_sequencial(itens_selecionados, capacidade_total_mochila, item_index + 1, 
                                                                next_current_x, 
                                                                next_current_y,
                                                                next_max_h_linha
                                                                )
            )
        else:
            print("Animação da mochila concluída.")
            pass 

    def _animate_single_item_drop(self, rect_id, text_id, target_y, speed_ms, callback_on_finish):
        current_coords = self.canvas_itens_mochila.coords(rect_id)
        current_y = current_coords[1]
        move_step = 5 

        if current_y < target_y:
            next_y = min(current_y + move_step, target_y)
            self.canvas_itens_mochila.move(rect_id, 0, next_y - current_y)
            self.canvas_itens_mochila.move(text_id, 0, next_y - current_y)
            self.id_animacao_atual = self.master.after(speed_ms, lambda: self._animate_single_item_drop(rect_id, text_id, target_y, speed_ms, callback_on_finish))
        else:
            self.canvas_itens_mochila.itemconfig(text_id, state=tk.NORMAL)
            if callback_on_finish:
                callback_on_finish()

def main():
    root = tk.Tk()
    app = AplicacaoMochila(root)
    root.mainloop()

if __name__ == "__main__":
    main()

print("Interface gráfica atualizada com correções de layout, botões e parâmetros.")

