# DARPG-Hackathon

Below given are the step-by-step execution process steps for this Django-based project for the DARPG Hackathon 2023 :

1. ## Clone the Repository:
   ### git clone https://github.com/anurag8423/Hackathon-DARPG.git
   ### cd <repository_directory>

2. ## Create a Virtual Environment:
   ```bash
   py -m venv virtual

4. ## Activate the Virtual Environment:
   - On Windows:
     ```bash
     virtual\Scripts\activate
     
   - On macOS/Linux:
     ```bash
     virtual/bin/activate

5. ## Install Dependencies:
   ```bash
   pip install -r requirements.txt

7. ## Apply Database Migrations:
   ```bash
   python manage.py migrate


8. ## Run the Development Server:
    ```bash
    python manage.py runserver

9. ## Access the Application:
    Open a web browser and go to `http://127.0.0.1:8000/` to view the application.

10. ## Deactivate the Virtual Environment:
    When you're done working on the project, deactivate the virtual environment.
    ```bash
    deactivate


## Important Note:
* ### After creating and activating the virtual environment, make sure you are in the same directory as of the home, static, & DARPG folder, before performing the further steps.


* ### Make sure you have enabled the script execution permission on your system before activating the virtual environment. To do this you can refer to the following steps to do so:
1. #### Open the PowerShell as administrator

2. #### Set the excution policy to unrestricted by giving the following command:
   ```bash
   Set-ExecutionPolicy Unrestricted

3. #### After pressing enter for the above command , press y/Y to confirm the command.

4. #### Now after activating the virtual environment, disable the script execution for the system's security, you can do so by giving the following command:
   ```bash
   Set-ExecutionPolicy Restricted

5. #### Now confirm the command after pressing enter to complete the operation.
