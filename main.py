import csv
import matplotlib.pyplot as plt

# Initialiser tom dictionary for å lagre data for hver stemmekrets
area_data = {}

# Løkke som går gjennom alle filene i CSV-mappa, leser data og kopierer til dictionary
for i in [2015, 2019, 2023]:
    filename = f"csv/2026-10-10_{i}_ko_partifordeling_halden_stemmekrets.csv"
    with open(filename, "r") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            area = row["Stemmekretsnavn"]
            if area not in area_data:
                area_data[area] = {}
            if row["Partinavn"] not in area_data[area]:
                area_data[area][row["Partinavn"]] = []
            area_data[area][row["Partinavn"]].append((i, float(row["Oppslutning prosentvis"])))


# Dictionary for å koble partier og farger
party_colors = {
    "Arbeiderpartiet": "red",
    "Høyre": "blue",
    "Senterpartiet": "lime",
    "Miljøpartiet De Grønne": "green",
    "Sosialistisk Venstreparti": "hotpink",
    "Rødt" : "darkred",
    "Kristelig Folkeparti" : "yellow",
    "Venstre" : "teal",
    "Fremskrittspartiet" : "navy",
    "Pensjonistpartiet" : "slateblue",
    "Partiet De Kristne" : "orange",
    "Norgesdemokratene" : "brown",
    "Industri- og Næringspartiet" : "darkorange",
    "Konservativt" : "slategrey",
    "Liberalistene" : "purple",
    "Andre" : "grey",
}

# Dictionary for å kombinere partier under felles navn
combined_parties = {
    "Andre": ["Konservativt", "Liberalistene","Partiet De Kristne","Norgesdemokratene"],
}

# Funksjon for å kombinere data fra flere partier
def combine_party_data(parties, combined_parties):
    combined_data = {}
    all_years = set(year for party in parties.values() for year, _ in party)
    
    for label, party_list in combined_parties.items():
        combined_data[label] = []
        
        for year in sorted(all_years):
            values_sum = 0
            count = 0
            
            for party in party_list:
                if party in parties and any(d[0] == year for d in parties[party]):
                    values_sum += next((d[1] for d in parties[party] if d[0] == year), 0)
                    count += 1
                else:
                    values_sum += 0
            
            combined_data[label].append((year, values_sum / count if count > 0 else 0))
    
    # Return the list of combined party names
    return combined_data, list(combined_parties.values())[0]

# Plott data for hver stemmekrets
for area, parties in area_data.items():
    plt.figure(figsize=(12, 8)) 
    combined_parties_data, combined_party_names = combine_party_data(parties, combined_parties)
    
    # Plott kombinerte partier (andre)
    for label, data in combined_parties_data.items():
        x = [year for year, _ in data]
        y = [value for _, value in data]
        color = party_colors.get(label, "black")  # Bruk svart hvis ikke farge oppgitt
        plt.plot(x, y, label=label, color=color, marker='s')
    
    # Plott partier som ikke er kombinert
    for party, data in parties.items():
        if party not in combined_party_names:
            x = [year for year, _ in data]
            y = [value for _, value in data]
            color = party_colors.get(party, "black")  # Bruk svart hvis ikke farge oppgitt
            plt.plot(x, y, label=party, color=color, marker='o')
    
    plt.xlabel("År")
    plt.ylabel("Oppslutning i prosent")
    plt.title(f"Valgresultat for {area} stemmekrets")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig(f"plots/{area}_valgresultat.png")
