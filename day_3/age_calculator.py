#Operators and Expressions

#Operators are of three types: 
    # 1) Arithematic Operators -> [+,-,*,/,//,**]
    # 2) Comparision Operators -> [==,>,<,>=,<=,!=]
    # 3) Comditional Operators -> [True,False]

### AGE CALCULATOR
name_1 = input("Hello!, What's your name?:")
r1 = f"Hey {name_1}!!, Welcome to Age-Magic:)"
gender = input("Are you Male/Female?:").strip().lower()
if(gender=="male"):
    r2 = f"Sir, This is a show where we let you know you are younger to someone or older to someone."
else:
    r2 = f"Madam,This is a show where we let you know you are younger to someone or older to someone."
age = int((input(f"Would you please enter your age {name_1}?:")))
if(gender=="male"):
    r3 = f"Oh!! Wow, you look so charming sir😉"
else:
    r3 = f"Oh!! Wow, you look so charming madam😉"
name_2 = input("May i know your relative name:")
age_1 = int(input("May i know your relative age:"))

print("-------AGE RESULT MAGIC-------")
if(age>age_1):
    print("Hey!!", name_1 , "You're older than", name_2)
elif(age<age_1):
    print("Hey!!", name_1, "You're younger than", name_2)
elif(age==age_1):
    print("You &",name_2,"are born as friends yaar!! You people are of same age:)")

print("-----Conversation History-----")
print(r1)
print(r2)
print(r3)