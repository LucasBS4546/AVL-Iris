import tkinter as tk
from avltree import AvlTree

class AvlTreeVisualizer(tk.Toplevel):
    def __init__(self, master_tk, window_title, tree):
        super().__init__(master_tk)
        self.title(window_title)
        self.geometry("1200x800")
        self.canvas = tk.Canvas(self, bg="white", width=1200, height=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.tree = tree
        self.node_radius = 20
        self.level_height = 80
        self.horizontal_spacing = 40

        self.__draw_tree()

    def __draw_tree(self):

        root_key = self.tree._AvlTree__root_key
        if root_key is None:
            return

        nodes = self.tree._AvlTree__nodes

        # Calcular posições x
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

        # Calcular escala horizontal
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

            # Desenhar linha para o pai
            if parent_coords:
                self.canvas.create_line(parent_coords[0], parent_coords[1], x, y, fill="black")

            # Desenhar nó (círculo e texto)
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius, fill="lightblue")
            self.canvas.create_text(x, y, text=str(round(key, 2)))

            node = nodes[key]
            draw_node(node.lesser_child_key, coords)
            draw_node(node.greater_child_key, coords)

        draw_node(root_key)


def visualize_species_trees(species_trees):
    root_tk = tk.Tk()
    root_tk.withdraw()

    for species, tree in species_trees.items():
        AvlTreeVisualizer(root_tk, species, tree)

    root_tk.mainloop()
