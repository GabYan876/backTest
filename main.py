import json
import re

filename = 'data.json'

def add(name, profit):
    # Charger les données depuis le fichier JSON
    with open(filename, 'r') as file:
        data = json.load(file)

    name = name.lower()
    
    # Trouver la devise correspondante et ajouter le profit
    devise_trouvee = False
    for devise in data:
    
        if devise["name"].lower() == name:
            devise["code"].append(profit)
            devise_trouvee = True
            break
    
    if not devise_trouvee:
        print(f"Erreur : La devise '{name}' n'a pas été trouvée.")
        return
    
    # Sauvegarder les données modifiées dans le fichier JSON
    with open(filename, 'w') as file:
        json_str = json.dumps(data, indent=4, separators=(',', ': '))
        
        # Manipuler le texte pour ajouter une ligne vide entre les objets mais pas dans les listes internes
        json_str = re.sub(r'\[\n\s+', '[', json_str)
        json_str = re.sub(r',\n\s+', ', ', json_str)
        json_str = re.sub(r'\n\s+\]', ']', json_str)
        json_str = json_str.replace('},\n{', '},\n\n{')
        
        file.write(json_str)
    
    print(f"Profit de {profit} ajouté à la devise '{name}'.")

def total():
    # Charger les données depuis le fichier JSON
    with open(filename, 'r') as file:
        data = json.load(file)

    # Créer une liste avec les noms de devises, leurs totaux, taux de réussite et nombre de trades
    devise_totals = []
    total_trades_global = 0
    total_trades_positifs_global = 0
    total_global = 0

    for devise in data:
        total_devise = sum(devise["code"])  # Calculer le total des profits
        total_trades = len(devise["code"])  # Nombre total de trades
        trades_positifs = len([profit for profit in devise["code"] if profit > 0])  # Compter les trades positifs
        taux_reussite = round((trades_positifs / total_trades * 100), 0) if total_trades > 0 else 0  # Arrondir le taux de réussite à l'unité près

        # Ajouter les résultats de la devise à la liste
        devise_totals.append((devise['name'], total_devise, taux_reussite, total_trades))

        # Mettre à jour les totaux globaux
        total_global += total_devise
        total_trades_global += total_trades
        total_trades_positifs_global += trades_positifs

    # Calculer le taux de réussite global
    taux_reussite_global = round((total_trades_positifs_global / total_trades_global * 100), 0) if total_trades_global > 0 else 0

    # Trier la liste des devises par leur total de profits en ordre décroissant
    devise_totals.sort(key=lambda x: x[1], reverse=True)

    # Afficher les devises triées, leurs profits, taux de réussite et nombre de trades
    for name, total_devise, taux_reussite, total_trades in devise_totals:
        print(f"Le profit total pour {name} est de : {total_devise} "
              f"({total_trades}/{taux_reussite:.0f}%)")

    # Afficher le total global, le nombre de trades et le taux de réussite global
    print(f"\nLe total global est de : {total_global} ({total_trades_global}/{taux_reussite_global:.0f}%).")

def main():
    while True:
        userInput = input("Entrez une commande (ou 'quit' pour sortir) : ").strip()
        
        match userInput:

            case "quit":
                break

            case "a":
                name = input("Name: ").strip().lower()
                profitInput = input("Profit: ").strip()
                try:
                    profit = int(profitInput)
                    add(name, profit)
                except ValueError:
                    print("Erreur.")

            case "t":
                try:
                    total()
                except ValueError:
                    print("Erreur.")

            case _:
                print("Commande non reconnue. Veuillez réessayer.")

if __name__ == "__main__":
    main()