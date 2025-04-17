#------Concepts Learnt----------

#variables are like containers/jars that store values. Also we can say they are the labels for the values.

#input() is like expecting the user to input some value for the things that we show relatively.

# BUILDING A FRIENDLY CHATBOT

name = input("Hey Mate!!, What's your name?:")

r1 = f"{name},That's a striking name my mate😉."

mood = input("Well!!, What's your mood right now?:")

r2 = f"Oh!!, You seem to be here on a purpose to {mood}. That's fanatastic mate." 

subject = input(f"{name}, what do you wanna learn?:")

r3 = f"Well, you wanna learn {subject}.That's so cool to know."

history =input(f"Sure, {subject} is quite a booming topic and it's gonna revolutionize the way we think of the future.Do you want to know the history of it {name}?:")

#printing the conversation history that's there in mind

print("-----Conversation History-----")

print(r1)

print(r2)

print(r3)

print(history)
