import random

# MIGLIORAMENTO: Dati strutturati per le aliquote IRPEF per anno
ALIQUOTE_IRPEF = {
    2023: [
        {"soglia": 50000, "aliquota": 0.43, "imposta_fissa": 11000}, # Correzione logica: imposta dovuta fino a 50k
        {"soglia": 28000, "aliquota": 0.35, "imposta_fissa": 3450 + 3250}, # (15k*0.23 + 13k*0.25)
        {"soglia": 15000, "aliquota": 0.25, "imposta_fissa": 3450}, # (15k*0.23)
        {"soglia": 0, "aliquota": 0.23, "imposta_fissa": 0},
    ],
    2024: [
        {"soglia": 50000, "aliquota": 0.43, "imposta_fissa": 14100}, # (28k*0.23 + 22k*0.35)
        {"soglia": 28000, "aliquota": 0.35, "imposta_fissa": 6440}, # (28k*0.23)
        {"soglia": 0, "aliquota": 0.23, "imposta_fissa": 0},
    ],
    2025: [ # Assumendo che le aliquote 2025 siano le stesse del 2024
        {"soglia": 50000, "aliquota": 0.43, "imposta_fissa": 14100},
        {"soglia": 28000, "aliquota": 0.35, "imposta_fissa": 6440},
        {"soglia": 0, "aliquota": 0.23, "imposta_fissa": 0},
    ]
}

def calcola_irpef(reddito, anno):
    """Calcola l'IRPEF lorda basandosi su scaglioni progressivi."""
    scaglioni = ALIQUOTE_IRPEF.get(anno, ALIQUOTE_IRPEF[2025]) # Usa 2025 come default
    
    # Semplificazione del calcolo progressivo
    if anno == 2023:
        if reddito > 50000:
            return 11000 + (reddito - 50000) * 0.43
        if reddito > 28000:
            return 6700 + (reddito - 28000) * 0.35
        if reddito > 15000:
            return 3450 + (reddito - 15000) * 0.25
        return reddito * 0.23
    else: # Per 2024 e 2025
        if reddito > 50000:
            return 14100 + (reddito - 50000) * 0.43
        if reddito > 28000:
            return 6440 + (reddito - 28000) * 0.35
        return reddito * 0.23


def calcola_imposta_lorda(reddito, anno):
    """Calcola l'imposta lorda in base agli scaglioni IRPEF"""
    scaglioni = ALIQUOTE_IRPEF[anno]
    for scaglione in scaglioni:
        if reddito > scaglione["soglia"]:
            return scaglione["imposta_fissa"] + (reddito - scaglione["soglia"]) * scaglione["aliquota"]
    return 0.0

def detrazione_lavoro_dipendente(reddito):
    """Calcola la detrazione da lavoro dipendente (semplificata)"""
    if reddito <= 15000:
        return max(1880, 690)  # minimo 690
    elif reddito <= 28000:
        return 1910 + 1190 * (28000 - reddito) / 13000
    elif reddito <= 50000:
        return 1910 * (50000 - reddito) / 22000
    else:
        return 0.0

def calcola_imposta_netta(reddito, anno):
    """Calcola l'imposta netta (lorda - detrazione)"""
    lorda = calcola_imposta_lorda(reddito, anno)
    detrazione = detrazione_lavoro_dipendente(reddito)
    netta = max(0, lorda - detrazione)
    return {
        "reddito": reddito,
        "anno": anno,
        "imposta_lorda": round(lorda, 2),
        "detrazione": round(detrazione, 2),
        "imposta_netta": round(netta, 2)
    }

def get_or_create_summary_data(anagrafica_obj):
    """
    Recupera i dati di riepilogo per l'utente, generando dati simulati
    con calcoli IRPEF più accurati e valori coerenti.
    """
    anni = [2023, 2024, 2025]
    riepiloghi = []
    is_simulated = True

    potenziale_recupero_corrente = random.uniform(800, 2000)

    for anno in anni:
        reddito_lordo = random.uniform(28000, 45000)
        
        # MIGLIORAMENTO: Usa la funzione di calcolo IRPEF invece di un moltiplicatore casuale
        imposte = calcola_irpef(reddito_lordo, anno)
        
        # Aggiungiamo una simulazione per le addizionali regionali/comunali
        imposte += reddito_lordo * random.uniform(0.015, 0.03)

        if anno == anni[-1]:
            rimborso = potenziale_recupero_corrente * random.uniform(0.5, 1.0)
        else:
            rimborso = reddito_lordo * random.uniform(0.02, 0.05)
        
        reddito_netto = reddito_lordo - imposte + rimborso
        
        riepilogo = {
            "anno": anno,
            "reddito_netto": round(reddito_netto, 2),
            "imposte_versate": round(imposte, 2),
            "rimborso_ottenuto": round(rimborso, 2),
        }
        riepiloghi.append(riepilogo)

    recupero_attuale_corrente = riepiloghi[-1]['rimborso_ottenuto']

    consigli = [
        "Hai detratto spese mediche? Ricorda di conservare tutti gli scontrini parlanti.",
        "Se hai fatto donazioni a enti del terzo settore, potresti avere diritto a una detrazione.",
        "Valuta l'adesione a un fondo pensione complementare per beneficiare di vantaggi fiscali."
    ]

    return {
        "is_simulated": is_simulated,
        "bar_chart_data": {
            "labels": [r['anno'] for r in riepiloghi],
            "datasets": [
                {"label": "Reddito Netto", "data": [r['reddito_netto'] for r in riepiloghi], "backgroundColor": "#4e73df"},
                {"label": "IRPEF e Addizionali dopo detrazioni standard", "data": [r['imposte_versate'] for r in riepiloghi], "backgroundColor": "#e74a3b"},
                {"label": "Recupero da 730", "data": [r['rimborso_ottenuto'] for r in riepiloghi], "backgroundColor": "#1cc88a"},
            ]
        },
        "gauge_chart_data": {
            "recupero_attuale": round(recupero_attuale_corrente, 2),
            "potenziale_recupero": round(potenziale_recupero_corrente, 2)
        },
        "advice_data": consigli
    }

