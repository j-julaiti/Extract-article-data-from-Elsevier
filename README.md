# Extract-article-data-from-Elsevier
This is an open source project using API from Elsevier to allow user download metadata of research articles.

Usage:
Step1: 

      Apply an Elsevier account and creat a APIKey under MyaAPI from:
      https://dev.elsevier.com/user/login
      
Step2:

    Clone the Repositories to some file

Step3:

    Open Jupyter notebook and open extract_elsevier.ipynb (or any python file editor and open extract_elsevier.py)

Step4:

    Setup the APIkey and querying keywords (defult is "queueing AND service interruption")

Step5:

    Run the code and explore the dataset
    In the end of the code, most of the data will be stored into a dataframe named "textdata".
    Addtionally, a full body of the paper will be in a new folder named with the time you ran the code
   
For version 1.0 the metadata contains:
1. Title
2. Authors
3. Abstract
4. Author provided keywords
5. Citation counts
6. Journal name
7. Journal type (book, Ebook, journal etc.)
8. Link to the paper
9. DOI (Digital object identifier)
10. Date of publication
11. Paper ID corresponding to the full body of the paper in the folder created based the time you ran the code
    
 
