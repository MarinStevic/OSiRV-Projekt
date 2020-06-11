import numpy as np
import cv2
import os

def createLitho(image, minThick, maxThick, dim, name):
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
        print(str(round(i / (height+1) * 20)) + "%")

    f = open("litho/" + name + ".obj", "w")

    f.write("o " + name + "\n")

    for i in range(height+1):
        for j in range(width+1):
            if (i%2 == 0 and j%2 == 0 and temp[i][j] == 0):
                temp[i][j] = int((temp[i-1][j-1] + temp[i-1][j+1] + temp[i+1][j-1] + temp[i+1][j+1]) / 4)
        print(str(round(i / (height+1) * 20) + 20) + "%")

    for i in range(height+1):
        for j in range(width+1):
            if ((i%2 == 0 or j%2 == 0) and temp[i][j] == 0):
                temp[i][j] = int((temp[i+1][j] + temp[i-1][j] + temp[i][j+1] + temp[i][j-1]) / 4)
        print(str(round(i / (height+1) * 20) + 40) + "%")

    for i in range(height+1):
        for j in range(width+1):
            temp[i][j] = minThick + ((maxThick - minThick) / 256 * (256 - temp[i][j]))
            f.write("v " + str(round(j*dim/2, 2)) + " " + str(round(i*dim/2, 2)) + " " + str(temp[i][j]) + "\n")
        print(str(round(i / (height+1) * 20) + 60) + "%")

    # frame
    f.write("v -10 -10 0\n")
    f.write("v " + str(width*dim/2+10) + " -10 0\n")
    f.write("v -10 " + str(height*dim/2+10) + " 0\n")
    f.write("v " + str(width*dim/2+10) + " " + str(height*dim/2+10) + " 0\n")

    f.write("v -10 -10 " + str(maxThick+3.5) + "\n")
    f.write("v " + str(width*dim/2+10) + " -10 " + str(maxThick+3.5) + "\n")
    f.write("v -10 " + str(height*dim/2+10) + " " + str(maxThick+3.5) + "\n")
    f.write("v " + str(width*dim/2+10) + " " + str(height*dim/2+10) + " " + str(maxThick+3.5) + "\n")

    f.write("v -5 -5 " + str(maxThick+3.5) + "\n")
    f.write("v " + str(width*dim/2+5) + " -5 " + str(maxThick+3.5) + "\n")
    f.write("v -5 " + str(height*dim/2+5) + " " + str(maxThick+3.5) + "\n")
    f.write("v " + str(width*dim/2+5) + " " + str(height*dim/2+5) + " " + str(maxThick+3.5) + "\n")

    f.write("v 0 0 " + str(maxThick+1) + "\n")
    f.write("v " + str(width*dim/2) + " 0 " + str(maxThick+1) + "\n")
    f.write("v 0 " + str(height*dim/2) + " " + str(maxThick+1) + "\n")
    f.write("v " + str(width*dim/2) + " " + str(height*dim/2) + " " + str(maxThick+1) + "\n")

    f.write("v 0 0 " + str(minThick) + "\n")
    f.write("v " + str(width*dim/2) + " 0 " + str(minThick) + "\n")
    f.write("v 0 " + str(height*dim/2) + " " + str(minThick) + "\n")
    f.write("v " + str(width*dim/2) + " " + str(height*dim/2) + " " + str(minThick) + "\n")

    f.write("s off\n")

    p = (width + 1) * (height + 1)

    # bottom
    f.write("f " + str(p+1) + " " + str(p+3) + " " + str(p+4) + " " + str(p+2) + "\n")

    # side walls
    f.write("f " + str(p+7) + " " + str(p+3) + " " + str(p+1) + " " + str(p+5) + "\n")
    f.write("f " + str(p+8) + " " + str(p+4) + " " + str(p+3) + " " + str(p+7) + "\n")
    f.write("f " + str(p+6) + " " + str(p+2) + " " + str(p+4) + " " + str(p+8) + "\n")
    f.write("f " + str(p+5) + " " + str(p+1) + " " + str(p+2) + " " + str(p+6) + "\n")

    # top walls
    f.write("f " + str(p+11) + " " + str(p+7) + " " + str(p+5) + " " + str(p+9) + "\n")
    f.write("f " + str(p+12) + " " + str(p+8) + " " + str(p+7) + " " + str(p+11) + "\n")
    f.write("f " + str(p+10) + " " + str(p+6) + " " + str(p+8) + " " + str(p+12) + "\n")
    f.write("f " + str(p+9) + " " + str(p+5) + " " + str(p+6) + " " + str(p+10) + "\n")

    # connecting walls
    f.write("f " + str(p+15) + " " + str(p+11) + " " + str(p+9) + " " + str(p+13) + "\n")
    f.write("f " + str(p+16) + " " + str(p+12) + " " + str(p+11) + " " + str(p+15) + "\n")
    f.write("f " + str(p+14) + " " + str(p+10) + " " + str(p+12) + " " + str(p+16) + "\n")
    f.write("f " + str(p+13) + " " + str(p+9) + " " + str(p+10) + " " + str(p+14) + "\n")

    f.write("f " + str(p+15) + " " + str(p+13))
    for i in range(height+1):
        f.write(" " + str(i*(width+1)+1))
    f.write("\n")

    f.write("f " + str(p+16) + " " + str(p+15))
    for i in range(width+1):
        f.write(" " + str(p-width+i))
    f.write("\n")

    f.write("f " + str(p+14) + " " + str(p+16))
    for i in range(height+1):
        f.write(" " + str(p-((width+1)*i)))
    f.write("\n")

    f.write("f " + str(p+13) + " " + str(p+14))
    for i in range(width+1):
        f.write(" " + str(width+1-i))
    f.write("\n")

    for i in range(height+1):
        for j in range(width+1):
            if not (i%2 == 0 or j%2 == 0):
                f.write("f " + str(i*(width+1)+j+1) + " " + str((i+1)*(width+1)+(j+1)+1) + " " + str((i+1)*(width+1)+(j)+1) + "\n")
                f.write("f " + str(i*(width+1)+j+1) + " " + str((i)*(width+1)+(j+1)+1) + " " + str((i+1)*(width+1)+(j+1)+1) + "\n")
                f.write("f " + str(i*(width+1)+j+1) + " " + str((i-1)*(width+1)+(j+1)+1) + " " + str((i)*(width+1)+(j+1)+1) + "\n")
                f.write("f " + str(i*(width+1)+j+1) + " " + str((i-1)*(width+1)+(j)+1) + " " + str((i-1)*(width+1)+(j+1)+1) + "\n")
                f.write("f " + str(i*(width+1)+j+1) + " " + str((i-1)*(width+1)+(j-1)+1) + " " + str((i-1)*(width+1)+(j)+1) + "\n")
                f.write("f " + str(i*(width+1)+j+1) + " " + str((i)*(width+1)+(j-1)+1) + " " + str((i-1)*(width+1)+(j-1)+1) + "\n")
                f.write("f " + str(i*(width+1)+j+1) + " " + str((i+1)*(width+1)+(j-1)+1) + " " + str((i)*(width+1)+(j-1)+1) + "\n")
                f.write("f " + str(i*(width+1)+j+1) + " " + str((i+1)*(width+1)+(j)+1) + " " + str((i+1)*(width+1)+(j-1)+1) + "\n")
        print(str(round(i / (height+1) * 19) + 80) + "%")
    
    f.close()
    print("100%\nDONE!")
    return temp

imgName = input("Unesite ime slike: ")
img = cv2.imread("images/" + imgName, 0)

minThickness = input("Unesite minimalnu debljinu (mm, default=0.6): ")
if (minThickness == ""):
    minThickness = 0.6
maxThickness = input("Unesite maksimalnu debljinu (mm, default=3.0): ")
if (maxThickness == ""):
    maxThickness = 3.0

while (True):
    x = input("Odaberite:\n  1. Odabir veličine pixela\n  2. Odabir veličine cijelog objekta\nOdabir: ")
    if (x == "1"):
        x = input("Unesite velicinu pixela (mm, default=0.2): ")
        if (x == ""):
            dim = 0.2
        else:
            dim = int(x)
        break
    elif (x == "2"):
        while (True):
            x = input("Odaberite:\n  1. Odabir visine\n  2. Odabir širine\nOdabir: ")
            if (x == "1"):
                x = input("Unesite visinu (mm, default=200): ")
                if (x == ""):
                    dim = 180 / img.shape[1]
                else:
                    dim = (int(x) - 20) / img.shape[0]
                break
            elif (x == "2"):
                x = input("Unesite širinu (mm, default=200): ")
                if (x == ""):
                    dim = 180 / img.shape[1]
                else:
                    dim = (int(x) - 20) / img.shape[1]
                break
        break

print("Odabrani parametri:")
print("Slika: " + imgName)
print("Debljina: " + str(minThickness) + "-" + str(maxThickness) + "mm")
print("Veličina pixela: " + str(dim) + "mm")
input("Press enter to continue...")

lithophane = createLitho(img, minThickness, maxThickness, dim, imgName.split(".")[0])

# try:
#     lithophane = createLitho(img, minThickness, maxThickness, dim, imgName.split(".")[0])
# except:
#     print("Something went wrong. Please try again. Check your parameters.")