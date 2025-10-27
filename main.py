import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
import numpy as np

class DiagrammeCirculaireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Créateur de diagramme circulaire")
        self.root.geometry("550x400")
        
        self.zones = []
        
        # Étape 1 : choix du nombre de zones
        self.label_intro = tk.Label(root, text="Nombre de zones (1 à 100) :", font=("Arial", 12))
        self.label_intro.pack(pady=10)
        
        self.entry_nb_zones = tk.Entry(root, width=10)
        self.entry_nb_zones.pack()
        
        self.btn_valider = tk.Button(root, text="Valider", command=self.creer_champs)
        self.btn_valider.pack(pady=10)
        
        self.frame_zones = tk.Frame(root)
        self.frame_zones.pack(pady=10)
        
        self.btn_creer = tk.Button(root, text="Prévisualiser le diagramme", command=self.previsualiser_diagramme)
        self.btn_creer.pack(pady=10)
    
    def creer_champs(self):
        """Crée dynamiquement les champs pour chaque zone."""
        for widget in self.frame_zones.winfo_children():
            widget.destroy()
        
        try:
            nb = int(self.entry_nb_zones.get())
            if nb < 1 or nb > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide entre 1 et 100.")
            return
        
        self.zones = []
        
        for i in range(nb):
            frame = tk.Frame(self.frame_zones)
            frame.pack(pady=4)
            
            tk.Label(frame, text=f"Zone {i+1} :", width=8).pack(side="left")
            
            name_entry = tk.Entry(frame, width=10)
            name_entry.insert(0, f"zone{i+1}")
            name_entry.pack(side="left", padx=3)

            color_entry = tk.Entry(frame, width=10)
            color_entry.insert(0, "blue")
            color_entry.pack(side="left", padx=3)
            
            val_entry = tk.Entry(frame, width=5)
            val_entry.insert(0, "5")
            val_entry.pack(side="left", padx=3)
            
            total_entry = tk.Entry(frame, width=5)
            total_entry.insert(0, "10")
            total_entry.pack(side="left", padx=3)
            
            self.zones.append((name_entry, color_entry, val_entry, total_entry))
    
    def generer_donnees(self):
        """Récupère les données saisies."""
        labels, values, colors = [], [], []
        
        for i, (name_entry, color_entry, val_entry, total_entry) in enumerate(self.zones):
            try:
                name = name_entry.get().strip()
                color = color_entry.get().strip()
                val = float(val_entry.get())
                total = float(total_entry.get())
                if total <= 0:
                    raise ValueError
                
                ratio = min(max(val / total, 0), 1)
                labels.append(name if name else f"Zone {i+1}")
                values.append(ratio)
                colors.append(color)
            except ValueError:
                messagebox.showerror("Erreur", f"Valeurs invalides pour la zone {i+1}.")
                return None
        return labels, values, colors
    
    def previsualiser_diagramme(self):
        """Affiche une prévisualisation avant enregistrement."""
        donnees = self.generer_donnees()
        if not donnees:
            return
        
        labels, values, colors = donnees
        
        # Création du diagramme
        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_axis_off()
        ax.set_ylim(0, 1)

        num_sections = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_sections + 1)
        
        for i, (angle_start, angle_end, value, color) in enumerate(zip(angles[:-1], angles[1:], values, colors)):
            theta = np.linspace(angle_start, angle_end, 100)
            r_inner = np.zeros_like(theta)
            r_outer = np.ones_like(theta) * value
            ax.fill_between(theta, r_inner, r_outer, color=color, alpha=0.8)
        
        # Cercles repères
        circle_5 = plt.Circle((0, 0), 0.5, transform=ax.transData._b,
                              color='grey', fill=False, linestyle='--', linewidth=1.5, alpha=0.8)
        circle_10 = plt.Circle((0, 0), 1.0, transform=ax.transData._b,
                               color='black', fill=False, linestyle='-', linewidth=2.5, alpha=1)
        ax.add_artist(circle_5)
        ax.add_artist(circle_10)
        
        # Légende (affiche le nom saisi par l’utilisateur)
        for label, color in zip(labels, colors):
            ax.bar(0, 0, color=color, label=label)
        ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
        
        # Fenêtre de prévisualisation
        def enregistrer():
            filename = simpledialog.askstring("Nom du fichier", "Entrez le nom du fichier (sans extension) :")
            if filename:
                fig.savefig(f"{filename}.png", bbox_inches='tight')
                plt.close(fig)
                messagebox.showinfo("Succès", f"Diagramme enregistré sous '{filename}.png' !")
                preview.destroy()
            else:
                messagebox.showinfo("Annulé", "Enregistrement annulé.")
        
        def modifier():
            plt.close(fig)
            preview.destroy()
        
        preview = tk.Toplevel(self.root)
        preview.title("Prévisualisation du diagramme")
        preview.geometry("400x100")
        
        tk.Label(preview, text="Voici un aperçu du diagramme généré.", font=("Arial", 11)).pack(pady=10)
        tk.Button(preview, text="Enregistrer", command=enregistrer, bg="lightgreen").pack(side="left", expand=True, padx=20)
        tk.Button(preview, text="Modifier", command=modifier, bg="lightcoral").pack(side="right", expand=True, padx=20)
        
        plt.show()


# Lancement de l’application
if __name__ == "__main__":
    root = tk.Tk()
    app = DiagrammeCirculaireApp(root)
    root.mainloop()
