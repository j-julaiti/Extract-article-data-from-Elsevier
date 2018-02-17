# Extract-article-data-from-Elsevier
This is an open source project using API from Elsevier to allow user download metadata of research articles.

Usage:

Step1: 

      Apply an Elsevier account and creat a APIKey under MyAPI from (it's free):
      https://dev.elsevier.com/user/login
      
Step2:

    Clone the Repositories to a folder

Step3:

    Open Jupyter notebook and open extract_elsevier.ipynb (or any python file editor and open extract_elsevier.py)

Step4:

    Setup the APIkey and querying keywords (defult is "artificial intelligence")

Step5:

    Run the code and explore the dataset
    In the end of the code, most of the data will be stored into a dataframe named "textdata".
    Addtionally, a full body of the paper will be in a new folder named with the time you ran the code

Overall, the inputs are:

      1) Keywords to query the articles, 2) APIkeys from Elsevier
And the outpus have two parts:
      
      1) basic information of the papers in a dataframe, 2) full body of the paper (may not be always available)

For version 1.0 the basic information contains:
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
    
 
Note: the dataframe of the basic information is saved as a pickle file (extracted_data.p) since some cells contain a list, saving as a csv and reading it back will cause unneccessry process to recover them to lists.

The pickle file is also in the folder named with the time you ran the code.



Some network analysis based on the data is under developing.
