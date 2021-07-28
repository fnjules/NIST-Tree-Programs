from vpython import*
from fpdf import FPDF
import os

#check where are files are being saved
cwd = os.getcwd()
print("Current working directory:", cwd)

#help setup environment
maxradius=1

def setupEnvironment():
    #greate graph environment
    circGraph= graph(fast=False, width=1000, height=1000,
        xmin=-1.1, xmax=1.1, ymin=-1.1, ymax=1.1,
        title="Tree Program")
    #circle/origin setup
    f1 = gcurve(fast=False, color=color.cyan)
    for theta in arange(0, 2*pi, 0.01):
        f1.plot(maxradius*cos(theta),maxradius*sin(theta))
    finit = gdots(fast=False, color=color.red)
    finit.plot([0,0])

if __name__ == "__main__":
    setupEnvironment()



mylines = [] # Declare an empty list named mylines.
with open ("yourName.txt", "rt") as myfile: # Open .txt for reading text data.
    mylines = [myline.strip() for myline in myfile] # For each line, stored as myline, add its contents to mylines; strip away spaces
split=int(mylines[0])  #get split value
rounds=int(mylines[1]) #get rounds value
Radius=float(mylines[2])#get Radius value
dateName=str(mylines[3])#get date
myPoints = [line.split('\t') for line in mylines[4:]] #put the points into a list of lists; split a string into a list
myPoints = [[float(coord) for coord in pair] for pair in myPoints] #turn all values (numbers stored as strings/integers) into floats (back to floating pt. number)
print(myPoints)



length = len(myPoints)

for i in range(length):
    X1 = myPoints[i][0]
    X2 = myPoints[i][2]
    Y1 = myPoints[i][1]
    Y2 = myPoints[i][3]
    gcurve(markers=True, fast=False, width=1, marker_color=color.red, color = color.black, radius = 2).plot([ [X1, Y1], [X2, Y2] ])

# Python program to convert text file to pdf file   
# save FPDF() class into a variable pdf
pdf = FPDF()   
   
# Add a page
pdf.add_page()
   
# set style and size of font 
# that you want in the pdf
pdf.set_font("Arial", size = 15)
pdf.image("yourName.png", x = None, y = None, w = 150)
  
# open the text file in read mode
f = open("yourName.txt", "r")
  
# insert the texts in pdf
for x in f:
    pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
   
# save the pdf with name .pdf
pdf.output("yourName.pdf")

#This would go at the end of the second program, Tree Program Duplicator
#To downlaod png, click on the far left icon at the top right of the graph
#"yourName" is a dummy name
#Ensure that all names for the text and pdf files match up with names assigned in Third_Modification2.py for this to work
