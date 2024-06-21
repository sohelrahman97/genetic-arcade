import csv, math
from matplotlib import pyplot as plt

def results_plot():
    # Input and output file paths
    input_file_path = 'fitness_history.csv'
    output_file_path = 'output.csv'

    # Declare local lists for holding x and y values
    x = []
    y1 = []
    y2 = []
    curr_y = 0


    # Read the input file and write to the output file
    with open(input_file_path, 'r', newline='') as infile, open(output_file_path, 'w', newline='') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        for row in csv_reader:
            if row:  # Check if the row is not empty
                # Split the single column into two values
                values = row[0].split()
                if len(values) == 2:  # Ensure there are exactly two values
                    # Convert values to floats, round them, and convert to integers
                    rounded_values = [str(round(float(value))) for value in values]
                    csv_writer.writerow(rounded_values)
                    x.append(curr_y)
                    curr_y += 1
                    y1. append(int(rounded_values[0]))
                    y2.append(int(rounded_values[1]))

    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.title("Simulation Results")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(["Maximum", "Average"])
    plt.show()

# Enable it to run standalone
if __name__ == '__main__':
    results_plot()