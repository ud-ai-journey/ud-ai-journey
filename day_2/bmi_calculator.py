#------Concepts Learnt----------

# type casting:
# 1) str to return string 
# 2) int to return int(math values)
# 3) float to return floating point values like 123.4567
# 4) bool to return True or False

# output formatting 
# 1) {:.2f} --> to round off values to 2
# 2) .format(values) --> to make sure all the corresponding values get frmatted or printed accordingly.

#BUILDING BMI CALCULATOR

#--BMI= weight/height

name = input("Hello!!, What's your name?:")

age = int(input(f"{name}, Would you please disclose your age?:"))

weight = float(input(f"{name},you seem to be an energitic individual, May I know your weight in (kg's) ?:"))

height = float(input(f"{name}, Now you are 1 step away from the surprise, Could you please tell me your height in (m)*2 ? :"))

BMI = weight/height**2

print(f"Hey!!, {name}, your Body Mass Index is {BMI:.2f}.\n")

print("---------BMI CARD DETAILS---------- \n")
print("NAME:{}\n AGE:{} \n WEIGHT:{} \n HEIGHT:{} \n BMI:{:.2f}".format(name,age,weight,height,BMI))