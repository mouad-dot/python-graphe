import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from matplotlib.table import table
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import pandas as pd

# Constantes
DESCRIPTION_COL = 'DESCRIPTION'
TIME_COL = 'TIME (ISO-8601)'
EMAIL_COL = 'email'
LAST_NAME_COL = 'last_name'
FILTER_DESCRIPTION_CONTAINS = 'Factory QBASE called the api API_DoQuery on table Professionals in app WP - Web Platform'

# Variable globale pour le chemin du fichier CSV
input_csv_path = ""

# Fonction pour lire le fichier CSV
def read_csv_file(file_path, email_filter=None):
    print(f"Lecture du fichier CSV : {file_path}")
    dtype_specification = {10: 'str'}
    
    # Lire le fichier CSV avec les spécifications de type
    df = pd.read_csv(file_path, parse_dates=[TIME_COL], dtype=dtype_specification, low_memory=False)
    df[TIME_COL] = pd.to_datetime(df[TIME_COL], errors='coerce')
    
    # Vérifier si les colonnes requises existent
    required_columns = [DESCRIPTION_COL, TIME_COL, EMAIL_COL, LAST_NAME_COL]
    print(f"Colonnes dans le CSV : {df.columns.tolist()}")
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"La colonne {col} est manquante dans le fichier CSV.")

    # Filtrer par email si nécessaire
    if email_filter:
        df = df[df[EMAIL_COL] == email_filter]
    
    print(f"Forme du DataFrame après lecture : {df.shape}")
    return df

# Fonction pour générer les données pour le tableau 2 (Description)
def generate_data_tableau_2(df, filter_value):
    print(f"Génération des données pour le tableau 2 avec le filtre : {filter_value}")
    df_filtered = df[df[DESCRIPTION_COL].str.contains(filter_value, case=False, na=False)]
    df_filtered[DESCRIPTION_COL] = df_filtered[DESCRIPTION_COL].str.replace("Factory QBASE ", "", regex=False)
    total_calls_by_description = df_filtered.groupby(DESCRIPTION_COL).size().reset_index(name='Total Calls')
    print(f"Forme du DataFrame pour le tableau 2 : {total_calls_by_description.shape}")
    return total_calls_by_description.sort_values('Total Calls', ascending=False)

# Fonction pour générer les données pour le tableau 2 (Nom de famille)
def generate_data_tableau_last_name(df, filter_value):
    print(f"Génération des données pour le tableau 2 avec le filtre sur le nom de famille : {filter_value}")
    df_filtered = df[df[LAST_NAME_COL].str.contains(filter_value, case=False, na=False)]
    total_calls_by_last_name = df_filtered.groupby(LAST_NAME_COL).size().reset_index(name='Total Calls')
    print(f"Forme du DataFrame pour le tableau 2 (nom de famille) : {total_calls_by_last_name.shape}")
    return total_calls_by_last_name.sort_values('Total Calls', ascending=False)

# Fonction pour générer les données pour le tableau 2 (Date)
def generate_data_tableau_date(df, filter_value):
    print(f"Génération des données pour le tableau 2 avec le filtre sur la date : {filter_value}")
    filter_date = pd.to_datetime(filter_value, errors='coerce')
    df_filtered = df[df[TIME_COL].dt.date == filter_date.date()]
    total_calls_by_date = df_filtered.groupby(df_filtered[TIME_COL].dt.date).size().reset_index(name='Total Calls')
    print(f"Forme du DataFrame pour le tableau 2 (date) : {total_calls_by_date.shape}")
    return total_calls_by_date

# Fonction pour remplir les jours manquants avec des valeurs nulles ou par défaut
def fill_missing_days(df, date_column):
    print(f"Remplissage des jours manquants pour la colonne : {date_column}")
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    date_range = pd.date_range(start=df[date_column].min(), end=df[date_column].max())
    full_date_range_df = pd.DataFrame({date_column: date_range})
    df_filled = pd.concat([full_date_range_df.set_index(date_column), df.set_index(date_column)], axis=1, join='outer').reset_index()
    df_filled['Total Calls'] = df_filled['Total Calls'].fillna(0)
    print(f"Forme du DataFrame après remplissage des jours manquants : {df_filled.shape}")
    return df_filled

# Tableau 3
def generate_data_tableau_3(df):
    print("Génération des données pour le tableau 3")
    df[TIME_COL] = pd.to_datetime(df[TIME_COL], errors='coerce')
    total_calls_by_day = df.groupby(df[TIME_COL].dt.date).size().reset_index(name='Total Calls')
    total_calls_by_day.columns = [TIME_COL, 'Total Calls']
    total_calls_by_day = fill_missing_days(total_calls_by_day, TIME_COL)
    print(f"Forme du DataFrame pour le tableau 3 : {total_calls_by_day.shape}")
    return total_calls_by_day

# Tableau 4
def generate_data_tableau_4(df):
    print("Génération des données pour le tableau 4")
    df_pro = df[df[DESCRIPTION_COL].str.contains(FILTER_DESCRIPTION_CONTAINS, na=False)]
    total_calls_by_day_pro = df_pro.groupby(df_pro[TIME_COL].dt.date).size().reset_index(name='Total Calls')
    total_calls_by_day_pro.columns = [TIME_COL, 'Total Calls']
    print(f"Forme du DataFrame pour le tableau 4 : {total_calls_by_day_pro.shape}")
    return total_calls_by_day_pro

# Fonction pour tracer le Tableau 2
def plot_tableau_2(data):
    print("Tracé du tableau 2")
    if data.empty:
        print("Aucune donnée disponible à tracer pour le tableau 2")
        return None
    fig, ax = plt.subplots(figsize=(11.7, 8.3))
    ax.axis('tight')
    ax.axis('off')
    table_data = data.values.tolist()
    the_table = table(ax, cellText=table_data, colLabels=data.columns, loc='center', cellLoc='center', rowLoc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(8)
    the_table.scale(1.2, 1.2)
    plt.title('Appels totaux par description')
    return fig

# Fonction pour tracer le Tableau 3
def plot_tableau_3(data):
    print("Tracé du tableau 3")
    if data.empty:
        print("Aucune donnée disponible à tracer pour le tableau 3")
        return None
    fig, ax = plt.subplots(figsize=(11.7, 8.3))
    ax.bar(data[TIME_COL], data['Total Calls'], align='center', alpha=0.5)
    ax.set_xlabel('Jour')
    ax.set_ylabel('Appels totaux')
    ax.set_title('Appels totaux par jour')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Fonction pour tracer le Tableau 4
def plot_tableau_4(data):
    print("Tracé du tableau 4")
    if data.empty:
        print("Aucune donnée disponible à tracer pour le tableau 4")
        return None
    fig, ax = plt.subplots(figsize=(11.7, 8.3))
    ax.plot(data[TIME_COL], data['Total Calls'])
    ax.set_xlabel('Jour')
    ax.set_ylabel('Appels totaux')
    ax.set_title('Appels totaux par jour pour les segments professionnels')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# Fonction pour calculer le pourcentage de lignes pour un filtre d'email donné
def calculate_email_percentage(df, filter_email):
    print(f"Calcul du pourcentage d'emails pour : {filter_email}")
    total_rows = len(df)
    filtered_rows = len(df[df[EMAIL_COL] == filter_email])
    percentage = (filtered_rows / total_rows) * 100
    return percentage

# Fonction pour générer le PDF avec un écran de chargement
def generate_pdf_with_loading(filter_method, filter_value, csv_path):
    global input_csv_path
    
    input_csv_path = csv_path
    print(f"Génération du PDF avec méthode de filtre : {filter_method}, valeur de filtre : {filter_value}, chemin du CSV : {csv_path}")
    
    try:
        # Lire le fichier CSV
        df = read_csv_file(input_csv_path)

        data_tableau_2 = None
        data_tableau_3 = None
        data_tableau_4 = None
        email_percentage = None

        if filter_method == 'Email':
            filter_value = filter_value.strip()
            df_filtered = df.loc[df[EMAIL_COL] == filter_value].copy()
            print(f"Forme du DataFrame après filtrage par email : {df_filtered.shape}")

            if not df_filtered.empty and set([DESCRIPTION_COL, TIME_COL]).issubset(df_filtered.columns):
                data_tableau_2 = generate_data_tableau_2(df_filtered, FILTER_DESCRIPTION_CONTAINS)
                data_tableau_3 = generate_data_tableau_3(df_filtered)
                data_tableau_4 = generate_data_tableau_4(df_filtered)
            else:
                print("Aucune donnée trouvée pour le filtre email sélectionné.")

            email_percentage = calculate_email_percentage(df, filter_value)
        else:
            if filter_method == 'Description':
                data_tableau_2 = generate_data_tableau_2(df, filter_value)
            elif filter_method == 'Date':
                data_tableau_2 = generate_data_tableau_date(df, filter_value)
            elif filter_method == 'Last name':
                data_tableau_2 = generate_data_tableau_last_name(df, filter_value)

            data_tableau_3 = generate_data_tableau_3(df)
            data_tableau_4 = generate_data_tableau_4(df)

            # Calculer le pourcentage d'emails pour chaque email unique
            email_percentage = calculate_email_percentage(df, filter_value)

        # Vérifier si des figures sont générées avant de créer le PDF
        figures = []

        if data_tableau_2 is not None:
            fig = plot_tableau_2(data_tableau_2)
            if fig:
                figures.append(fig)

        if data_tableau_3 is not None:
            fig = plot_tableau_3(data_tableau_3)
            if fig:
                figures.append(fig)

        if data_tableau_4 is not None:
            fig = plot_tableau_4(data_tableau_4)
            if fig:
                figures.append(fig)

        if email_percentage is not None:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie([email_percentage, 100 - email_percentage], labels=[f'{filter_value} ({email_percentage:.2f}%)', 'Autres'], autopct='%1.1f%%', startangle=140)
            ax.set_title(f'Distribution des emails : {filter_value}')
            figures.append(fig)

        if figures:
            with PdfPages(f'QuickbaseAnalysis-{datetime.now().strftime("%Y-%m-%d")}.pdf') as pdf:
                for fig in figures:
                    pdf.savefig(fig)
                    plt.close(fig)
            return True
        else:
            messagebox.showwarning("Avertissement", "Aucune figure n'a été générée pour le PDF.")
            return False

    except IndexError as ie:
        messagebox.showerror("Erreur", f"IndexError : {ie}. Vérifiez vos accès aux index dans le code.")
        return False

    except ValueError as ve:
        messagebox.showerror("Erreur", f"ValueError : {ve}")
        return False

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
        return False

# Fonction pour gérer le clic sur le bouton et afficher la boîte de dialogue de fichier
def select_csv_file():
    global input_csv_path
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
    if file_path:
        input_csv_path = file_path
        process_filter(input_csv_path)

# Fonction pour gérer le clic sur le bouton et afficher l'écran de chargement
def process_filter(csv_path):
    filter_method = filter_method_var.get()
    filter_value = filter_entry.get()
    
    if filter_method and filter_value:
        if filter_method in ['Email', 'Description', 'Date', 'Last name']:
            loading_screen = tk.Toplevel(root)
            loading_screen.title("Chargement...")
            loading_label = ttk.Label(loading_screen, text="Génération du PDF, veuillez patienter...")
            loading_label.pack(padx=20, pady=20)
            
            loading_screen.update_idletasks()
            
            success = generate_pdf_with_loading(filter_method, filter_value, csv_path)
            
            loading_screen.destroy()
            
            if success:
                messagebox.showinfo("Succès", "PDF généré avec succès.")
                root.destroy()
        else:
            messagebox.showwarning("Avertissement", "Méthode de filtre sélectionnée invalide.")
    else:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner une méthode de filtre et entrer une valeur.")

# Fenêtre principale Tkinter
root = tk.Tk()
root.title("Générateur de PDF")
root.geometry("600x400")
root.configure(bg='lightblue')

# Cadre pour contenir les options de filtre
filter_frame = ttk.Frame(root, padding=(100,90))
filter_frame.pack()

# Liste déroulante pour la méthode de filtre
filter_method_label = ttk.Label(filter_frame, text="Sélectionnez la méthode de filtre :")
filter_method_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

filter_method_var = tk.StringVar()
filter_method_combobox = ttk.Combobox(filter_frame, textvariable=filter_method_var, values=['Email', 'Description', 'Date', 'Last name'])
filter_method_combobox.current(0)
filter_method_combobox.grid(row=0, column=1, padx=10, pady=5)

# Champ de saisie pour la valeur du filtre
filter_value_label = ttk.Label(filter_frame, text="Entrez la valeur du filtre :")
filter_value_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

filter_entry = ttk.Entry(filter_frame, width=50)
filter_entry.grid(row=1, column=1, padx=10, pady=5)

# Bouton pour sélectionner le fichier CSV
select_file_button = ttk.Button(root, text="Sélectionner le fichier CSV", command=select_csv_file)
select_file_button.pack(pady=10)

# Bouton pour générer le PDF
process_button = ttk.Button(root, text="Générer le PDF", command=lambda: process_filter(input_csv_path))
process_button.pack(pady=10)

root.mainloop()
