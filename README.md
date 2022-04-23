# Triad-GiveOne

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Jewel-CC/Triad-GiveOne/)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Deployed application: https://giveone.herokuapp.com/

The application is deployed and live, however, there are errors preventing it from working normally 100% of the time. That is, sometimes it works as it supposed to but sometimes it does not. However, this only happens on the deployed verison, running the application locally through a "flask run" command in the termal of VSCode shows the application working perfectly 100% of the time, the gitpod workspace is also up and working. 

Steps on how to run the application locally (through VSCode):

1. Download the repository as a zip.
2. Extract the files from the zip to a folder of your choice.
3. Open VSCode and click "File" in the menu then "Open Folder" then navigate to the folder that has the application. 
4. In the terminal, run the command "flask run" (NOTE: If you do have the requirements installed, please do "pip install -r requirements.txt in the terminal)
5. (Users may login with the credentials Username: bob, Passowrd: bobpass)

Steps on how to deploy the application via heroku:
1. After creating a profile on Heroku, create a new app.
2. Navigate to Settings, click on Reveal Config Vars and add the following:
      - ENV:Production
      - JWTDELTADAYS:14
      - SECRET_KEY:"Key of your choice"
      - SQLITEDB:False
3. Go to resources, search and find Heroku Postgres and submit the form to create a Postgres Database for your app
4. Back in the application, inside the create_app() function in app.py, replace the app.config lines with:
      - app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') 
      - app.config['SQLITEDB'] = False 
      - app.config['SECRET_KEY'] = "SECRET" 
      - app.config['JWT_EXPIRATION_DELTA'] = 7 
5. To deploy using the heroku CLI do the following within your terminal:
      - heroku login 
      - heroku git:clone -a "your app name"  
      - cd "your app name" 
      - git add . 
      - git commit -am "message" 
      - git push heroku main 
      
      
