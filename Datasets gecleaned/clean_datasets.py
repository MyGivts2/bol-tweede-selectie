import pandas as pd
import os
import gc
from pathlib import Path

# Columns to keep
COLUMNS_TO_KEEP = [
    "productId",
    "ean",
    "title",
    "productPageUrlNL",
    "imageUrl",
    "description",
    "OfferNL.sellingPrice",
    "OfferNL.condition",
    "OfferNL.isDeliverable",
    "OfferNL.maximalDeliveryDays",
    "Category.category",
    "Category.productgroup",
    "Category.subgroup",
    "Category.subssubgroup"
]

def clean_single_dataset(input_path, output_path):
    """Clean a single dataset file"""
    print(f"  Verwerken: {input_path.name}")
    
    try:
        # Process in chunks for memory efficiency
        chunk_size = 10000
        first_chunk = True
        total_rows_kept = 0
        
        for chunk in pd.read_csv(input_path, delimiter='|', chunksize=chunk_size, low_memory=False):
            # Keep only specified columns that exist
            cols_to_keep = [col for col in COLUMNS_TO_KEEP if col in chunk.columns]
            chunk = chunk[cols_to_keep]
            
            # Convert columns for filtering
            chunk['OfferNL.maximalDeliveryDays'] = pd.to_numeric(chunk['OfferNL.maximalDeliveryDays'], errors='coerce')
            chunk['OfferNL.sellingPrice'] = pd.to_numeric(chunk['OfferNL.sellingPrice'], errors='coerce')
            
            # Apply filters
            mask = (
                (chunk['OfferNL.maximalDeliveryDays'] <= 2) &
                (chunk['OfferNL.condition'] == 'new') &
                (chunk['OfferNL.isDeliverable'] == 'Y') &
                (chunk['OfferNL.sellingPrice'] >= 10) &
                (chunk['OfferNL.sellingPrice'] <= 250)
            )
            
            filtered_chunk = chunk[mask]
            
            # Free memory
            del chunk
            
            if not filtered_chunk.empty:
                if first_chunk:
                    filtered_chunk.to_csv(output_path, index=False, sep='|')
                    first_chunk = False
                else:
                    filtered_chunk.to_csv(output_path, mode='a', header=False, index=False, sep='|')
                
                total_rows_kept += len(filtered_chunk)
            
            # Free memory
            del filtered_chunk
            
            # Force garbage collection every 10 chunks
            if total_rows_kept % 100000 == 0:
                gc.collect()
        
        print(f"    ✓ Behouden: {total_rows_kept:,} rijen")
        return True
        
    except Exception as e:
        print(f"    ✗ Fout: {e}")
        return False

def clean_all_datasets():
    """Clean all datasets in the Datasets folder"""
    
    # Paths
    script_dir = Path(__file__).parent.parent
    input_dir = script_dir / 'Datasets'
    output_dir = Path(__file__).parent
    
    # Get all CSV files
    csv_files = list(input_dir.glob('*.csv'))
    print(f"Start cleaning van {len(csv_files)} datasets...\n")
    
    successful = 0
    failed = 0
    
    for csv_file in csv_files:
        output_file = output_dir / csv_file.name
        
        if clean_single_dataset(csv_file, output_file):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✓ Cleaning voltooid!")
    print(f"  - Succesvol: {successful} bestanden")
    print(f"  - Mislukt: {failed} bestanden")