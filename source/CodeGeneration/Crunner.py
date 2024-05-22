import subprocess

# Compile the C file (adjust compiler path and flags as needed)
subprocess.run(['gcc', '-o', 'output', 'output.c'])

# Execute the program
process = subprocess.run(['./output.c'], capture_output=True)

# Check exit status and capture output (if needed)
# ... (as in previous example)

