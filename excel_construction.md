## Tricks for constructing excel for model
### **Insert \n for seperate lines**  
If the variable name is too long and will cause to the intersection of name and axis, for instance, 
variable **Cumulative dose of prednisone during pre-engraftment phase** in the following figure.
  ![image](https://user-images.githubusercontent.com/105685749/229343537-867ed1a1-3a2b-43d8-acfe-e3c60554d52f.png)
Then insert \n in the name, for instance,
  ![image](https://user-images.githubusercontent.com/105685749/229343673-84b419c3-8b66-41f6-bd4a-5ec44fb9e0bd.png)
In this case, you will get the nomogram,
  ![image](https://user-images.githubusercontent.com/105685749/229343696-08b3e453-ca07-4c0e-863e-c38a8fafd22c.png)

### **type can be filled with "norminal", "ordinal", "continuous"**

### **Use _ for one-hot coding variables of nominal data & fill up in position columns to advoid intersections.**
If the variable is nominal and processed with one-hot encoding, to draw the variable as the same line, the variable can be filled as "variable_value",
for instance,  

![image](https://user-images.githubusercontent.com/105685749/229344355-4ae1ccc5-d48e-48d9-86d3-0be471919bf5.png)  
However, there can be intersections, for instance,  

![image](https://user-images.githubusercontent.com/105685749/229344385-283482e8-8e65-4122-bb18-decd13c65252.png)
In this case, you can put up in the position columns of which value you want it to move above, for instance,  
![image](https://user-images.githubusercontent.com/105685749/229344518-dda9784a-6f6c-442c-97ee-f8b44f234c29.png)  
Then you can get the nomogram without overlapping.
![image](https://user-images.githubusercontent.com/105685749/229344534-61af05b2-4b58-42b2-8ab1-ce26c15d0ac1.png)


