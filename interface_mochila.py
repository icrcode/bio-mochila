# -*- coding: utf-8 -*-
# interface_mochila.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
# importando o módulo do algoritmo genético
# certifique-se de que mochila_genetico.py está na mesma pasta ou no pythonpath
import mochila_genetico

# --- configuração da interface estilo anos 90 ---

# cores nostálgicas
COR_FUNDO_JANELA = "#c0c0c0"  # cinza claro clássico
COR_FUNDO_FRAME = "#d3d3d3" # um cinza um pouco mais claro para frames internos
COR_TEXTO = "#000000"      # preto
COR_BOTAO = "#c0c0c0"
COR_BOTAO_ATIVO = "#a0a0a0"
COR_ENTRADA_FUNDO = "#ffffff" # branco
COR_TEXTO_RESULTADO = "#000080" # azul marinho para resultados

# fontes (tentar algo que lembre a época)
# "System" ou "Fixedsys" são boas, mas podem não estar em todos os sistemas
# "Courier" é uma alternativa monoespaçada mais comum
FONTE_PADRAO = ("Courier", 10)
FONTE_TITULO = ("Courier", 12, "bold")
FONTE_BOTAO = ("Courier", 10, "bold")

class AplicacaoMochila:
    def __init__(self, master):
        self.master = master
        master.title("Problema da Mochila - AG (Estilo 90s)")
        master.configure(bg=COR_FUNDO_JANELA)
        master.geometry("750x650") # tamanho inicial da janela

        # para garantir que a janela não fique muito pequena
        master.minsize(700, 600)

        # lista para armazenar os itens adicionados pelo usuário
        self.itens_para_algoritmo = []

        # --- estilo dos widgets ttk (para um visual mais consistente) ---
        style = ttk.Style()
        style.theme_use('clam') # 'clam', 'alt', 'default', 'classic' podem dar visuais diferentes
                                # 'clam' costuma ser mais fácil de estilizar para um look retro

        style.configure("TFrame", background=COR_FUNDO_FRAME)
        style.configure("TLabel", background=COR_FUNDO_FRAME, foreground=COR_TEXTO, font=FONTE_PADRAO)
        style.configure("TButton", background=COR_BOTAO, foreground=COR_TEXTO, font=FONTE_BOTAO, relief="raised")
        style.map("TButton", background=[('active', COR_BOTAO_ATIVO)])
        style.configure("TEntry", fieldbackground=COR_ENTRADA_FUNDO, foreground=COR_TEXTO, font=FONTE_PADRAO)
        style.configure("Resultado.TLabel", background=COR_FUNDO_FRAME, foreground=COR_TEXTO_RESULTADO, font=FONTE_TITULO)

        # --- layout principal com frames ---
        # frame para entrada de itens
        frame_itens = ttk.Frame(master, padding="10 10 10 10", relief="groove", borderwidth=2)
        frame_itens.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame_itens, text="Adicionar Item:", font=FONTE_TITULO).grid(row=0, column=0, columnspan=3, pady=5, sticky="w")

        ttk.Label(frame_itens, text="Nome do Item:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome_item = ttk.Entry(frame_itens, width=15)
        self.entry_nome_item.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.entry_nome_item.insert(0, "ItemX") # valor padrão

        ttk.Label(frame_itens, text="Peso do Item:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_peso_item = ttk.Entry(frame_itens, width=10)
        self.entry_peso_item.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_itens, text="Valor do Item:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_valor_item = ttk.Entry(frame_itens, width=10)
        self.entry_valor_item.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.btn_adicionar_item = ttk.Button(frame_itens, text="Adicionar Item", command=self.adicionar_item_lista)
        self.btn_adicionar_item.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.btn_limpar_itens = ttk.Button(frame_itens, text="Limpar Itens", command=self.limpar_lista_itens)
        self.btn_limpar_itens.grid(row=4, column=1, columnspan=2, pady=10, padx=(0,5), sticky="e")

        # frame para exibir itens adicionados
        frame_lista_itens = ttk.Frame(master, padding="10 10 10 10", relief="groove", borderwidth=2)
        frame_lista_itens.pack(pady=10, padx=10, fill="both", expand=True)
        ttk.Label(frame_lista_itens, text="Itens Disponíveis:", font=FONTE_TITULO).pack(pady=5, anchor="w")
        self.texto_itens_adicionados = scrolledtext.ScrolledText(frame_lista_itens, width=60, height=8, font=FONTE_PADRAO, bg=COR_ENTRADA_FUNDO, fg=COR_TEXTO, relief="sunken", borderwidth=2)
        self.texto_itens_adicionados.pack(pady=5, fill="both", expand=True)
        self.texto_itens_adicionados.configure(state='disabled') # apenas para leitura

        # frame para parâmetros da mochila e do ag
        frame_parametros = ttk.Frame(master, padding="10 10 10 10", relief="groove", borderwidth=2)
        frame_parametros.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame_parametros, text="Configurações:", font=FONTE_TITULO).grid(row=0, column=0, columnspan=4, pady=5, sticky="w")

        ttk.Label(frame_parametros, text="Capacidade Mochila:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_capacidade_mochila = ttk.Entry(frame_parametros, width=10)
        self.entry_capacidade_mochila.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_capacidade_mochila.insert(0, "10") # valor padrão

        ttk.Label(frame_parametros, text="Tam. População:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_tam_pop = ttk.Entry(frame_parametros, width=10)
        self.entry_tam_pop.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.entry_tam_pop.insert(0, "50") # valor padrão

        ttk.Label(frame_parametros, text="Nº Gerações:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_num_ger = ttk.Entry(frame_parametros, width=10)
        self.entry_num_ger.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.entry_num_ger.insert(0, "100") # valor padrão

        ttk.Label(frame_parametros, text="Taxa Mutação (0-1):").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_taxa_mut = ttk.Entry(frame_parametros, width=10)
        self.entry_taxa_mut.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.entry_taxa_mut.insert(0, "0.02") # valor padrão
        
        ttk.Label(frame_parametros, text="Tam. Torneio:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_tam_torneio = ttk.Entry(frame_parametros, width=10)
        self.entry_tam_torneio.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.entry_tam_torneio.insert(0, "5") # valor padrão

        # frame para botão de execução e resultados
        frame_execucao = ttk.Frame(master, padding="10 10 10 10", relief="groove", borderwidth=2)
        frame_execucao.pack(pady=10, padx=10, fill="x")

        self.btn_executar_ag = ttk.Button(frame_execucao, text="Resolver Mochila com AG!", command=self.executar_algoritmo_genetico, style="TButton")
        self.btn_executar_ag.pack(pady=10)

        ttk.Label(frame_execucao, text="Resultado:", font=FONTE_TITULO, style="Resultado.TLabel").pack(pady=5, anchor="w")
        self.texto_resultado = scrolledtext.ScrolledText(frame_execucao, width=70, height=7, font=FONTE_PADRAO, bg=COR_ENTRADA_FUNDO, fg=COR_TEXTO_RESULTADO, relief="sunken", borderwidth=2)
        self.texto_resultado.pack(pady=5, fill="x", expand=True)
        self.texto_resultado.configure(state='disabled')
        
        # Adicionar alguns itens de exemplo para facilitar o teste
        self.itens_para_algoritmo = [
            {"nome": "diamante", "peso": 3, "valor": 55},
            {"nome": "ouro", "peso": 4, "valor": 60},
            {"nome": "prata", "peso": 2, "valor": 30},
            {"nome": "rubi", "peso": 1, "valor": 20},
            {"nome": "esmeralda", "peso": 2, "valor": 45}
        ]
        self.atualizar_display_itens()

    def adicionar_item_lista(self):
        # obter nome, peso e valor dos campos de entrada
        nome = self.entry_nome_item.get().strip()
        peso_str = self.entry_peso_item.get().strip()
        valor_str = self.entry_valor_item.get().strip()

        if not nome:
            messagebox.showerror("Erro de Entrada", "O nome do item não pode estar vazio.", parent=self.master)
            return

        try:
            peso = int(peso_str)
            valor = int(valor_str)
            if peso <= 0 or valor <= 0:
                raise ValueError("Peso e valor devem ser positivos.")
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Peso e Valor devem ser números inteiros positivos. Erro: {e}", parent=self.master)
            return

        # adicionar o item à lista interna
        self.itens_para_algoritmo.append({"nome": nome, "peso": peso, "valor": valor})
        # atualizar a exibição dos itens
        self.atualizar_display_itens()
        # limpar campos de entrada após adicionar
        self.entry_nome_item.delete(0, tk.END)
        self.entry_nome_item.insert(0, f"Item{len(self.itens_para_algoritmo)+1}") # sugere próximo nome
        self.entry_peso_item.delete(0, tk.END)
        self.entry_valor_item.delete(0, tk.END)
        self.entry_nome_item.focus()
        print(f"item adicionado: {nome}, peso: {peso}, valor: {valor}")

    def limpar_lista_itens(self):
        if messagebox.askyesno("Confirmar Limpeza", "Tem certeza que deseja remover todos os itens da lista?", parent=self.master):
            self.itens_para_algoritmo = []
            self.atualizar_display_itens()
            print("lista de itens limpa.")

    def atualizar_display_itens(self):
        self.texto_itens_adicionados.configure(state='normal') # habilitar para edição
        self.texto_itens_adicionados.delete(1.0, tk.END) # limpar conteúdo atual
        if not self.itens_para_algoritmo:
            self.texto_itens_adicionados.insert(tk.END, "Nenhum item adicionado ainda.\nUse os campos acima para adicionar itens.")
        else:
            for i, item in enumerate(self.itens_para_algoritmo):
                self.texto_itens_adicionados.insert(tk.END, f"{i+1}. {item['nome']} (Peso: {item['peso']}, Valor: {item['valor']})\n")
        self.texto_itens_adicionados.configure(state='disabled') # desabilitar novamente

    def executar_algoritmo_genetico(self):
        # obter parâmetros da interface
        try:
            capacidade = int(self.entry_capacidade_mochila.get())
            tam_pop = int(self.entry_tam_pop.get())
            num_ger = int(self.entry_num_ger.get())
            taxa_mut = float(self.entry_taxa_mut.get())
            tam_torneio = int(self.entry_tam_torneio.get())

            if capacidade <= 0 or tam_pop <= 0 or num_ger <= 0 or not (0 <= taxa_mut <= 1) or tam_torneio <= 0:
                raise ValueError("Parâmetros inválidos. Verifique os valores.")
        except ValueError as e:
            messagebox.showerror("Erro de Parâmetro", f"Parâmetros inválidos: {e}.\nCapacidade, População, Gerações, Torneio devem ser inteiros positivos.\nTaxa de Mutação deve ser um float entre 0 e 1.", parent=self.master)
            return

        if not self.itens_para_algoritmo:
            messagebox.showwarning("Nenhum Item", "Adicione pelo menos um item antes de executar o algoritmo.", parent=self.master)
            return

        # desabilitar botão para evitar cliques múltiplos durante a execução
        self.btn_executar_ag.config(state="disabled")
        self.master.update_idletasks() # forçar atualização da interface
        
        self.texto_resultado.configure(state='normal')
        self.texto_resultado.delete(1.0, tk.END)
        self.texto_resultado.insert(tk.END, "Executando Algoritmo Genético... Por favor, aguarde.\n")
        self.texto_resultado.insert(tk.END, f"Itens: {len(self.itens_para_algoritmo)}, Capacidade: {capacidade}\n")
        self.texto_resultado.insert(tk.END, f"Pop: {tam_pop}, Ger: {num_ger}, Mut: {taxa_mut}, Torneio: {tam_torneio}\n\n")
        self.texto_resultado.configure(state='disabled')
        self.master.update_idletasks()

        try:
            # chamar o algoritmo genético do outro arquivo
            melhor_solucao, melhor_valor, peso_final, _ = mochila_genetico.algoritmo_genetico_mochila(
                self.itens_para_algoritmo,
                capacidade,
                tam_pop,
                num_ger,
                taxa_mut,
                tam_torneio
            )

            # exibir os resultados
            self.texto_resultado.configure(state='normal') # habilitar para edição
            # self.texto_resultado.delete(1.0, tk.END) # limpar conteúdo anterior
            self.texto_resultado.insert(tk.END, "--- MELHOR SOLUÇÃO ENCONTRADA ---\n")
            
            itens_selecionados_str = []
            if melhor_solucao:
                for i, selecionado in enumerate(melhor_solucao):
                    if selecionado:
                        itens_selecionados_str.append(self.itens_para_algoritmo[i]['nome'])
            
            if itens_selecionados_str:
                self.texto_resultado.insert(tk.END, f"Itens na Mochila: {', '.join(itens_selecionados_str)}\n")
            else:
                self.texto_resultado.insert(tk.END, "Nenhum item selecionado (mochila vazia ou itens não couberam).\n")

            self.texto_resultado.insert(tk.END, f"Valor Total: {melhor_valor}\n")
            self.texto_resultado.insert(tk.END, f"Peso Total: {peso_final} (Capacidade Máxima: {capacidade})\n")
            self.texto_resultado.configure(state='disabled') # desabilitar novamente

        except Exception as e:
            messagebox.showerror("Erro na Execução", f"Ocorreu um erro durante a execução do algoritmo: {e}", parent=self.master)
            self.texto_resultado.configure(state='normal')
            self.texto_resultado.insert(tk.END, f"\nERRO: {e}")
            self.texto_resultado.configure(state='disabled')
        finally:
            # reabilitar o botão após a execução (ou erro)
            self.btn_executar_ag.config(state="normal")

# --- função principal para iniciar a aplicação ---
def main():
    root = tk.Tk()
    # Tentar definir um ícone (opcional, pode não funcionar em todos os SOs ou requerer um arquivo .ico)
    # try:
    #     # root.iconbitmap('caminho/para/seu/icone.ico') # no windows
    #     # img = tk.PhotoImage(file='caminho/para/seu/icone.png') # para png, pode precisar de Pillow
    #     # root.tk.call('wm', 'iconphoto', root._w, img)
    #     pass # deixar sem por enquanto para simplicidade
    # except tk.TclError:
    #     print("não foi possível definir o ícone da janela.")
        
    app = AplicacaoMochila(root)
    root.mainloop()

if __name__ == "__main__":
    main()

print("interface gráfica básica criada em interface_mochila.py")

