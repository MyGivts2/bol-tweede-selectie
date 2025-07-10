import os
import sys
from pathlib import Path

# Add subdirectories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Chunking'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Subssubcategorieën sheet'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Datasets gecleaned'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Dataset compleet'))

def ask_user(question):
    """Ask user a yes/no question"""
    while True:
        answer = input(f"{question} (j/n): ").lower()
        if answer in ['j', 'n']:
            return answer == 'j'
        print("Voer alstublieft 'j' voor ja of 'n' voor nee in.")

def main():
    print("=== Tweede selectie bol - Data Processing Pipeline ===\n")
    
    # Step 1: Chunking
    print("STAP 1: Home-interior.csv chunken")
    print("Dit verdeelt het grote home-interior.csv bestand (~20GB) in 4 delen.")
    
    if not ask_user("Is het chunken al gedaan?"):
        try:
            from chunking import chunk_home_interior
            chunk_home_interior()
            print("✓ Chunking voltooid\n")
        except Exception as e:
            print(f"✗ Fout bij chunking: {e}")
            return
    else:
        print("✓ Chunking overgeslagen\n")
    
    # Step 2: Create subcategories sheet
    print("STAP 2: Subssubcategorieën sheet maken")
    print("Dit maakt een overzicht van alle unieke subssubcategorieën uit alle datasets.")
    
    if not ask_user("Is de subssubcategorieën sheet al gemaakt?"):
        try:
            from create_subssubcategories_sheet import create_subssubcategories_sheet
            create_subssubcategories_sheet()
            print("✓ Subssubcategorieën sheet aangemaakt\n")
        except Exception as e:
            print(f"✗ Fout bij maken subcategorieën sheet: {e}")
            return
    else:
        print("✓ Subssubcategorieën sheet maken overgeslagen\n")
    
    # Step 3: Clean datasets
    print("STAP 3: Datasets cleanen")
    print("Dit verwijdert onnodige kolommen en filtert producten op basis van criteria.")
    
    if not ask_user("Zijn de datasets al gecleaned?"):
        try:
            from clean_datasets import clean_all_datasets
            clean_all_datasets()
            print("✓ Datasets gecleaned\n")
        except Exception as e:
            print(f"✗ Fout bij cleanen datasets: {e}")
            return
    else:
        print("✓ Dataset cleaning overgeslagen\n")
    
    # Step 4: Merge datasets
    print("STAP 4: Datasets mergen tot compleet bestand")
    print("Dit combineert alle gecleande datasets met de subcategorieën matches.")
    
    if not ask_user("Is het complete bestand al aangemaakt?"):
        try:
            from merge_datasets import merge_all_datasets
            merge_all_datasets()
            print("✓ Compleet bestand aangemaakt\n")
        except Exception as e:
            print(f"✗ Fout bij mergen datasets: {e}")
            return
    else:
        print("✓ Dataset merging overgeslagen\n")
    
    print("=== Pipeline voltooid! ===")
    print("\nResultaten:")
    print("- Gechunkte bestanden in: ./Chunking/")
    print("- Subssubcategorieën sheet in: ./Subssubcategorieën sheet/subssubcategorieën.csv")
    print("- Gecleande datasets in: ./Datasets gecleaned/")
    print("- Compleet bestand in: ./Dataset compleet/bol subcategorieën selectie compleet.csv")

if __name__ == "__main__":
    main()