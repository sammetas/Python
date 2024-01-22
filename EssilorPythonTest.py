import os
from datetime import datetime

class Output4:
    def __init__(self, nom=0.0, avg=0.0):
        self.nom = nom
        self.avg = avg
    def __str__(self):
        return f'nom: {self.nom}, avg: {self.avg}'

def calculate_log_duration(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        start_time = datetime.strptime(lines[0][:8], '%H:%M:%S')
        end_time = datetime.strptime(lines[-1][:8], '%H:%M:%S')
        duration_in_seconds = (end_time - start_time).total_seconds()
        return int(duration_in_seconds)

def write_numbers(file_path):
    step_numbers = {}
    with open(file_path, 'r') as file:
        for line in file:
            if "Start Step No" in line:
                line_parts = line.split()
                if len(line_parts) == 17:
                    step_number = int(line_parts[5])
                    key = f"Step No. {line_parts[5]} {line_parts[6]} {line_parts[7]}"
                    value = line_parts[11].strip()
                    step_numbers[key] = value
    return step_numbers

def find_process_step_times(file_path):
    sum_times = 0
    is_it_2_or_3 = False
    with open(file_path, 'r') as file:
        for line in file:
            if "Start Step No. 2" in line or "Start Step No. 3" in line:
                is_it_2_or_3 = True
            elif is_it_2_or_3 and "Process Step Time" in line:
                line_parts = line.split()
                sum_times += int(line_parts[7].strip())
                is_it_2_or_3 = False
    return sum_times

def find_nom_and_avg(file_path, step_no):
    is_step_satisfied = False
    output4 = Output4()
    with open(file_path, 'r') as file:
        for line in file:
            if step_no in line:
                is_step_satisfied = True
            elif is_step_satisfied and "XTAL Thickness" in line:
                line_parts = line.split()
                if len(line_parts) == 10 and line_parts[6] == "Nom.:" and line_parts[8] == "Act.:":
                    output4.nom = float(line_parts[7].strip())
                    output4.avg = float(line_parts[9].strip())
    return output4

def search_in_file(file_path, search_term):
    with open(file_path, 'r') as file:
        return sum(1 for line in file if search_term in line)

# Main
file_path = "/Users/samm/Downloads/prod001.log"
search_term = "F1 - Gas 1 ready"
print(search_in_file(file_path, search_term))

output = find_nom_and_avg(file_path, "Start Step No. 4")
print(output)

print(find_process_step_times(file_path))
print(write_numbers(file_path))
print(calculate_log_duration(file_path))
