import pandas as pd
import os
from pathlib import Path

def normalize_match_value(match_value):
    """Normalize match value: remove spaces, convert to lowercase"""
    if pd.isna(match_value) or match_value == '':
        return None
    return str(match_value).lower().replace(' ', '').replace('&', '').strip()

def merge_all_datasets():
    """Merge all cleaned datasets with subssubcategories matches"""
    
    # Paths
    script_dir = Path(__file__).parent.parent
    cleaned_dir = script_dir / 'Datasets gecleaned'
    subcategories_file = script_dir / 'Subssubcategorieën sheet' / 'subssubcategorieën.csv'
    output_dir = Path(__file__).parent
    output_file = output_dir / 'bol subcategorieën selectie compleet.csv'
    
    print("Start mergen van datasets...")
    
    # Load subcategories with matches
    print("Laden subssubcategorieën sheet...")
    try:
        subcategories_df = pd.read_csv(subcategories_file, delimiter=',')
        
        # Normalize Match values first
        subcategories_df['Match_normalized'] = subcategories_df['Match'].apply(normalize_match_value)
        
        # Filter only rows with non-empty Match values
        matches_df = subcategories_df[subcategories_df['Match_normalized'].notna()]
        
        # Create lookup dictionary: category_subssubgroup -> normalized_match
        match_dict = {}
        for _, row in matches_df.iterrows():
            # Use lowercase for case-insensitive matching
            key = f"{row['Category.category'].lower()}_{row['Category.subssubgroup'].lower()}"
            match_dict[key] = row['Match_normalized']
        
        print(f"  Gevonden: {len(match_dict)} matches")
        
    except Exception as e:
        print(f"✗ Fout bij laden subssubcategorieën sheet: {e}")
        return
    
    # Process all cleaned datasets
    csv_files = list(cleaned_dir.glob('*.csv'))
    print(f"\nVerwerken van {len(csv_files)} gecleande datasets...")
    
    first_file = True
    total_rows = 0
    matched_categories = set()
    
    for csv_file in csv_files:
        product_category = csv_file.stem.lower()  # Use lowercase for matching
        print(f"\n  Verwerken: {csv_file.name}")
        
        try:
            rows_added = 0
            
            # Process in chunks
            for chunk in pd.read_csv(csv_file, delimiter='|', chunksize=50000, low_memory=False):
                # Create match key using category and subssubgroup
                chunk['match_key'] = (product_category + '_' + 
                                     chunk['Category.subssubgroup'].astype(str).str.lower())
                
                # Add Match column (normalized match values)
                chunk['Match'] = chunk['match_key'].map(match_dict)
                
                # Keep only rows with matches AND where both category and subssubgroup exist
                matched_chunk = chunk[chunk['Match'].notna() & chunk['match_key'].isin(match_dict.keys())]
                
                if not matched_chunk.empty:
                    # Track which categories had matches
                    matched_categories.update(matched_chunk['match_key'].unique())
                    
                    # Drop the temporary match_key column
                    matched_chunk = matched_chunk.drop('match_key', axis=1)
                    
                    if first_file:
                        matched_chunk.to_csv(output_file, index=False, sep=',')
                        first_file = False
                    else:
                        matched_chunk.to_csv(output_file, mode='a', header=False, index=False, sep=',')
                    
                    rows_added += len(matched_chunk)
            
            print(f"    ✓ Toegevoegd: {rows_added:,} rijen")
            total_rows += rows_added
            
        except Exception as e:
            print(f"    ✗ Fout: {e}")
    
    print(f"\n✓ Merging voltooid!")
    print(f"  Totaal aantal rijen in compleet bestand: {total_rows:,}")
    print(f"  Aantal unieke subssubcategorieën gematched: {len(matched_categories)}")
    
    # Show some statistics
    total_possible_matches = len(match_dict)
    print(f"  Mogelijke matches in subssubcategorieën sheet: {total_possible_matches}")
    print(f"  Daadwerkelijk gevonden matches: {len(matched_categories)}")
    if total_possible_matches > 0:
        match_percentage = (len(matched_categories) / total_possible_matches) * 100
        print(f"  Match percentage: {match_percentage:.1f}%")