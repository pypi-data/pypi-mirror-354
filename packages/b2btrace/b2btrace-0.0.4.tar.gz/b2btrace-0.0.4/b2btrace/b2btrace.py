import subprocess
import shlex
import pandas as pd
import numpy as np
import re
import os



# --- DNA Sequence Manipulation Functions ---
def complement_base(base):
    """Returns the complement of a single DNA base, handles 'X' and 'N'."""
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C',
                      'a': 't', 't': 'a', 'c': 'g', 'g': 'c','N': 'N', 'n': 'n'}
    return complement_map.get(base, base) # Return base itself if not in map

def transform_pattern(pattern, transformation_type):
    """
    Transforms a DNA pattern containing 'X' (wildcard) for reverse, complement, etc.
    'X' is treated as a literal 'X' during transformation.
    """
    transformed_pattern = ""
    if transformation_type == "reverse":
        transformed_pattern = pattern[::-1]
    elif transformation_type == "complement":
        # Complement of the pattern as-is (X remains X)
        transformed_pattern = "".join([complement_base(b) for b in pattern])
    elif transformation_type == "reverse_complement":
        # Reverse complement of the pattern (X remains X)
        transformed_pattern = "".join([complement_base(b) for b in reversed(pattern)])
    else: # "forward"
        transformed_pattern = pattern
    return transformed_pattern

# Function to convert ASCII quality score to Phred score
def phred_to_score(char):
    """Converts an ASCII quality character to its Phred score."""
    return ord(char) - 33 # Phred+33 encoding


def create_regex_pattern(target_pattern):
    raw_search_patterns_with_x = {
        "forward": transform_pattern(target_pattern, "forward"),
        "reverse": transform_pattern(target_pattern, "reverse"),
        "complement": transform_pattern(target_pattern, "complement"),
        "reverse_complement": transform_pattern(target_pattern, "reverse_complement")
    }

    #if either has *. change to .*
    for key in raw_search_patterns_with_x:
        if "*." in raw_search_patterns_with_x[key]:
            print(f"Replacing '*.' with '.*' in pattern for {key}")
            raw_search_patterns_with_x[key] = raw_search_patterns_with_x[key].replace("*.", ".*")


    # Combine all patterns for the main AWK regex
    regex_for_awk = '|'.join(raw_search_patterns_with_x.values())

    awk_python_regex_patterns = {
        "forward": raw_search_patterns_with_x["forward"],
        "reverse": raw_search_patterns_with_x["reverse"],
        "complement": raw_search_patterns_with_x["complement"],
        "reverse_complement": raw_search_patterns_with_x["reverse_complement"]
    }
    
    
    return regex_for_awk, awk_python_regex_patterns




def awk_template(regex_for_awk):
    # --- Build the AWK Script ---
    # The AWK script will filter and print the same fields as before.
    # The heavy lifting of finding the exact matched substring and qualities will be in Python.
    awk_script_template = """
    BEGIN {{ OFS="\\t" }} # Set output field separator to tab
    $10 ~ /{regex_for_awk}/ {{
        umi = "N/A";
        cb = "N/A";

        # Extract UMI and Cell Barcode
        for (i=12; i<=NF; i++) {{
            if ($i ~ /^UB:Z:/) {{
                umi = substr($i, 6);
            }} else if ($i ~ /^CB:Z:/) {{
                cb = substr($i, 6);
            }}
        }}

        # No need to determine matched_pattern_type in AWK anymore, Python will do it.
        # Print relevant fields
        if (umi != "N/A" && cb != "N/A") {{ # Only print if both UMI and CB found
            print cb, umi, $10, $11, $6; # CB, UMI, Aligned_Seq, Qual_Scores, CIGAR
        }}
    }}
    """
    return awk_script_template.format(regex_for_awk=regex_for_awk)

def validate_inputs(region_start, region_end, bam_path):
    """Validate all inputs before processing"""
    if not os.path.exists(bam_path):
        raise FileNotFoundError(f"BAM file not found: {bam_path}")
    
    if region_start >= region_end:
        raise ValueError("region_start must be less than region_end")
    
def check_samtools():
    """Check if samtools is installed and accessible."""
    try:
        result = subprocess.run(["samtools", "--version"], 
                              capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            raise RuntimeError("samtools not found or not working")
        return True
    except FileNotFoundError:
        raise RuntimeError(
            "samtools is required but not found. "
            "Please install samtools: https://www.htslib.org/download/"
        )
    except UnicodeDecodeError:
        # If there's still a Unicode error, try without text mode
        try:
            result = subprocess.run(["samtools", "--version"], 
                                  capture_output=True)
            if result.returncode != 0:
                raise RuntimeError("samtools not found or not working")
            return True
        except Exception:
            raise RuntimeError("samtools check failed due to encoding issues")
    

def run_search(chromosome, region_start, region_end, bam_path,awk_script):

    validate_inputs(region_start, region_end, bam_path)
    # --- Construct and Execute Command ---
    region = f"{chromosome}:{region_start}-{region_end}"

    # Use shlex.quote to safely quote the paths and script
    bam_path_quoted = shlex.quote(bam_path)
    region_quoted = shlex.quote(region)
    awk_script_quoted = shlex.quote(awk_script)

    check_samtools()

    # The command string
    command = f"samtools view {bam_path_quoted} {region_quoted} | awk {awk_script_quoted}"

    print(f"Executing command:\n{command}\n")

    result = subprocess.run(["bash", "-c", command], capture_output=True, text=True)

    # --- Process Output ---
    if result.returncode != 0:
        print("Error executing command:")
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
        raise RuntimeError(f"Command failed with exit code {result.returncode}")
    return result



def create_results_df(result, awk_python_regex_patterns):

    # Parse the output into a DataFrame
    output_lines = result.stdout.strip().split('\n')
    if not output_lines or output_lines == ['']:
        print("No matching reads found.")
        df = pd.DataFrame(columns=["Barcode", "UMI", "Aligned_Seq", "Quality_Scores", "CIGAR",
                                "Matched_Subsequence", "Matched_Subsequence_Quals", "Avg_Phred_Score", "Matched_Pattern_Type"])
    else:
        data = []
        for line in output_lines:
            parts = line.split('\t')
            if len(parts) == 5: # Now expecting 5 parts from AWK: CB, UMI, Aligned_Seq, Qual_Scores, CIGAR
                data.append(parts)
            else:
                print(f"Warning: Skipping malformed line from awk output (expected 5 fields, got {len(parts)}): {line}")

        if data:
            df = pd.DataFrame(data, columns=["Barcode", "UMI", "Aligned_Seq", "Quality_Scores", "CIGAR"])
        else:
            print("No valid data parsed from output.")
            df = pd.DataFrame(columns=["Barcode", "UMI", "Aligned_Seq", "Quality_Scores", "CIGAR",
                                    "Matched_Subsequence", "Matched_Subsequence_Quals", "Avg_Phred_Score", "Matched_Pattern_Type"])

    # --- Post-processing in Python to extract matched subsequence and calculate quality scores ---
    if not df.empty:
        print("\n---Post-processing DataFrame---")
        matched_subsequences = []
        matched_subsequence_quals = []
        avg_phred_scores = []
        matched_pattern_types = [] # Re-introducing this as a derived column
        query_subsequences = []
        query_subsequence_quals = []
        avg_query_phred_scores = []

        # Compile the regexes for efficient matching in Python

        compiled_patterns = {
            key: re.compile(regex_str) for key, regex_str in awk_python_regex_patterns.items()
        }
        
        forward = awk_python_regex_patterns["forward"]
        wildcard_presence = "." in forward
        print(f"Wildcard presence in patterns: {wildcard_presence}")
        
        for index, row in df.iterrows():
            aligned_seq = row['Aligned_Seq']
            qual_scores = row['Quality_Scores']
            
            found_match = False
            # Iterate through the patterns in a defined order if there's a preference (e.g., forward first)
            # Or simply iterate through the compiled_patterns dictionary (order not guaranteed, but one match is enough)
            for pattern_type, regex_obj in compiled_patterns.items():
                match = regex_obj.search(aligned_seq)
                if ".*" in forward:
                    n_chars_begin = len(regex_obj.pattern.split('.*')[0])
                    n_chars_end = len(regex_obj.pattern.split('.*')[-1])
                elif "." in forward:
                    n_chars_begin = len(regex_obj.pattern.split('.')[0])
                    n_chars_end = len(regex_obj.pattern.split('.')[-1])

                if match:
                    matched_seq = match.group(0) # The exact matched substring
                    start, end = match.span()
                    matched_qual = qual_scores[start:end] # Corresponding quality scores

                    if wildcard_presence:
                        
                        query_seq = matched_seq[n_chars_begin:len(matched_seq)-n_chars_end]
                        query_qual = matched_qual[n_chars_begin:len(matched_qual)-n_chars_end]
                        avg_query_phred_score = sum([phred_to_score(q) for q in query_qual]) / len(query_qual) if query_qual else 0

                    
                    # Calculate average Phred score
                    phred_scores = [phred_to_score(q) for q in matched_qual]
                    avg_phred = sum(phred_scores) / len(phred_scores) if phred_scores else 0
                    
                    matched_subsequences.append(matched_seq)
                    matched_subsequence_quals.append(matched_qual)
                    avg_phred_scores.append(f"{avg_phred:.2f}") # Format to 2 decimal places
                    matched_pattern_types.append(pattern_type)
                    if wildcard_presence:
                        query_subsequences.append(query_seq)
                        query_subsequence_quals.append(query_qual)
                        avg_query_phred_scores.append(f"{avg_query_phred_score:.2f}")


                    found_match = True
                    break # Stop after finding the first match for this row
            
            if not found_match:
                # This should ideally not happen if awk correctly filtered, but good for robustness
                matched_subsequences.append(None)
                matched_subsequence_quals.append(None)
                avg_phred_scores.append(None)
                matched_pattern_types.append(None)
                if wildcard_presence:
                    query_subsequences.append(None)
                    query_subsequence_quals.append(None)
                    avg_query_phred_scores.append(None)

        df['Matched_Subsequence'] = matched_subsequences
        df['Matched_Subsequence_Quals'] = matched_subsequence_quals
        df['Avg_Phred_Score'] = avg_phred_scores
        df['Matched_Pattern_Type'] = matched_pattern_types # Add back the pattern type
        if wildcard_presence:
            df['Query_Subsequence'] = query_subsequences
            df['Query_Subsequence_Quals'] = query_subsequence_quals
            df['Avg_Query_Phred_Score'] = avg_query_phred_scores

    print("\n--- Results DataFrame ---")
    print(df.head())
    print(f"\nTotal matching reads found: {len(df)}")
    print(f"Unique UMIs found: {df['UMI'].nunique()} (Note: This is unique within the filtered results, not necessarily after full deduplication across the genome)")
    return df



def umi_collapse(df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapses DataFrame rows based on UMI, applying specific selection criteria
    related to Query_Subsequence.

    Args:
        df: A pandas DataFrame expected to contain 'Barcode', 'UMI',
            'Avg_Phred_Score', 'Query_Subsequence', and 'Avg_Query_Phred_Score' columns.

    Returns:
        A new DataFrame with unique (Barcode, UMI) pairs, selected according to the rules.
    """

    if df.empty:
        print("Input DataFrame is empty. Returning empty DataFrame.")
        return pd.DataFrame(columns=df.columns)
    
    

    # Ensure relevant columns are numeric for comparison.
    # 'errors='coerce'' will turn non-numeric values (like None from failed extractions) into NaN.
    df['Avg_Phred_Score_Numeric'] = pd.to_numeric(df['Avg_Phred_Score'], errors='coerce')

    # Check if 'Query_Subsequence' column exists and has at least one non-null value.
    # This determines which collapse logic to use.
    has_query_subsequence_data = 'Query_Subsequence' in df.columns and \
                                 df['Query_Subsequence'].dropna().empty is False
    
    if has_query_subsequence_data:
        #remove all rows where 'Query_Subsequence' is None or NaN
        df = df[df['Query_Subsequence'].notna()]
    elif 'Matched_Subsequence' in df.columns:
        df = df[df['Matched_Subsequence'].notna()]


    if has_query_subsequence_data:
        df['Avg_Query_Phred_Score_Numeric'] = pd.to_numeric(df['Avg_Query_Phred_Score'], errors='coerce')

    collapsed_rows = []

    # Group by Barcode and UMI. These two fields together define a unique molecule.
    for (barcode, umi), group_df in df.groupby(['Barcode', 'UMI']):
        # Determine if this specific group has valid Query_Subsequence data
        sequence_column = 'Query_Subsequence' if has_query_subsequence_data else 'Matched_Subsequence'

        query_seq_counts = group_df[sequence_column].value_counts()

        max_count = query_seq_counts.max()
        most_common_query_seqs = query_seq_counts[query_seq_counts == max_count].index.tolist()

        if len(most_common_query_seqs) == 1:
            chosen_query_seq = most_common_query_seqs[0]
            filtered_by_query_seq = group_df[group_df[sequence_column] == chosen_query_seq]
            selected_row = filtered_by_query_seq.loc[filtered_by_query_seq['Avg_Query_Phred_Score_Numeric'].idxmax()]
        else:
            tied_query_seqs_df = group_df[group_df[sequence_column].isin(most_common_query_seqs)]
            selected_row = tied_query_seqs_df.loc[tied_query_seqs_df['Avg_Query_Phred_Score_Numeric'].idxmax()]
        # Append the selected row to our list.
        collapsed_rows.append(selected_row)

    if not collapsed_rows:
        print("No rows left after collapsing. Returning empty DataFrame.")
        # Return a DataFrame with original columns to maintain structure.
        return pd.DataFrame(columns=df.columns)

    # Create the final collapsed DataFrame and drop temporary numeric columns.
    collapsed_df = pd.DataFrame(collapsed_rows).reset_index(drop=True)
    collapsed_df = collapsed_df.drop(columns=['Avg_Phred_Score_Numeric'], errors='ignore')
    if has_query_subsequence_data:
        collapsed_df = collapsed_df.drop(columns=['Avg_Query_Phred_Score_Numeric'], errors='ignore')

    alleles = collapsed_df[sequence_column].unique()
    print(f"Unique alleles after collapsing: {len(alleles)}")
    print(f"Alleles: {alleles}")
    
    return collapsed_df, alleles



def assign_genotype_to_umi(df, wt=None, mut=None, query_subsequence=False):
    
    seq_column = 'Query_Subsequence' if query_subsequence else 'Matched_Subsequence'

    if mut is not None:
        df = df[df[seq_column].isin([wt, mut])]
    
    genotypes = []
    if wt is not None:
        for i in range(len(df)):
            sequence = df.iloc[i][seq_column]
            if sequence == wt:
                genotypes.append(f'WT-{sequence}')
            else:
                genotypes.append(f'MUT-{sequence}')
            # Genotype is WT if either the Query_Subsequence or Matched_Subsequence matches the WT sequence
    else:
        for i in range(len(df)):
            sequence = df.iloc[i][seq_column]
            genotypes.append(f'{sequence}')
    
    df['Genotype'] = genotypes

    return df

def assign_genotype_to_barcode(df):
    #only do this if Genotype is not all "Unclear"
    if 'Genotype' not in df.columns or df['Genotype'].isnull().all() or df['Genotype'].nunique() == 1:
        df = df.groupby("Barcode").first().reset_index()
        print("No Genotype information available. Returning DataFrame without Het_Hom assignment.")
        return df

    df['Het_Hom'] = 'Unclear'  # Default value
    df["more_than_2_genotypes"] = df.groupby("Barcode")["Genotype"].transform(lambda x: len(x.unique()) > 2)

    unique_genotypes = df['Genotype'].unique()
    for genotype in unique_genotypes:
        df[f'n_{genotype}'] = df.groupby("Barcode")["Genotype"].transform(lambda x: (x == genotype).sum())
    
    #count total rows for each Barcode
    df["n_total"] = df.groupby("Barcode").transform('size')
    
    #for each Barcode, find how many genotypes are present, if more than 2, find two most common
    for barcode in df['Barcode'].unique():
        genotype_counts = df[df['Barcode'] == barcode]['Genotype'].value_counts()
        if len(genotype_counts) > 2:
            # More than two genotypes, find the two most common
            most_common = genotype_counts.nlargest(2)
            #sort alphabetically
            most_common = most_common.sort_index()
            df.loc[df['Barcode'] == barcode, 'Het_Hom'] = f'Het ({most_common.index[0]}, {most_common.index[1]})'
        elif len(genotype_counts) == 2:
            # Exactly two genotypes
            genotype_counts = genotype_counts.sort_index()
            df.loc[df['Barcode'] == barcode, 'Het_Hom'] = f'Het ({genotype_counts.index[0]}, {genotype_counts.index[1]})'
        elif len(genotype_counts) == 1:
            # Only one genotype
            #if count is > 3
            if genotype_counts.iloc[0] > 3:
                df.loc[df['Barcode'] == barcode, 'Het_Hom'] = f'Hom ({genotype_counts.index[0]})'
            else:
                df.loc[df['Barcode'] == barcode, 'Het_Hom'] = f'Potential Hom ({genotype_counts.index[0]})'

    #make final df collapsed by Barcode and remove UMI col
    df = df.drop(columns=["UMI"])
    df = df.groupby("Barcode").first().reset_index()
    return df



def calc_genotype_frequencies(adata, inplace=True):
    """
    Calculate allele frequencies for each Barcode in the DataFrame.
    Assumes 'Genotype' column exists with values 'WT', 'MUT', or 'Unclear'.
    """
    if 'Het_Hom' not in adata.obs.columns or adata.obs['Het_Hom'].isnull().all():
        print("No Het_Hom information available. Doing nothing.")
        return adata if not inplace else None
    df = adata.obs.copy()
    frequencies = df["Het_Hom"].value_counts(normalize=True).to_dict()
    
    if inplace:
        adata.uns["allele_frequency"] = frequencies
    elif not inplace:
        new_adata = adata.copy()
        new_adata.uns["allele_frequency"] = frequencies
        return new_adata
    


# add to adata
def add_to_adata(adata, df,inplace=True):
    if not inplace:
        adata = adata.copy()
        obs = adata.obs.copy()
        #if barcode not in, make from index
        if 'Barcode' not in obs.columns:
            obs['Barcode'] = obs.index
        merged_obs = obs.merge(df, left_on="Barcode", right_on='Barcode', how='left')
        new_adata = adata.copy()
        new_adata.obs = merged_obs
        return new_adata
    else:
        obs = adata.obs.copy()
        if 'Barcode' not in obs.columns:
            obs['Barcode'] = obs.index
        merged_obs = obs.merge(df, left_on="Barcode", right_on='Barcode', how='left')
        adata.obs = merged_obs



def run_workflow(region_start, region_end, chromosome, bam_path, wt="A", mut=None, target_pattern="TTTTATC.*ATGATG",adata=None):

    regex_for_awk,awk_python_regex_patterns = create_regex_pattern(target_pattern=target_pattern)
    awk_script = awk_template(regex_for_awk)
    result = run_search(chromosome, region_start, region_end, bam_path,awk_script)
    df = create_results_df(result, awk_python_regex_patterns = awk_python_regex_patterns)
    df, alleles = umi_collapse(df)
    query_subsequence = 'Query_Subsequence' in df.columns and df['Query_Subsequence'].notna().any()
    collapsed_df = assign_genotype_to_umi(df, wt=wt, mut=mut, query_subsequence=query_subsequence)
    barcodes_geno_df = assign_genotype_to_barcode(collapsed_df)

    if adata is not None:
        add_to_adata(adata, barcodes_geno_df, inplace=True)
        calc_genotype_frequencies(adata, inplace=True)


    return collapsed_df, barcodes_geno_df, alleles




