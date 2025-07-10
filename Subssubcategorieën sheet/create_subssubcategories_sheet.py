import csv
import os
import glob
from collections import defaultdict
import random
from pathlib import Path

def create_subssubcategories_sheet():
    """Create subssubcategories sheet from all datasets"""
    
    # Paths
    script_dir = Path(__file__).parent.parent
    datasets_dir = script_dir / 'Datasets'
    output_dir = Path(__file__).parent
    
    # Dictionary to store data per category and subssubgroup
    category_data = defaultdict(lambda: defaultdict(lambda: {
        'count': 0,
        'example': None
    }))
    
    # Find all CSV files in Datasets folder
    csv_files = list(datasets_dir.glob('*.csv'))
    print(f"Gevonden CSV bestanden: {len(csv_files)}")
    
    # Process each CSV file
    for csv_file in csv_files:
        product_category = csv_file.stem  # filename without extension
        print(f"\nVerwerken van: {csv_file.name}")
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter='|')
                
                row_count = 0
                for row in reader:
                    row_count += 1
                    
                    if row_count % 10000 == 0:
                        print(f"  Verwerkt: {row_count} rijen...", end='\r')
                    
                    try:
                        # Use subssubgroup as required
                        subssubgroup = row.get('Category.subssubgroup', '').strip()
                        
                        if not subssubgroup:
                            continue
                        
                        # Update counter
                        category_data[product_category][subssubgroup]['count'] += 1
                        
                        # Save example product
                        if (category_data[product_category][subssubgroup]['example'] is None or 
                            random.random() < 0.01):  # 1% chance to replace
                            
                            title = row.get('title', '').strip()
                            description = row.get('description', '').strip()
                            url = row.get('productPageUrlNL', '').strip()
                            
                            if title and description and url:
                                category_data[product_category][subssubgroup]['example'] = {
                                    'title': title,
                                    'description': description,
                                    'url': url
                                }
                    
                    except Exception as e:
                        continue
                
                print(f"\n  Aantal subssubgroepen gevonden: {len(category_data[product_category])}")
                print(f"  Totaal verwerkte rijen: {row_count}")
                
        except Exception as e:
            print(f"  Fout bij verwerken bestand {csv_file}: {e}")
            continue
    
    # Write output file
    output_path = output_dir / 'subssubcategorieën.csv'
    print(f"\nAanmaken van subssubcategorieën.csv...")
    
    with open(output_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_ALL)
        
        # Write header matching your format
        writer.writerow([
            'Match',
            'Category.category',
            'Category.subssubgroup',
            'Aantal',
            'Voorbeeld_product_titel',
            'Voorbeeld_product_beschrijving',
            'Voorbeeld_product_link'
        ])
        
        # Write data for each category/subssubgroup combination
        total_rows = 0
        for category, subssubgroups in sorted(category_data.items()):
            for subssubgroup, data in sorted(subssubgroups.items()):
                example = data['example'] or {'title': '', 'description': '', 'url': ''}
                
                writer.writerow([
                    '',  # Empty Match column for manual input
                    category,
                    subssubgroup,
                    data['count'],
                    example['title'],
                    example['description'],
                    example['url']
                ])
                
                total_rows += 1
        
        print(f"\nTotaal aantal rijen geschreven: {total_rows}")
    
    print("\n✓ Subssubcategorieën sheet aangemaakt!")
    
    # Print summary
    print("\nSamenvatting:")
    for category in sorted(category_data.keys()):
        total_products = sum(data['count'] for data in category_data[category].values())
        print(f"  {category}: {len(category_data[category])} subssubgroepen, {total_products:,} producten")