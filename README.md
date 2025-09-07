# TedsBarAndCafe
This application is simple customer side platform that allows them to browse shop menu, select items from menu and learn about those items, add items to cart and purchase them by adding their payment info. Apart from this, there is about us page where users can learn information about the shop and a contact us page where they can message to the shop and navigate the static location of the shop. 

Technologies used:
This application is developed using Flask as Backend, HTML,CSS,and JavaScript as Frontend and PostgreSQL as database.

How to run this application:
Step 1: Open your command line and open the directory where you want to save the application.
Step 2: run the command "git clone https://github.com/1322harshd/TedsBarAndCafe"
Step 3: After application folder is created open it in command line and run command "python -m venv venv". This will create a virtual emvironment inside your application folder.
Step 4: Activate your virtual environment by entering command "source venv/bin/activate" or 
"venv\Scripts\activate.bat" for windows in command prompt.
Step 5: We need to install certain dependencies to run the application so run the command "pip install -r requirements.txt" to install the dependencies.
Step 6:Now, your application is ready to run but you need to setup database first,so to do that open your pg admin and create new database with name of your choice.
Step 7: Now restore the database using dump file in application folder this will add data from the file to your newly created database.
Step 8: Now change the connection string on line 31 with 'postgresql://postgres:**yourpassword**@localhost/**yourdatabasename**' by adding the password and db name.
Step 9: Now enter command "python app.py" to run the application.