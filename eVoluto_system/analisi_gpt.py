# gpt_relazione.py

def genera_relazione_finale(analisi_tecnica: str, nome_azienda: str = "", periodo: str = "") -> str:
    prompt = f"""
Agisci come consulente aziendale esperto.
Trasforma l’analisi tecnica qui sotto in una relazione professionale per un imprenditore, con linguaggio semplice e valore strategico.

🧩 Dati aggiuntivi:
- Azienda: {nome_azienda if nome_azienda else "non specificata"}
- Periodo di riferimento: {periodo if periodo else "non indicato"}

📄 Analisi tecnica:
{analisi_tecnica}

🎯 Output atteso:
- Riassunto dei punti chiave dell'analisi
- Indicazioni sui benefici strategici
- Linguaggio chiaro e coinvolgente
- Conclusione con una frase come: “Richiedi un approfondimento gratuito per conoscere le azioni consigliate.”
"""
    return prompt
