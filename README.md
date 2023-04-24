# Local-Projection-Approach
I used local projection approach to explore the response of some core macroeconomic variables to changes in total factor productivity (two different measured shocks: FORD TFP shocks,  Fernald TFP shocks.)

**Overview**

This project uses the local projection approach to explore the response of some core macroeconomic variables to changes in total factor productivity (TFP). The analysis is based on data obtained from the Federal Reserve Economic Data (FRED) repository. The project focuses on two different measured shocks: FORD TFP shocks and Fernald TFP shocks.

**Data**

The data used in this project is sourced from the Federal Reserve Economic Data repository (FRED) maintained by the Federal Reserve Bank of St. Louis. The following series were downloaded from the FRED database:

Civilian Noninstitutional Population (CNP16OV)
Gross Domestic Product (GDP)
GDP Deflator (GDPDEF)
Hours (HOANBS)
Consumption (PCE)
Non-Residential Investment (PNFI)

**Local Projection**

The effects of the TFP shocks, denoted as ε, were measured using local projection regressions following Jorda (2005). For each variable z and each horizon h, a linear regression was run as follows:

![Screen Shot 2023-04-24 at 11 40 39](https://user-images.githubusercontent.com/94282435/234047164-96d0d0fe-39c9-45e6-a5fb-ff885934ec96.png)


In this regression, the dependent variable z is regressed on the current value of the shock and two lags, the lagged value of the dependent variable (zt−1) and a vector of lagged control variables (Xt−1). The term ut,t+h is the regression residual. It is important to note that this regression must be run separately for each horizon of interest h.

**Results**

The results of the local projection analysis show the response of each of the core macroeconomic variables to the FORD TFP shocks and Fernald TFP shocks. The analysis provides valuable insights into how changes in TFP affect the economy and its components. The results are presented in the form of charts and tables, which make it easy to interpret and visualize the findings.


![Outout IRF (ford_tfp)](https://user-images.githubusercontent.com/94282435/233797075-21d1af3b-3f3b-44bb-a9d5-8c1c3f817e98.png)

![Output IRF (dtfp_util)](https://user-images.githubusercontent.com/94282435/233797079-33689c93-d0f5-4771-b810-3a4d219ce529.png)


**Conclusion**

This project demonstrates the use of the local projection approach to analyze the response of core macroeconomic variables to TFP shocks. The results show that changes in TFP have significant effects on the economy and its components. The project provides a useful framework for understanding the dynamics of the economy and its response to different shocks.

--
JORDA, O. (2005): “Estimation and Inference of Impulse Responses by Local Projections”, American Economic Review, 161–182.




