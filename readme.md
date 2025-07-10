# Bol.com Product Data Processing Pipeline

## Project Overzicht
Dit Python project verwerkt productdata van bol.com voor cadeau-categorieën selectie. Het bevat scripts voor het voorbereiden, filteren en samenvoegen van productdatasets in een gestructureerde pipeline.

## Doel
Het doel is om uit verschillende productcategorieën relevante producten te selecteren en te categoriseren voor een cadeau-selectie systeem, waarbij alleen producten worden behouden die voldoen aan specifieke criteria (snelle levering, nieuw, betaalbaar).

## Folderstructuur

### 📂 **Initiële folderstructuur (voor pipeline uitvoering)**
```
Tweede selectie bol/
├── Chunking/
│   ├── chunking.py
│   └── home-interior.csv
├── Datasets/
│   ├── baby.csv
│   ├── computer.csv
│   ├── daily-care.csv
│   ├── diy.csv
│   ├── dutch-books.csv
│   ├── entertainment.csv
│   ├── fashion-accessories.csv
│   ├── fashion-footwear.csv
│   ├── feed_sports.csv
│   ├── health.csv
│   ├── kitchen-household.csv
│   ├── mobile.csv
│   ├── outdoor-mobility.csv
│   ├── pet.csv
│   ├── sound-vision.csv
│   └── toys.csv
├── Subssubcategorieën sheet/
│   └── create_subssubcategories_sheet.py
├── Datasets gecleaned/
│   └── clean_datasets.py
├── Dataset compleet/
│   └── merge_datasets.py
├── main.py
├── readme.md
├── requirements.txt
└── venv/
```

### 📂 **Finale folderstructuur (na pipeline uitvoering)**
```
Tweede selectie bol/
├── Chunking/
│   ├── chunk_1.csv
│   ├── chunk_2.csv
│   ├── chunk_3.csv
│   ├── chunk_4.csv
│   ├── chunking.py
│   └── home-interior_original.csv
├── Datasets/
│   ├── baby.csv
│   ├── computer.csv
│   ├── daily-care.csv
│   ├── diy.csv
│   ├── dutch-books.csv
│   ├── entertainment.csv
│   ├── fashion-accessories.csv
│   ├── fashion-footwear.csv
│   ├── feed_sports.csv
│   ├── health.csv
│   ├── home-interior.csv (chunk_1)
│   ├── kitchen-household.csv
│   ├── mobile.csv
│   ├── outdoor-mobility.csv
│   ├── pet.csv
│   ├── sound-vision.csv
│   └── toys.csv
├── Subssubcategorieën sheet/
│   ├── create_subssubcategories_sheet.py
│   └── subssubcategorieën.csv
├── Datasets gecleaned/
│   ├── baby.csv
│   ├── clean_datasets.py
│   ├── computer.csv
│   ├── daily-care.csv
│   ├── diy.csv
│   ├── dutch-books.csv
│   ├── entertainment.csv
│   ├── fashion-accessories.csv
│   ├── fashion-footwear.csv
│   ├── feed_sports.csv
│   ├── health.csv
│   ├── home-interior.csv
│   ├── kitchen-household.csv
│   ├── mobile.csv
│   ├── outdoor-mobility.csv
│   ├── pet.csv
│   ├── sound-vision.csv
│   └── toys.csv
├── Dataset compleet/
│   ├── bol subcategorieën selectie compleet.csv
│   └── merge_datasets.py
├── main.py
├── readme.md
├── requirements.txt
└── venv/
```

## Folderstructuur & Functionaliteit

### 📁 **Chunking/** (bevat chunking.py)
**Functie**: Verdeelt grote datasets voor betere prestaties
- Chunkt het ~20GB home-interior.csv bestand in 4 gelijke delen
- Chunk 1 komt terecht in Datasets/
- Origineel bestand + chunks 2-4 worden opgeslagen in Chunking/
- Gebruik: Nodig voor verwerking van grote datasets

### 📁 **Datasets/**
**Functie**: Opslagplaats voor originele productdata
- Bevat 17 productcategorieën als CSV bestanden (baby, computer, health, etc.)
- Gebruikt "|" als delimiter
- home-interior.csv is gechunked voor performance
- Bron: Originele bol.com productdata

### 📁 **Subssubcategorieën sheet/** (bevat create_subssubcategories_sheet.py)
**Functie**: Genereert overzicht van alle productsubcategorieën
- Analyseert alle datasets en extraheert unieke subssubgroepen
- Creëert `subssubcategorieën.csv` met:
  - **Match**: Lege kolom voor handmatige cadeau-categorieën
  - **Category.category**: Productcategorie naam
  - **Category.subssubgroup**: Subssubgroep naam
  - **Aantal**: Aantal producten per subssubgroep
  - **Voorbeeld_product_titel**: Voorbeeldproduct titel
  - **Voorbeeld_product_beschrijving**: Voorbeeldproduct beschrijving
  - **Voorbeeld_product_link**: Link naar voorbeeldproduct
- Output: "," delimiter voor Google Sheets import

### 📁 **Datasets gecleaned/** (bevat clean_datasets.py)
**Functie**: Filtert en zuivert productdata
- **Kolom filtering**: Behoudt alleen relevante kolommen:
  - `productId`, `ean`, `title`, `productPageUrlNL`, `imageUrl`, `description`
  - `OfferNL.sellingPrice`, `OfferNL.condition`, `OfferNL.isDeliverable`, `OfferNL.maximalDeliveryDays`
  - `Category.category`, `Category.productgroup`, `Category.subgroup`, `Category.subssubgroup`
- **Product filtering**: Alleen producten die voldoen aan:
  - Levering ≤ 2 dagen
  - Conditie = 'new'
  - Leverbaar = 'Y'
  - Prijs tussen €10 - €250
- Behoudt "|" delimiter

### 📁 **Dataset compleet/** (bevat merge_datasets.py)
**Functie**: Combineert alle data tot eindresultaat
- Merged alle gecleande datasets met subssubcategorieën matches
- Behoudt alleen producten met handmatige Match waarde
- Output: `bol subcategorieën selectie compleet.csv`
- Gebruikt "," delimiter voor eindresultaat

## Pipeline Uitvoering

### 🚀 **main.py**
**Functie**: Geautomatiseerde pipeline orchestratie
- Voert alle stappen sequentieel uit
- Interactieve gebruikersinput per stap
- Controleert of stappen al uitgevoerd zijn
- Foutafhandeling en voortgangsindicatie

**Stappen**:
1. **Chunking**: Verdeelt home-interior.csv
2. **Subcategorieën**: Maakt overzichtsbestand
3. **Cleaning**: Filtert en zuivert data
4. **Merging**: Combineert tot eindresultaat

Volg de interactieve prompts om de pipeline uit te voeren.

## Resultaten
Na voltooiing van de pipeline:
- **Gechunkte bestanden**: `./Chunking/`
- **Subssubcategorieën overzicht**: `./Subssubcategorieën sheet/subssubcategorieën.csv`
- **Gecleande datasets**: `./Datasets gecleaned/`
- **Eindresultaat**: `./Dataset compleet/bol subcategorieën selectie compleet.csv`