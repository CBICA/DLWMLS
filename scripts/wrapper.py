# This wrapper script takes two output dirs (--out_csv, --out_seg), calls the installed DLWMLS and applies post-processing to extract vols

import argparse
import os
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--in_dir", help="Provide the path to the input FL MRI images.", required=True)
parser.add_argument("--out_seg", help="Provide the path to the output dir for white matter lesion segmentations.", required=True)
parser.add_argument("--out_csv", help="Provide the path to the output lesion volume CSV file.", required=True)
parser.add_argument("-device", help="cuda, cpu or mps", required=True, default="cuda")
args, unknown_args = parser.parse_args()

def validate_and_setup():
    """Validate inputs and create output directories if needed."""
    errors = []
    
    # Convert to Path objects for easier handling
    in_dir = Path(args.in_dir)
    out_seg_dir = Path(args.out_seg)
    out_csv_path = Path(args.out_csv)
    
    # Check input directory exists
    if not in_dir.exists():
        errors.append(f"Input directory does not exist: {in_dir}")
    elif not in_dir.is_dir():
        errors.append(f"Input path is not a directory: {in_dir}")
    
    # Check if input directory is empty (optional check)
    if in_dir.exists() and in_dir.is_dir():
        if not any(in_dir.iterdir()):
            errors.append(f"Input directory is empty: {in_dir}")
    
    # Create output segmentation directory if it doesn't exist
    try:
        out_seg_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output segmentation directory ready: {out_seg_dir}")
    except PermissionError:
        errors.append(f"Permission denied creating output directory: {out_seg_dir}")
    except OSError as e:
        errors.append(f"Error creating output directory {out_seg_dir}: {e}")
    
    # Check output CSV path
    out_csv_parent = out_csv_path.parent
    
    # Create parent directory for CSV if it doesn't exist
    try:
        out_csv_parent.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        errors.append(f"Permission denied creating directory for CSV: {out_csv_parent}")
    except OSError as e:
        errors.append(f"Error creating directory for CSV {out_csv_parent}: {e}")
    
    # Check if CSV file already exists (warn but don't error)
    if out_csv_path.exists():
        print(f"Warning: Output CSV file already exists and will be overwritten: {out_csv_path}")
    
    # Check write permissions for CSV location
    if out_csv_parent.exists() and not os.access(out_csv_parent, os.W_OK):
        errors.append(f"No write permission for CSV output directory: {out_csv_parent}")
    
    # If there are errors, print them and exit
    if errors:
        print("Validation errors found:")
        for error in errors:
            print(f"  ERROR: {error}")
        sys.exit(1)
    
    print("All validation checks passed!")
    return in_dir, out_seg_dir, out_csv_path

def format_unknown_args(unknown_args):
    """Format unknown arguments for passing to another command line tool."""
    if not unknown_args:
        return []
    
    # Print info about unknown args
    print(f"Unknown arguments to pass through: {' '.join(unknown_args)}")
    
    # Return as-is - they're already properly formatted for command line use
    return unknown_args

# Run validation and setup
in_dir, out_seg_dir, out_csv_path = validate_and_setup()

passthrough_args = format_unknown_args(unknown_args)

# Your main code continues here...
print(f"Processing MRI images from: {in_dir}")
print(f"Segmentations will be saved to: {out_seg_dir}")
print(f"Results CSV will be saved to: {out_csv_path}")
print(f"Using device {args.device}")

dlwmls_cmd = f"DLWMLS -i { in_dir } -o { out_seg_dir } -device { args.device } { ' '.join(passthrough_args) }"
dlwmls_return_code = os.system(dlwmls_cmd)
if dlwmls_return_code > 0:
    print(f"DLWMLS failed with non-zero exit code {dlwmls_return_code}.")
    sys.exit(dlwmls_return_code)

post_cmd = f"/usr/bin/python3 /app/scripts/wmls_post.py --in_dir { out_seg_dir } --in_suff _FL_WMLS.nii.gz --out_csv { out_csv_path }"
post_return_code = os.system(post_cmd)
if post_return_code > 0:
    print(f"DLWMLS post-process volume extraction failed with non-zero exit code {post_return_code}.")
    sys.exit(post_return_code)


