
# bioinformatics

### Requirement
python 3.5 or Anaconda

### Installation
Since this project contains many large files, it is recommend to clone this project into your external disk.

After finish cloning, download database files and tools via the following link:

https://engcu-my.sharepoint.com/personal/57306355_eng_chula_ac_th/_layouts/15/guestaccess.aspx?folderid=0c63b28a49bff427b8eece3ee2333a6bc&authkey=ARXBfu6nn1Cki3pbddnf4gU

Put "data" folder into "tools/Exomizer" and put the other files into "database"

It will be safer to work in virtual environment.

In case you have Anaconda:

  Create a virtual environment using this command:

    conda create -n bioinformatics python=3.5 anaconda
  
  Activate virtual environment:

    activate bioinformatics

cd to project_path (the folder that contains requirements.txt)

    pip install -r requirements.txt
    
    
### Start program
Note: Make sure that you are in virtual environment before starting the program (if you want to use virtual environment)

    python manage.py runserver

