import subprocess

output = subprocess.run(["git", "diff", "--name-status", "master..stg"], capture_output=True)
output_data = output.stdout.decode("utf-8")
output_data_lines = output_data.splitlines()
out_lines_transform = map(lambda val: val.split("\t"), output_data_lines)
print(list(out_lines_transform))`