HEALTH_EXPENDITURE_SETTINGS = {
    "base_price_year": 2024,
    "default_deflator": "istat_nic_general",
    "default_accounting_basis": "competenza_ce",
    "public_output_formats": ["csv", "json"],
    "keep_cash_and_accrual_separate": True,
}

DEMOGRAPHIC_DENOMINATORS = [
    {"denominator_id": "population_total", "description": "Popolazione residente totale", "preferred_use": "spesa sanitaria totale e voci senza platea specifica"},
    {"denominator_id": "population_0", "description": "Popolazione residente con eta 0", "preferred_use": "neonatologia e prime prestazioni dell'infanzia"},
    {"denominator_id": "population_0_4", "description": "Popolazione residente 0-4 anni", "preferred_use": "prima infanzia"},
    {"denominator_id": "population_0_14", "description": "Popolazione residente 0-14 anni", "preferred_use": "pediatria e servizi per minori"},
    {"denominator_id": "population_0_17", "description": "Popolazione residente 0-17 anni", "preferred_use": "servizi sanitari per minori"},
    {"denominator_id": "births", "description": "Nati vivi nell'anno", "preferred_use": "nascite, parti, punti nascita, neonatologia"},
    {"denominator_id": "women_15_49", "description": "Donne residenti 15-49 anni", "preferred_use": "salute riproduttiva, gravidanza, consultori quando coerente"},
    {"denominator_id": "population_65_plus", "description": "Popolazione residente di 65 anni e oltre", "preferred_use": "cronicita, anziani, assistenza territoriale anziani"},
    {"denominator_id": "population_75_plus", "description": "Popolazione residente di 75 anni e oltre", "preferred_use": "lungodegenza, fragilita, non autosufficienza"},
    {"denominator_id": "population_80_plus", "description": "Popolazione residente di 80 anni e oltre", "preferred_use": "RSA, ADI anziani, non autosufficienza molto anziana"},
]
