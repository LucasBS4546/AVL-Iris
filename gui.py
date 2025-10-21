import tkinter as tk
from tkinter import ttk
from avltree import AvlTree

class AvlTreeVisualizer(ttk.Frame):
    def __init__(self, master_tk, window_title, tree, df):
        super().__init__(master_tk)
        self.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self, bg="white", width=1200, height=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.tree = tree
        self.node_radius = 30
        self.level_height = 80
        self.horizontal_spacing = 40
        self.df_iris = df

        self.__draw_tree()

    def __draw_tree(self):
        root_key = self.tree._AvlTree__root_key
        if root_key is None:
            return
        nodes = self.tree._AvlTree__nodes
        positions = {}
        x_counter = [0]

        def assign_positions(key, depth):
            if key is None:
                return
            node = nodes[key]
            assign_positions(node.lesser_child_key, depth + 1)
            positions[key] = (x_counter[0], depth)
            x_counter[0] += 1
            assign_positions(node.greater_child_key, depth + 1)

        assign_positions(root_key, 0)
        total_width = x_counter[0]
        canvas_width = 1200
        scale_x = canvas_width / max(total_width, 1)

        def draw_node(key, parent_coords=None):
            if key is None:
                return
            x_index, depth = positions[key]
            x = x_index * scale_x + self.node_radius
            y = depth * self.level_height + self.node_radius + 20
            coords = (x, y)
            dados_iris = self.df_iris.iloc[nodes[key].value]
            sl = dados_iris["sepal length (cm)"]
            sw = dados_iris["sepal width (cm)"]
            pl = dados_iris["petal length (cm)"]
            pw = dados_iris["petal width (cm)"]
            sp = dados_iris["species"]
            str_node = f"{sp}\n{sl} | {sw}\n{pl} | {pw}"
            if parent_coords:
                self.canvas.create_line(parent_coords[0], parent_coords[1], x, y, fill="black")
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=str(str_node))
            node = nodes[key]
            draw_node(node.lesser_child_key, coords)
            draw_node(node.greater_child_key, coords)

        draw_node(root_key)


def visualize_species_trees(species_trees, df, dados_estatisticos):
    root_tk = tk.Tk()
    root_tk.title("AVL Trees")
    root_tk.geometry("1200x800")

    texto_label = "Ordem de exibição dos dados:\nSpecies\nSepal Length (cm) | Sepal Width (cm)\nPetal Length (cm) | Petal Width (cm)\n"

    label_text = tk.Label(root_tk, text=texto_label, font=("Arial", 12))
    label_text.pack(fill=tk.X)

    notebook = ttk.Notebook(root_tk)
    notebook.pack(fill=tk.BOTH, expand=True)

    for species, tree in species_trees.items():
        frame = AvlTreeVisualizer(notebook, species, tree, df)
        notebook.add(frame, text=species)

    tables_frame = ttk.Frame(notebook)
    texto_tables = "Exibição dos dados estatísticos coletados\nMédia\nMediana\nDesvio Padrão\n"
    notebook.add(tables_frame, text="Tabela")

    def on_tab_changed(event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "Tabela":
            label_text.config(text=texto_tables)
        else:
            label_text.config(text=texto_label)

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    tree = ttk.Treeview(tables_frame, columns=("A", "B", "C", "D", "E"), show="headings", height=20)
    tree.heading("A", text="especie")
    tree.heading("B", text="dado")
    tree.heading("C", text="media")
    tree.heading("D", text="mediana")
    tree.heading("E", text="desvio padrao")
    
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    especies = []
    dados = []
    medias = []
    medianas = []
    dps = []
    for especie in ["setosa", "versicolor", "virginica", "geral"]:
        for medida in ["petal_length", "petal_width", "sepal_length", "sepal_width"]:
            especies.append(especie)
            dados.append(medida)
            medias.append(dados_estatisticos["media"][especie][medida])
            medianas.append(dados_estatisticos["mediana"][especie][medida])
            dps.append(dados_estatisticos["desvio_padrao"][especie][medida])

    for i in range(len(dados)):
        tree.insert("", "end", values=(especies[i], dados[i], medias[i], medianas[i], dps[i]))


    root_tk.mainloop()