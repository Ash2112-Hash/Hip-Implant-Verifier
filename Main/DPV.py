#

# Imports the respective libraries
import time
import math

def Subprogram_1(body_weight, canal_diameter,ult_ten_strength):  # Subprogram 1 - Calculating the minimum stem diameter of the implant
    load = 3.25 * body_weight
    min_stem_dia = 0.80 * canal_diameter

    def stress_calculation(implant_load, stem_dia):
        axial_stress = implant_load / (math.pi / 4 * (stem_dia ** 2))
        bending_stress = (implant_load * 38 * (0.5 * stem_dia)) / (math.pi / 64 * (stem_dia ** 4))
        ten_stress = (-axial_stress) + bending_stress
        return ten_stress

    app_ten_stress = stress_calculation(load, min_stem_dia)

    while app_ten_stress >= ult_ten_strength:
        min_stem_dia += 0.1
        app_ten_stress = stress_calculation(load, min_stem_dia)

    print("Body weight of Patient:", round(float(body_weight), 1), "Newtons")
    print("Diameter of the Medullary Canal of Patient's femur:", round(float(canal_diameter), 1), "mm")
    print("Ultimate Tensile Strength (UTS) of stem material:", round(float(ult_ten_strength), 1), "MPa")
    print("Minimum implant stem diameter corresponding to applied tensile stress:", round(float(min_stem_dia), 1), "mm")
    print("Applied Tensile Stress of stem material:", round(float(app_ten_stress), 1), "MPa")



def Subprogram_2(body_weight, stem_dia,team_number):  # Subprogram 2- calculating the fatigue life of our implant design

    # this function gets a list of cycles to be used in later calculations
    def cycles_fail_list():
        N = []
        file = open("SN Data - Sample Polymer.txt", "r")
        lines = file.readlines()
        for i in lines:
            N.append(int((i.split()[1])))
        file.close()
        return N

    # this calculates adjusted stress amplitude
    def calc_adj_stress_amp(N):
        stress_amp = (((12 * int(body_weight)) - (-12 * int(body_weight))) / ((math.pi * (stem_dia / 2) ** 2) / 2))
        adj_stress_amp = []
        for i in N:
            adj_stress_amp.append(((8.5 + math.log(i, 10) ** ((0.7 * team_number) / 40)) * stress_amp))
        return (adj_stress_amp)

    # this function compares SN values with calculated values to determine final adjusted stress amplitude
    def calc_stress_fail(stress, N):
        S = []
        with open("SN Data - Sample Polymer.txt", "r") as file:
            for i in file:
                S.append(float((i.split()[0])))
        for i in range(len(S)):
            if stress[i] < S[i]:
                print("\n")
                print("Cycles to failure:", round(N[i], 1))
                print("The adjusted stress amplitude is", round(stress[i], 1), "MPa")
                break

            else:
                print('Implant will not fail under max cyclical load:', round(max(N), 1), "(number of cycles)")
                break

    N = cycles_fail_list()
    print(N)
    stress = calc_adj_stress_amp(cycles_fail_list())
    calc_stress_fail(stress, N)




def Subprogram_3(body_weight, modulus_bone, modulus_implant, outer_dia, canal_diameter):
    load = 30 * body_weight  # calculating the load using 30*Body weight
    area = (math.pi / 4) * (outer_dia ** 2 - canal_diameter ** 2)

    stress_comp = load / area

    stress_reduc = stress_comp * ((3 * modulus_bone) / (modulus_bone + modulus_implant)) ** (1 / 3)

    yrs = 0
    E_ratio = math.sqrt(modulus_implant / modulus_bone)
    comp_strength = (0.0015 * yrs ** 2) - (3.752 * yrs * E_ratio) + 168.54

    while comp_strength != stress_reduc:
        comp_strength = (0.0015 * yrs ** 2) - (3.752 * yrs * E_ratio) + 168.54
        print("Year:", yrs, "\t", "Compressive Strength:", round(comp_strength, 1), "MPa")
        if comp_strength > stress_reduc:
            yrs += 1
        else:
            break
    stress_fail = comp_strength
    yrs_fail = yrs

    print("The implant will fail", yrs_fail, "years after implantation.")
    print("The compressive strength when the implant fails is", round(stress_fail, 1), "MPa.", "\n")


def menu():
    print("""
Program Menu
    1. Subprogram 1
    2. Subprogram 2
    3. Subprogram 3
    4. Exit from program
    """
          )

    choice = int(input("Please enter your subprogram of choice: "))

    return choice




def main():
    print("Welcome to the Python DPV (Design Parameter Verifier)!")

    time.sleep(0.3)

    factor = 10 # Factor is a number used to differentiate results based on each patient, feel free to change this to accomadate your patient
    body_weight = 637  # BW = 65*9.8
    outer_dia = 30
    canal_diameter = 14
    femoral_head_offset = 38
    modulus_bone = 17  # Literature: Y. Lai, W. Chen, C. Huang, C. Cheng, K. Chan and T. Chang, "The Effect of Graft Strength on Knee Laxity and Graft In-Situ Forces after Posterior Cruciate Ligament Reconstruction", PLOS ONE, vol. 10, no. 5, p. e0127293, 2015. Available: 10.1371/journal.pone.0127293 [Accessed 7 December 2021].
    ult_ten_strength = 120  # Material: CFR PEEK
    modulus_implant = 14  # Material: CFR PEEK
    stem_dia = 19  # Actual diameter of our stem

    print(
        "Please enter a number corresponding to the desired subprogram. For example, to access 'Subprogram 1', please enter 1.")  # Instructions on how to use program menu
    print("Please enter 4 to quit the program.")  # Instructions on how to use program menu

    time.sleep(0.3)

    user_choice = menu()

    while user_choice != 4:
        time.sleep(0.1)

        if user_choice == 1:
            Subprogram_1(body_weight, canal_diameter, ult_ten_strength)

        elif user_choice == 2:
            Subprogram_2(body_weight, stem_dia, factor)

        elif user_choice == 3:
            Subprogram_3(body_weight, modulus_bone, modulus_implant, outer_dia, canal_diameter)

        else:
            print("Sorry, please enter another value")

        time.sleep(2)
        user_choice = menu()

    time.sleep(0.5)
    print("Thank you for your using the Python DPV. Have a great day!")


main()
