def distance

dims = None
while type(dims) is not int:
    try:
        dims = int(input("\nHow many dimensions does your space have ?\n"))
    except:
        pass;

print("Your space has", dims ,"dimensions so you must define the coordinates of", dims+1, "emitters and their distance from the target.")

emitters = []

for i in range(dims+1):
    current_emitter = []
    coordinates = input("Coordinates of emitter {} :\n".format(i))
    for data in coordinates.split(";"):
        current_emitter.append(float(data))
    emitters.append(current_emitter)

estimator = [0.,0.,0.]

to_minimize = 