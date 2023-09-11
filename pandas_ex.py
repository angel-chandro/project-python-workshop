# import our modules
import sqlite3
import pandas as pd

# connect to the database
con = sqlite3.connect('portal_mammals.sqlite')

# execute a query and save the results to a dataframe
surveys_df = pd.read_sql("SELECT * FROM surveys", con)
