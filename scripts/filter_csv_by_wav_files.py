import pandas as pd
import os
from pathlib import Path

def filter_csv_by_wav_files():
    """
    Filter track_reference.csv to keep only records where the corresponding
    WAV file exists in the rec folder.
    
    Files are named as: musicbrainz_id + ".wav"
    """
    # Read the CSV file
    print("Reading track_reference.csv...")
    df = pd.read_csv('track_reference.csv')
    print(f"Original CSV has {len(df)} records")
    
    # Get the rec folder path
    rec_folder = Path('rec')
    
    # Get all WAV files in the rec folder
    print("Scanning rec folder for WAV files...")
    wav_files = set()
    for wav_file in rec_folder.glob('*.wav'):
        wav_files.add(wav_file.name)
    
    print(f"Found {len(wav_files)} WAV files in rec folder")
    
    # Filter the dataframe to keep only rows where the musicbrainz_id + ".wav" exists
    print("Filtering CSV records...")
    df_filtered = df[df['musicbrainz_id'].apply(lambda x: f"{x}.wav" in wav_files)]
    
    print(f"Filtered CSV has {len(df_filtered)} records")
    print(f"Removed {len(df) - len(df_filtered)} records that don't have corresponding WAV files")
    
    # Save the filtered CSV
    output_file = 'track_reference_filtered.csv'
    df_filtered.to_csv(output_file, index=False)
    print(f"\nFiltered CSV saved to: {output_file}")
    
    # Show some statistics
    print("\n=== Summary ===")
    print(f"Original records: {len(df)}")
    print(f"WAV files in rec folder: {len(wav_files)}")
    print(f"Filtered records: {len(df_filtered)}")
    print(f"Records removed: {len(df) - len(df_filtered)}")
    
    # Find records in CSV that don't have WAV files
    missing_wav = df[~df['musicbrainz_id'].apply(lambda x: f"{x}.wav" in wav_files)]
    if len(missing_wav) > 0:
        print(f"\nFirst 10 records missing WAV files:")
        print(missing_wav[['musicbrainz_id', 'title', 'artist']].head(10).to_string())
    
    # Find WAV files that don't have CSV records
    csv_ids = set(df['musicbrainz_id'].apply(lambda x: f"{x}.wav"))
    extra_wav = wav_files - csv_ids
    if len(extra_wav) > 0:
        print(f"\nFound {len(extra_wav)} WAV files without CSV records:")
        print(list(extra_wav)[:10])

if __name__ == "__main__":
    filter_csv_by_wav_files()

