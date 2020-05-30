import numpy as np
import cv2
import os

def createLitho(image, minThick, maxThick, dim):
    width = image.shape[1]*2
    height = image.shape[0]*2
    temp = np.zeros((height+1, width+1), dtype=float)
    for i in range(height+1):
        for j in range(width+1):
            if (i == 0 or j == 0 or i == height or j == width):
                temp[i][j] = 128
            elif (i%2 == 0 or j%2 == 0):
                temp[i][j] = 0
            else:
                temp[i][j] = image[int((i-1)/2), int((j-1)/2)]
            # print(temp[i*width+1+j])
        print(str(round(i / (height+1) * 33)) + "%")

    f = open("lithophane.obj", "w")

    # f.write("v 0 0 0\n")
    # f.write("v " + str(width*dim) + " 0 0\n")
    # f.write("v 0 " + str(height*dim) + " 0\n")
    # f.write("v " + str(width*dim) + " " + str(height*dim) + " 0\n")

    for i in range(height+1):
        for j in range(width+1):
            if ((i%2 == 0 or j%2 == 0) and temp[i][j] == 0):
                temp[i][j] = int((temp[i-1][j] + temp[i+1][j] + temp[i][j-1] + temp[i][j+1]) / 4)
            temp[i][j] = 256 - temp[i][j]
            temp[i][j] = minThick + ((maxThick - minThick) / 256 * temp[i][j])
            f.write("v " + str(round(j*dim, 2)) + " " + str(round(i*dim, 2)) + " " + str(temp[i][j]) + "\n")
        print(str(round(i / (height+1) * 33) + 33) + "%")

    # f.write("f 1 2 3 4\n")
    # f.write("f 1 2 3 4\n")
    # f.write("f 1 2 3 4\n")
    # f.write("f 1 2 3 4\n")
    # f.write("f 1 2 3 4\n")

    for i in range(height):
        for j in range(width):
            f.write("f " + str(i*(width+1)+j+1) + " " + str((i+1)*(width+1)+j+1) + " " + str((i+1)*(width+1)+j+2) + "\n")
            f.write("f " + str(i*(width+1)+j+1) + " " + str(i*(width+1)+j+2) + " " + str((i+1)*(width+1)+j+2) + "\n")
        print(str(round(i / (height+1) * 33) + 66) + "%")
    
    f.close()
    print("100%\nDONE!")
    return temp

imgName = input("Unesite ime slike: ")
img = cv2.imread(imgName, 0)

minThickness = input("Unesite minimalnu debljinu (mm, default=0.6): ")
if (minThickness == ""):
    minThickness = 0.6
maxThickness = input("Unesite maksimalnu debljinu (mm, default=3.0): ")
if (maxThickness == ""):
    maxThickness = 3.0

while (True):
    x = input("Odaberite:\n  1. Odabir veličine pixela\n  2. Odabir veličine cijelog objekta\nOdabir: ")
    if (x == "1"):
        dim = input("Unesite velicinu pixela (mm, default=0.2): ")
        if (dim == ""):
            dim = 0.2
        break
    elif (x == "2"):
        while (True):
            x = input("Odaberite:\n  1. Odabir visine\n  2. Odabir širine\nOdabir: ")
            if (x == "1"):
                dim = input("Unesite visinu (mm, default=0.2): ")
                if (dim == ""):
                    dim = 0.2
                else:
                    dim = dim / img.shape[0]
                break
            elif (x == "2"):
                dim = input("Unesite širinu (mm, default=0.2): ")
                if (dim == ""):
                    dim = 0.2
                else:
                    dim = dim / img.shape[1]
                break
        break

print("Odabrani parametri:")
print("Slika: " + imgName)
print("Debljina: " + str(minThickness) + "-" + str(maxThickness) + "mm")
print("Veličina pixela: " + str(dim) + "mm")
input("Press enter to continue...")

lithophane = createLitho(img, minThickness, maxThickness, dim)