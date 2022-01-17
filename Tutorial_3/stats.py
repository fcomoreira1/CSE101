def average(numlist):
    """ Return average of a list of numbers """
    mean = 0
    for i in numlist:
        mean += float(i) / len(numlist)
    return round(mean, 2)
def string_floats_to_list(string_floats):
    """ Return a list from the string of floats string_floats"""
    return [ float(x) for x in string_floats.split(" ")]

def student_data(data_string):
    """Compute (name, results) tuple from the string data_string."""
    (name, results) = data_string.split(" ", 1)
    return (name, string_floats_to_list(results))

def tuple_to_string(name, results):
    """Return string from (name, results) tuple""" 
    return name + ' ' + ' '.join([str(x) for x in results])

def read_student_data(filename):
    """Return list of student data from file"""
    students_list = []
    with open(filename, 'r') as file:
        for line in file:
            students_list.append(student_data(line))
    return students_list

def extract_averages(filename):
    """Return list of name and average for each line in file"""
    list_averages = []
    students_list = read_student_data(filename)
    for student in students_list:
        list_averages.append((student[0], average(student[1])))
    return list_averages

def discard_scores(numlist):
    """Filter numlist: construct a new list from numlist with
    the first two, and then the lowest two, scores discarded.
    """
    newlist = numlist[2:]
    least = [-1,-1]
    for i in range(len(newlist)):
        if least[0] == -1 or newlist[i] < least[0]:
            least[1] = least[0]
            least[0] = newlist[i]
        elif least[1] == -1 or newlist[i] < least[1]:
            least[1] = newlist[i]
    newlist.remove(least[0])
    newlist.remove(least[1])
    return newlist

def summary_per_student(infilename, outfilename):
    """Create summaries per student from the input file 
    and write the summaries to the output file.
    """
    data = read_student_data(infilename)
    total_sum = 0
    with open(outfilename, 'w') as outfile:
        for student in data:
            new_average = discard_scores(student[1])
            output_string = tuple_to_string(student[0], new_average)
            sum = 0
            for i in new_average:
                sum += float(i)
            output_string += ' sum: ' + str(round(sum, 2))
            total_sum += sum
            outfile.write(output_string)
            outfile.write('\n')
        outfile.write("total average: " + str(round(total_sum/len(data), 2)))
        outfile.write("\n")

def summary_per_tutorial(infilename, outfilename):
    """Create summaries per student from infile and write to outfile."""
    data = read_student_data(infilename)
    quantity_tds = len(data[0][1])
    quantity_students = len(data)
    with open(outfilename, 'w') as outfile:
        for i in range(quantity_tds):
            average = 0
            min = -1
            max = -1
            for student in data:
                grade = float(student[1][i])
                average += grade 
                if min == -1 or min > grade:
                    min = grade
                if max < grade:
                    max = grade
            average = round(average/quantity_students, 2)
            outstring = "TD" + str(i+1) + ": average: " + str(average) + " min: " + str(min) + " max: " + str(max) + '\n'
            outfile.write(outstring)
def generate_emails(filename):
    """Generate emails to students with their results"""
    data = read_student_data(filename)
    for student in data:
        with open(student[0] + ".txt", 'w') as file:
            file.write("To: " + str(student[0]) + "@polytechnique.edu\n\n")
            file.write("This is to notify you of your final results for the CSE101 course, see\n")
            file.write("table below.  (Note that the two first and two lowest scores are\n")
            file.write("excluded from the result.)\n\n")
            string = ""
            for i in range(1,len(student[1])+1):
                string += "TD" + str(i)
                spaces = 2
                spaces += max(0, - 2 - len(str(i)) + len(str(student[1][i - 1])))
                for _ in range(spaces):
                    string += " "
            string += "Result"
            file.write(string)
            file.write('\n')
            dotted_line = ""
            for _ in range(len(string)):
                dotted_line += "-"
            file.write(dotted_line)
            file.write('\n')

            grade_string = ""
            for i in range(len(student[1])):
                grade_string += str(student[1][i])
                spaces = 2
                spaces += max(0, - len(str(student[1][i])) + 2 + len(str(i + 1)))
                for _ in range(spaces):
                    grade_string += " "

            final_grades = discard_scores([float(x) for x in student[1]])
            grade_string += str(round(sum(final_grades),2))
            file.write(grade_string)

            file.write('\n\nBest regards,\nand please get back to me if you have any questions,\n')
            file.write('Your Teacher')
