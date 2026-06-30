import matplotlib.pyplot as plt

subjects = ["python","Java","SQL","Power BI"]
students = [40,30,20,10]

plt.pie(students,labels=subjects)
plt.title("Students Enrolled")
plt.show()
