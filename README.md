
# bioinformatics


### [Optional]
It's will be safer to work in virtual environment.

In case you have Anaconda:

  Create a virtual environment using this command:

    conda create -n yourenvname python=3.5 anaconda
  
  Activate virtual environment:

    activate yourenvname
    
### Installation

Backend

cd to project_path (the folder that contains requirements.txt)

    pip install -r requirements.txt
    
Frontend

If you don't have Node.js installed in your system, you can download it here:
https://nodejs.org/en/

cd to project_path/static

    npm install -g bower
    bower install
    
### Start program
    python manage.py runserver

