#!pip install pandas
#!pip install numpy
#!pip install openpyxl
#!pip install pandas-datareader

### IMPORTING ESSENTIAL LIBRARIES ####
import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
import datetime as dt

pd.set_option('display.max_columns', None)   # to see all columns.
pd.set_option('display.max_rows', 20)   # limited to 20 rows max.

### GETTING THE DATESETS ####

## ford_tfp dataset.
ford = pd.read_csv("ford_tfp.csv")
# Separating the quarter column from the dot and replacing 0, 25, 50, 75 with Q1, Q2, Q3, Q4 respectively seems like the most practical solution.
ford["quarter"] = ford["quarter"].astype(str) # Since I needed to use a string method, I converted it to a string.
new= ford["quarter"].str.split(".", n=1, expand=True) # Dividing the quarter in a new dataframe
new["1"] = new.iloc[:, 1].map({"0":"Q1",    # I redefined them in a dictionary using map function.
                               "25":"Q2",
                               "5":"Q3",
                               "75":"Q4"})
ford["quarter"] = new[0]+new["1"]   # Converted as desired.
ford.rename(columns={"quarter":"DATE"}, inplace=True) # Renamed for subsequent operations.

## quarterly_tfp dataset.
# We get only the columns we need from the data set below. We leave out lines that contain information in the sheet with skiprows and skipfooter arguments.
fernald = pd.read_excel("quarterly_tfp.xlsx", sheet_name="quarterly", skiprows=1, skipfooter=6)[["date", "dtfp_util"]]
fernald["date"] = fernald["date"].str.replace(":", "", regex=True) # If we  skip the colon in between, the problem seems to be solved.
fernald.rename(columns={"date":"DATE"}, inplace=True) # Renamed for subsequent operations.

# the two dataset above are merged as a single dataframe on their DATE column. They are ready for further process.
ford = pd.merge(ford, fernald, on="DATE")

## FRED data
# I used pandas_datareader as recommended.
ticker = ["CNP16OV", "GDP", "GDPDEF", "HOANBS","PCE","PNFI"]    # The initials of the datasets we will get from the database
start = dt.datetime(1947, 1,1)  # The earliest date of all datasets
fred = pdr.get_data_fred(ticker, start) # I told the function what I wanted and from what date. It seems ready.

# CNP16OV and PCE are at a montly frequency. They will need to be converted to quarter.
# I would have preferred the last month's value for the stock variables but I followed the instructions here.
fredCNP16OV = fred.CNP16OV.resample('Q').mean().reset_index()   # Taking its mean at quarterly frequency and reset its index because of below proceeding.
fredCNP16OV["DATE"] = pd.PeriodIndex(fredCNP16OV.DATE, freq='Q') # I easy concerted it as quarterly

fredPCE = fred.PCE.resample('Q').mean().reset_index()   # The same applies here with CNP16OV.
fredPCE["DATE"] = pd.PeriodIndex(fredPCE.DATE, freq='Q')

# The below columns are at quarterly frequency.
fred = fred.loc[:,["GDP", "GDPDEF", "HOANBS","PNFI"]].reset_index()
fred["DATE"] = pd.PeriodIndex(fred.DATE, freq='Q')
fred.drop_duplicates(subset="DATE", keep="first", inplace=True) # I drop the rows which are null, so I have the dataset with same index with the dateset above.

# I merged fredPCE and fredCNP16OV on DATE.
fredPCE = pd.merge(fredPCE, fredCNP16OV, on="DATE")
fred = pd.merge(fred, fredPCE, on="DATE") # Merged seperetaly because of the nature of the merge funciton.
fred["DATE"] = fred["DATE"].astype(str) # Converted to string becasue merge function requires so.

dfs = pd.merge(fred, ford, on="DATE") # dfs is the final dataset that contains all variables.
dfs.set_index("DATE", inplace=True) # I used DATA as merge key until here. The set it as index.

### DATA PROCESSING ###

# As instructed at 1.
dfs["GDPpc"] = np.log((dfs["GDP"]/dfs["GDPDEF"])/dfs["CNP16OV"])*100
dfs["PCEpc"] = np.log((dfs["PCE"]/dfs["GDPDEF"])/dfs["CNP16OV"])*100
dfs["PNFIpc"] = np.log((dfs["PNFI"]/dfs["GDPDEF"])/dfs["CNP16OV"])*100

# As instructed at 2.
dfs["HOANBSpc"] = np.log(dfs["PNFI"]/dfs["CNP16OV"])*100

# As instructed at 3.
dfs["LABOR_PROD"] = np.log((dfs["GDP"]/dfs["HOANBS"])/dfs["GDPDEF"])*100

### LOCAl PROJECTIONS

# I citied this web sites for the proceddings below https://github.com/suahjl/localprojections
!pip install localprojections
import localprojections as lp

endog = ['LABOR_PROD','GDPpc',  'PCEpc', "PNFIpc"]      # Determining the endogenous variables
response = endog.copy() # We see the effect of the shocks to these variables
irf_horizon = 20 # As instructed IRFs have 20 periods
opt_lags = 2 # included 2 lags in the model as described in its mathematical form on the assignment.
opt_cov = 'robust' # HAC is used as instructed
opt_ci = 0.67 # 67% confidence intervals

# The belows are lagged variables.
dfs["lagGDPpc"] =dfs["GDPpc"].shift(-1)
dfs["lagLABOR_PROD"] =dfs["LABOR_PROD"].shift(-1)
dfs["lagPCEpc"] =dfs["PCEpc"].shift(-1)
dfs["lagPNFIpc"] =dfs["PNFIpc"].shift(-1)

## For the shock dtfp_util
# The following code runs the impulse response function.
irf = lp.TimeSeriesLP(data=dfs.loc[:, ['LABOR_PROD','GDPpc', 'PCEpc', "PNFIpc", "lagGDPpc", "lagLABOR_PROD", "lagPCEpc", "dtfp_util"]], # as input, only indicated variables in the mathematical form on the assignment paper.
                      Y=endog, # dependent variables in the model
                      response=response, # variables whose IRFs should be estimated
                      horizon=irf_horizon, # horizon
                      lags=opt_lags, # refers to lags
                      newey_lags=2, # refers to maximum lags when estimating Newey-West standard errors
                      ci_width=opt_ci # refers to confidence band
                      )

irfplot = lp.IRFPlot(irf=irf, # plot's input which we run above
                     response=['LABOR_PROD','GDPpc', 'PCEpc', "PNFIpc"],
                     shock=endog,
                     n_columns=4, # 4 columns in the figure
                     n_rows=4, # f rows in the figure
                     maintitle='dtfp_util', # the name of the shock, also the title of the figures.
                     show_fig=True, # display figure
                     save_pic=False # do not save automatically
                     )

# For the shock ford_tfp
irf = lp.TimeSeriesLP(data=dfs.loc[:, ['LABOR_PROD','GDPpc', 'PCEpc', "PNFIpc", "lagGDPpc", "lagLABOR_PROD", "lagPCEpc", "ford_tfp"]], # as input, only indicated variables in the mathematical form on the assignment paper
                      Y=endog, # dependent variables in the model
                      response=response, # variables whose IRFs should be estimated
                      horizon=irf_horizon, # horizon
                      lags=opt_lags, # refers to lags
                      newey_lags=2, # refers to maximum lags when estimating Newey-West standard errors
                      ci_width=opt_ci # width of confidence band
                      )

irfplot = lp.IRFPlot(irf=irf, # take output from the estimated model
                     response=['LABOR_PROD','GDPpc', 'PCEpc', "PNFIpc"],
                     shock=endog, # ... to shocks from all variables
                     n_columns=4, # max 2 columns in the figure
                     n_rows=4, # max 2 rows in the figure
                     maintitle="ford_tfp", # self-defined title of the IRF plot
                     show_fig=True, # display figure (from plotly)
                     save_pic=False # refers to confidence band
                     )
