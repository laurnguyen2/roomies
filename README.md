# roomies
cs50 fall 2021 final project

Link to video: https://youtu.be/6slF1HLojzA

User’s Manual

1) Setting Up VS Code

In order to use our program, you must have VS Code, a source-code editor designed for  programming applications and websites, installed and running on your laptop device. 

- Visit https://code.visualstudio.com/ for download links for each of the computer softwares VS Code supports. More specifically, laptop and desktop devices that use Windows, Linus, and macOS will be able to run this application.
- Depending on your laptop device and the software it operates on, select the download link that correlates with your device and wait for the zip file to download. 


After successfully following the instructions prompted by the file to download VS Code, you now should be able to have VS Code successfully installed and running on your device. You can now open the VS Code and drop code files from github into the 
VS Code Explorer tab. 

- With VS Code still open in a tab, visit https://github.com/laurnguyen2/roomies in your website browser order to access our code files for our final project. 
- On the website, click the green button that says “Code” and then from that dropdown list, click “download zip” in order for the code to be transferred into VS Code. 
- After downloading the zip files of our program, drag and drop the files into the explorer tab of VS Code. This action will allow you to see all of the code that we’ve implemented for this program. 



2) Flask Tutorial

There are some commands that need to be taken care of first before being able to access the website. Flask, a command able to provide a basic understanding for URL routing and page rendering, needs to be installed in our VS Code in order to get the actual link to our website. 
- In order to get flask installed in VS Code, visit https://marketplace.visualstudio.com/items?itemName=ms-python.python
  to download the Python extension

- Click on “Install” 

3) VS Code and Terminal Commands 
A. VS CODE: 
- Go back to VS Code, and open a new terminal by clicking going to “Terminal” -> “New Terminal” on your desktop
- Click on the “Explore” tab on the left, and Add a new folder to create a project environment for this Flask tutorial. 
- Revisit the Flask tutorial website (https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  And focus on Step 2 under the “Create a project environment for the Flask tutorial” heading. 


B. Terminal Commands: 
In your terminal, carry out the following commands: 
- Depending on your device’s software, copy and paste the following text that is presented under the software’s device (that suits your device) into the terminal. 
- Go to File > Open Folder 
- In VS Code, open the Command Palette (View > Command Palette) and select the “Python: Select Interpreter” Command. 
- From the list given, select the virtual environment in your folder that starts with ./.venv or .\.venv
- Run Terminal: Create New Terminal which will automatically activate the virtual environment you selected. 

Update pip in the virtual environment by running such commands: 
- Type “python -m pip install --upgrade pip”
- Type “python -m pip install flask”

Because we are using SQL from CS50, it is important that CS50 commands are also installed in your application as well: 
- Type “Pip3 install cs50” 
- Type “Pip3 install Flask-Session”
- Type “pip install Flask-Session”
- Type python3 -m “pip install requests”
- Last but not least, type “export FLASK_ENV=development”

4. Running the Website: 
Now that you have finished installing flask and CS50 SQL commands, you are now able to run the actual website
- Type “flask run” in your terminal 
- Type Command -> C and immediately afterwards click on the link presented in the terminal after carrying out flask run. At this point, you should be taken to our website 
- Welcome to Roomies! In order to use the website to get your roommate match, make sure to register as a potential roommate at the top right corner with the button “Register”, Input your registration information and submit. 
- Afterwards, login to your roommate profile on the top right corner with the button “Login”
- You are now ready to take the roommate quiz. In order to do this, make sure to click on the “Homepage on the top left corner and click the “Take Quiz” button. After filling out the form, press “Submit”. 
- In order to see your roommate match, revisit the home page and press on the “Find Your Match” to find more information about your roommate. 
