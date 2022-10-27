# Reagent Calculator
# Script Takes User Input for Number of Samples to Run
# For Each Number of Sample, Accepts User Input for Demographics
# From Demographic Entry, Summation Dilutions for Resource Count
# Calculate Resources Required
# Show User How Much Reagent to Prepare BSA and PNP

# Nijmegen Calculator
# Script unpacks each Patient and Dilutions allowing for Result Entry
# For each Dilution, Function converts Entered Value to Residual Activity
# From Residual Activity, Presence of Inhibitor is Determined
# If Inhibitor is Present, Find Closest to 50% Activity and Return Dilution Corrected Bethesda Unit

# File Output
# For Each Patient, Attributes and Results unpacked and loaded into Excel template
# Excel Template Saves into New File with Designated File Name and File Path
# User Prints Files

# Class saves Patient Demographics into Profile Object
class Patient():
    def __init__(self, first_name, last_name, sample_id, mrn, factor, dilutions, array, inhibitor):
        self.first_name = first_name
        self.last_name = last_name
        self.sample_id = sample_id
        self.mrn = mrn
        self.factor = factor
        self.dilutions = dilutions # Integer from 1-13
        self.array = array # Dilution Array with Results and Calculations
        self.inhibitor = inhibitor # Boolean Statement for Inhibitor Presence, Default False

# User Input Error Check Functions
def is_number(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_limit(value):
    if value[0] not in (">","<"):
        return True
    elif (value[0] in (">","<")) and (len(value[1:]) > 0) and (is_float(value[1:]) == True):
        return True
    else:
        return False

# Function to Check and Limit Samples Run
def get_workload():
    while True:
        workload_string = input("Number of Inhibitors to Run: ")
        # Check if Input is a Valid Number
        if not is_number(workload_string):
            print("Not a valid number")
            continue
        # Check if Input is Within Range
        workload = int(workload_string)
        if workload >= 10:
            print("Workload exceeds suggested limits")
            continue
        return workload

# Function to Obtain Factor Result
def get_factor():
    while True:
        factor_string = input("Factor VIII Result: ")
        # Check if Limit Breaker
        if not is_limit(factor_string):
            # Check if Input is a Valid Number
            if not is_float(factor_string):
                print("Not a valid number")
                continue
            continue
        return factor_string

# Function to Obtain Dilutions with Error and Limitation Checking
def get_dilutions():
    while True:
        dilutions_string = input("Number of Dilutions: ")
        # Check if Input is a Valid Number
        if not is_number(dilutions_string):
            print("Not a valid number")
            continue
        # Check if Input is Within Range
        dilutions = int(dilutions_string)
        if dilutions not in range(1,14):
            print("Dilutions not within range")
            continue
        return dilutions

# Function Allows User to Input Patient Demographics
def get_patient():
    first_name = str(input(("Patient First Name: "))).lower().capitalize()
    last_name = str(input(("Patient Last Name: "))).lower().capitalize()
    sample_id = str(input(("Sample ID: "))).lower().capitalize()
    mrn = str(input(("Patient ID: "))).lower().capitalize()
    # Fetch Results with Error Checking
    factor = get_factor()
    dilutions = get_dilutions()
    # Initialize Results Array
    array = [['Neat',None,None,None,None]]
    for x in range(2,14):
        array.append([str(2 ** x), None, None, None, None])
    # Default Inhibitor Setting
    inhibitor = False

    patient = Patient(first_name, last_name, sample_id, mrn, factor, dilutions, array, inhibitor)
    return patient

# Calculate BSA Needed for Each Patient and Controls
def bsa_resource(all_dilutions):
    # Controls Require 2 BSA
    bsa_total = 2 + all_dilutions
    # Convert to Vials Required
    bsa_needed = (bsa_total*200/1500)
    return round(bsa_needed, 2)

# Calculate PNP Needed for Each Patient and Controls
def pnp_resource(all_dilutions,num_samples):
    # Controls Require 4 PNP
    pnp_total = 4 + all_dilutions + num_samples
    # Convert to Vials Required
    pnp_needed = (pnp_total*200/1500)
    return round(pnp_needed, 2)

# Function to Calculate Residual Factor
def get_residual(control_mix, value):
    residual_factor = (value/control_mix)*100
    residual_factor = round(residual_factor,3)
    return residual_factor

# Function to Calculate Bethesda Unit
def get_bethesda(residual_factor, dilution_factor):
    import math
    bethesda = ((2-math.log10(residual_factor))/0.30103)*dilution_factor
    bethesda = round(bethesda,3)
    return bethesda

# Allows User Input of Control Values
def get_controls(control_array):
    # Cycle down the Controls to Accept User Input
    for x in range(0,4):
        factor_string = input(control_array[x][0] + " Factor Result : ")
        if not is_float(factor_string):
            print("Not a valid number")
            continue
        control_array[x][1] = float(factor_string)

    # Define Control Mix for Calculations
    global control_mix
    control_mix = control_array[0][1]
    # Calculate Residual Activity, Bethesda for Each Control
    for x in range(1,4):
        control_array[x][2] = get_residual(control_mix, control_array[x][1])
        control_array[x][3] = get_bethesda(control_array[x][2], 1)
    # Calculate Corrected Bethesda for Each Control with Dilution
    for x in range (1,3):
        control_array[x][4] = control_array[x][3]
    control_array[3][4] = control_array[3][3]*2

    return control_mix, control_array

# Allows User Input of Patient Results
def get_results():
    for patient in all_patients:
        print (patient.sample_id)
        print (patient.last_name,",",patient.first_name)
        # Data Entry for Patient
        for x in range(0, patient.dilutions + 1):
            factor_string = input( patient.array[x][0] + " Factor Result : ")
            if not is_float(factor_string):
                print("Not a valid number")
                continue
            patient.array[x][1] = float(factor_string)
        # Iterate through Calculations
        for x in range(0, patient.dilutions + 1):
            patient.array[x][2] = get_residual(control_mix, patient.array[x][1])
            patient.array[x][3] = get_bethesda(patient.array[x][2], 1)
        # Calculate Corrected Bethesda for Each Control with Dilution if % RA outside Limits
        for x in range(1, patient.dilutions + 1):
            if patient.array[x][2] > 25 and patient.array[x][2] < 75:
                patient.array[x][4] = patient.array[x][3] * int(patient.array[x][0])
                # Corrected Bethesda Indicates Presence of Inhibitor
                patient.inhibitor = True

# Finds Closest to 50% RA
def find_fifty():
    # Create List of % RA for Each Dilution Entry
    temp_list = []
    for x in range(0, patient.dilutions + 1):
        current_value = patient.array[x][2]
        temp_list.append(current_value)
    # Iterate Through patient.array[x][2] list to find closest %RA to 50
    closest_value = min(temp_list, key=lambda x:abs(x-50))
    closest_index = temp_list.index(closest_value)
    return closest_index

if __name__ == '__main__':

    all_patients = []
    all_dilutions = 0

    control_array = [
        ["Control Mix",None],
        ["Negative",None,None,None,None],
        ["Positive Neat",None,None,None,None],
        ["Positive x2",None,None,None,None]
    ]

    # Get Number of Samples to Run
    num_samples = get_workload()
    for x in range(num_samples):
        patient = get_patient()
        all_patients.append(patient)
    # Tally Total Dilutions
    for patient in all_patients:
        all_dilutions += patient.dilutions

    # Tally BSA and PNP Totals
    print("# of BSA Required: ", bsa_resource(all_dilutions))
    print("# of PNP Required: ", pnp_resource(all_dilutions, num_samples))

    # Allow Control Result Entry
    get_controls(control_array)

    # Temporary Code to Print Control Array
    for x in range(0,4):
        print(control_array[x])

    # Allow Patient Result Entry
    get_results()

    # Temporary Code to Print Patient Results
    for patient in all_patients:
        print(patient.last_name,",",patient.first_name)
        print(patient.sample_id)
        print(patient.mrn)

        for x in range(0, patient.dilutions +1):
            print(patient.array[x])
        if patient.inhibitor == True:
            # Find Closest to Fifty
            closest_index = find_fifty()
            # Use Found Fifty For Details
            print("Inhibitor Detected at x", patient.array[closest_index][0], " with ",patient.array[closest_index][4], " BU/mL")
        else:
            print("None Detected")

# Allow User to Return to Amend Patient Demographics and Dilutions
