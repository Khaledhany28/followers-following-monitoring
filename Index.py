from User_class import User
import subprocess


print("1. Update your followers and following list")
print("2. Update your followers list only")
print("3. Update your following list only")
print("4. print old followers list")
print("5. print old following list")

userChoice = int( input("Choose the option you want:") )

user = User()

if userChoice == 1:
    user.updateFollowers()
    user.updateFollowing()

elif userChoice == 2:
    user.updateFollowers()

elif userChoice == 3:
    user.updateFollowing()

elif userChoice == 4:
    old = user.loadOldFollowers()

    counter = 1
    for name in old:
        print(f"{counter} - {name}")
        counter+=1

elif userChoice == 5:
    old = user.loadOldFollowing()

    counter = 1
    for name in old:
        print(f"{counter} - {name}")
        counter+=1

else:
    raise ValueError("Unknown Choice")


if userChoice in [1,2,3]:
    subprocess.run(["explorer", fr"Output\{user.username}"])