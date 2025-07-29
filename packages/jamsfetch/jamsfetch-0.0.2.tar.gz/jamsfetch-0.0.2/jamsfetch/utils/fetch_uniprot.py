import os
import requests
import time

def get_uniprot(uniprot_id, outdir="uniprot_fasta"):
    """
    Fetches the original FASTA sequence from UniProt and saves it to a file.

    Args:
        uniprot_id (str): UniProt protein ID (e.g. "P12345")
        outdir (str): Directory to save the FASTA file
    """
    base_url = "https://rest.uniprot.org/uniprotkb/"
    fasta_url = f"{base_url}{uniprot_id}.fasta"
    os.makedirs(outdir, exist_ok=True)

    response = requests.get(fasta_url)

    if response.status_code == 200:
        fasta_path = os.path.join(outdir, f"{uniprot_id}.fasta")
        with open(fasta_path, "w") as f:
            f.write(response.text)
        print(f"Saved: {fasta_path}")
    else:
        print(f"Error downloading FASTA for {uniprot_id}: status {response.status_code}")

def get_uniprot_batch(ids, output_dir="uniprot_fasta", delay=0.5):
    """
    Download multiple FASTA sequences from UniProt and save them to files.

    Args:
        ids (list of str): List of UniProt protein IDs to download.
        output_dir (str): Directory to save the downloaded files.
        delay (float): Number of seconds to wait after each query.

    Returns:
        None
    """
    for uniprot_id in ids:
        get_uniprot(uniprot_id, output_dir)
        time.sleep(delay) 