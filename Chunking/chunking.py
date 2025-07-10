import pandas as pd
import os
import shutil
from pathlib import Path

def chunk_home_interior():
    """Chunk the home-interior.csv file into 4 parts"""
    
    # Paths
    script_dir = Path(__file__).parent.parent
    datasets_dir = script_dir / 'Datasets'
    chunking_dir = script_dir / 'Chunking'
    
    # Source file - check both Datasets and Chunking folder
    source_file = datasets_dir / 'home-interior.csv'
    
    if not source_file.exists():
        # Check if it's in the Chunking folder
        source_file = chunking_dir / 'home-interior.csv'
        if not source_file.exists():
            raise FileNotFoundError(f"home-interior.csv niet gevonden in {datasets_dir} of {chunking_dir}")
    
    print(f"Start chunking van {source_file}...")
    
    # Count total rows
    print("Tellen van rijen...")
    with open(source_file, 'r', encoding='utf-8') as f:
        header = f.readline()
        total_rows = sum(1 for line in f)
    
    print(f"Totaal aantal rijen (excl. header): {total_rows}")
    
    # Calculate rows per chunk
    rows_per_chunk = total_rows // 4 + (1 if total_rows % 4 != 0 else 0)
    print(f"Rijen per chunk: {rows_per_chunk}")
    
    # Read and split the file
    print("Verdelen van bestand...")
    
    chunk_num = 1
    current_chunk_rows = 0
    output_file = None
    
    with open(source_file, 'r', encoding='utf-8') as infile:
        header = infile.readline()
        
        for line_num, line in enumerate(infile, 1):
            # Start new chunk if needed
            if current_chunk_rows == 0:
                if output_file:
                    output_file.close()
                
                # All chunks go to Chunking folder first
                output_path = chunking_dir / f'chunk_{chunk_num}.csv'
                
                print(f"Schrijven naar: {output_path}")
                output_file = open(output_path, 'w', encoding='utf-8')
                output_file.write(header)
            
            output_file.write(line)
            current_chunk_rows += 1
            
            # Check if chunk is complete
            if current_chunk_rows >= rows_per_chunk and chunk_num < 4:
                current_chunk_rows = 0
                chunk_num += 1
            
            # Progress indicator
            if line_num % 100000 == 0:
                print(f"  Verwerkt: {line_num:,} rijen...", end='\r')
        
        if output_file:
            output_file.close()
    
    # Move original file to Chunking folder
    print("\nVerplaatsen origineel bestand naar Chunking folder...")
    original_backup = chunking_dir / 'home-interior_original.csv'
    shutil.move(str(source_file), str(original_backup))
    
    # Copy chunk_1 back to Datasets as home-interior.csv
    chunk1_path = chunking_dir / 'chunk_1.csv'
    if chunk1_path.exists():
        shutil.copy(str(chunk1_path), str(datasets_dir / 'home-interior.csv'))
    
    print("✓ Chunking voltooid!")
    print(f"  - Chunk 1 staat nu in Datasets/home-interior.csv")
    print(f"  - Chunks 2-4 staan in Chunking/")
    print(f"  - Origineel bestand staat in Chunking/home-interior_original.csv")