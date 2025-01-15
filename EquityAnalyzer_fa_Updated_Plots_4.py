# Equity Analyzer
# Importing necessary libraries and Dependencies
import streamlit as st
import pandas as pd
import datetime
import math
import yfinance as yf
import FundamentalAnalysis as fa
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pandas import DataFrame


# Defining the api key for FundamentalAnalysis package
api_key = "e397a9f256fbe6f05d2281aa2eae2496"

#Plotting of financial statements
# Graph Function
def financial_statement_chart(chart, data, categories):
    if chart:
        chosen_category = st.selectbox("Select the metric you want to analyze", categories)
        if chosen_category:
            category_df = data.loc[chosen_category].values
            year = data.loc["fillingDate"].values
            chart = px.bar(x=year, y=category_df, text=category_df, color=year,
                           labels={"x":"Year", "y": chosen_category})
            chart.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            st.plotly_chart(figure_or_data=chart)


# Waterfall Chart Function
def fs_wf_chart(fig, data_1, Year_lst):
    if fig:
        year_selection = st.selectbox("Select Year", Year_lst)
        if year_selection:
            data_1[["revenue","costOfRevenue","grossProfit","researchAndDevelopmentExpenses","generalAndAdministrativeExpenses","sellingAndMarketingExpenses","otherExpenses","operatingExpenses","costAndExpenses","interestExpense","depreciationAndAmortization","ebitda","operatingIncome","totalOtherIncomeExpensesNet","incomeBeforeTax","incomeTaxExpense","netIncome"]] = data_1[["revenue","costOfRevenue","grossProfit","researchAndDevelopmentExpenses","generalAndAdministrativeExpenses","sellingAndMarketingExpenses","otherExpenses","operatingExpenses","costAndExpenses","interestExpense","depreciationAndAmortization","ebitda","operatingIncome","totalOtherIncomeExpensesNet","incomeBeforeTax","incomeTaxExpense","netIncome"]].apply(pd.to_numeric)
            data_1 = data_1[data_1.Year == year_selection]
            Revenue = data_1.iloc[0][1]
            COGS = data_1.iloc[0][2]*(-1)
            grossProfit = data_1.iloc[0][3]
            RND = data_1.iloc[0][4]*(-1)
            GAE = data_1.iloc[0][5]*(-1)
            SME = data_1.iloc[0][6]*(-1)
            OTE = data_1.iloc[0][7]*(-1)
            OPE = data_1.iloc[0][8]*(-1)
            CAE = data_1.iloc[0][9]*(-1)
            IE = data_1.iloc[0][10]*(-1)
            DEPR = data_1.iloc[0][11]*(-1)
            EBT = data_1.iloc[0][12]
            OI = data_1.iloc[0][13]*(-1)
            OINET = data_1.iloc[0][14]
            incbTax = data_1.iloc[0][15]
            TaxE = data_1.iloc[0][16]
            netIncome = data_1.iloc[0][17]
            fig = go.Figure(go.Waterfall(
                name = "20", orientation = "v",

                measure = ["relative", "relative", "total", "relative", "relative", "relative", "relative", "relative", "relative", "relative","relative", "total", "relative", "total", "relative", "relative","total"],

                x = ["revenue","costOfRevenue","grossProfit","researchAndDevelopmentExpenses","generalAndAdministrativeExpenses","sellingAndMarketingExpenses","otherExpenses","operatingExpenses","costAndExpenses","interestExpense","depreciationAndAmortization","ebitda","operatingIncome","totalOtherIncomeExpensesNet","incomeBeforeTax","incomeTaxExpense","netIncome"],

                textposition = "outside",

                #text = [Revenue/100000, COGS/100000, grossProfit/100000, RD/100000, GA/1000000, operatingExpenses/1000000,interest/100000, EBT/100000,incTax/100000, netIncome/100000],

                y = [Revenue, COGS, grossProfit, RND, GAE, SME, OTE, OPE, CAE, IE, DEPR, EBT, OI, OINET, incbTax, TaxE, netIncome],

                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))

            fig.update_layout(
                    title = "Profit and loss statement",
                    showlegend = True
            )
            st.plotly_chart(figure_or_data=fig)












# Get Compnay Information from yfinance Package
@st.cache
def get_company_info(stock):
    company_dict = yf.Ticker(stock).info
    return company_dict

# Income Statement Function - Was getting some mutable error while using @st.cache
def company_income_statement(stock):
    company_is = fa.income_statement(stock,api_key,period="annual")
    return company_is

# Balance Sheet Function
def company_balance_sheet(stock):
    company_bs = fa.balance_sheet_statement(stock,api_key,period="annual")
    return company_bs

# Cash Flow Satement Function
def company_cash_flow(stock):
    company_cf = fa.cash_flow_statement(stock,api_key,period="annual")
    return company_cf



# Fundamental Analysis Block
# Show all company list from S&P 500 Sector  and Industry Classification
def FundamentalAnalysis():
    image_8 = Image.open('Word_Cloud_3.jpeg')
    st.image(image_8,use_column_width=True)
    df = pd.read_csv('SP500_list.csv')
    st.title("Fundamental Analysis")
    equity_sector = sorted(df["Sector"].unique().tolist())
    sector = st.selectbox("Select Sector", equity_sector)
    stock = st.sidebar.text_input("Enter Symbol", value="")
    stock_lst = df[df.Sector == sector]
    st.write(f"Sector : {sector}")
# Note: I have to add a condition here where stock !=stock_lst

    if stock == "":
        st.table(stock_lst[["Symbol","Name"]].reset_index(drop=True))
    else:
        company_info = get_company_info(f"{stock}")
        st.write(f"Company Name : {company_info['longName']}")
        st.write(f"Industry : {company_info['industry']}")
        business_summary = st.checkbox("Business Summary")
        if business_summary:
            st.write(company_info['longBusinessSummary'])
        contact_info = st.checkbox("Contact Information")
        if contact_info:
            st.write(f"City: {company_info['city']}")
            st.write(f"Phone: {company_info['phone']}")
            st.write(f"Website: {company_info['website']}")

        st.sidebar.header("Financial Statements")
        Financials_1 = st.sidebar.checkbox("Income Statement")

        if Financials_1:
            st.header(f"Income Statement")
            company_is = company_income_statement(stock)
            st.dataframe(company_is)
            data = company_is
            data.drop(["reportedCurrency"], inplace=True)
            data.drop(["acceptedDate"], inplace=True)
            data.drop(["period"], inplace=True)
            data.drop(["link"], inplace=True)
            data.drop(["finalLink"], inplace=True)
            cols = data.select_dtypes(exclude='int').columns.to_list()
            data[cols] = data[cols].astype('str')
            data = data.replace(['None',"0",0], np.nan).dropna(how='all')
            categories = data.index.to_list()
            categories.remove("fillingDate")
            chart = st.checkbox("Visualize Income Statement")
            financial_statement_chart(chart, data, categories)



            # Waterfall Chart
            # Dropping unnecessary columns from the Data Frame
            #company_is.drop(["reportedCurrency"], inplace=True)
            #company_is.drop(["acceptedDate"], inplace=True)
            #company_is.drop(["period"], inplace=True)
            company_is.drop(["grossProfitRatio"], inplace=True)
            company_is.drop(["ebitdaratio"], inplace=True)
            company_is.drop(["operatingIncomeRatio"], inplace=True)
            company_is.drop(["fillingDate"], inplace=True)
            company_is.drop(["incomeBeforeTaxRatio"], inplace=True)
            company_is.drop(["netIncomeRatio"], inplace=True)
            company_is.drop(["eps"], inplace=True)
            company_is.drop(["epsdiluted"], inplace=True)
            company_is.drop(["weightedAverageShsOut"], inplace=True)
            company_is.drop(["weightedAverageShsOutDil"], inplace=True)
            #company_is.drop(["link"], inplace=True)
            #company_is.drop(["finalLink"], inplace=True)

            # Preprocessing data
            # Making a list of Year for Selection Box
            Year_lst = company_is.columns.to_list()
            # Making a lis of metric for later use
            Metric = company_is.index.to_list()

            # Transpose the Original Data - company_is

            data_T = company_is.T

            # Adding an Index column at the end of the transposed data set

            data_T['Index_Column'] = range(1,len(data_T)+1)

            # Setting the added last column as the Index Column

            data_T = data_T.set_index('Index_Column')

            # Converting Year_lst to a data frame to be added to the data frame

            df = DataFrame(Year_lst,columns=['Year'])

            # Adding Index column to the above data frame for merging with Original transposed data frame
            df['Index_Column'] = range(1,len(df)+1)

            df = df.set_index('Index_Column')

            # Merging two data sets - Transposed and the Year Data frame
            data_1 = pd.merge(df, data_T, left_index=True, right_index=True)

            # Visualize Waterfall Chart option
            fig = st.checkbox("Visualize Income Statement for a Year in Waterfall Chart")
            fs_wf_chart(fig, data_1, Year_lst)




            # Streamlit Functions
            #year_selection = st.selectbox("Select Year", Year_lst)

            #wf_data = data_1[data_1.Year == year_selection]

            #st.table(wf_data[["Year","revenue"]].reset_index(drop=True))



        Financials_2 = st.sidebar.checkbox("Balance Sheet")

        if Financials_2:
            st.header(f"Balance Sheet")
            company_bs = company_balance_sheet(stock)
            st.dataframe(company_bs)
            data = company_bs
            data.drop(["reportedCurrency"], inplace=True)
            data.drop(["acceptedDate"], inplace=True)
            data.drop(["period"], inplace=True)
            data.drop(["link"], inplace=True)
            data.drop(["finalLink"], inplace=True)
            cols = data.select_dtypes(exclude='int').columns.to_list()
            data[cols] = data[cols].astype('str')
            data = data.replace(['None',"0",0], np.nan).dropna(how='all')
            categories = data.index.to_list()
            categories.remove("fillingDate")
            chart = st.checkbox("Visualize Balance Sheet Items")
            financial_statement_chart(chart, data, categories)

        Financials_3 = st.sidebar.checkbox("Cash Flow Statement")

        if Financials_3:
            st.header(f"Cash Flow Statement")
            company_cf = company_cash_flow(stock)
            st.dataframe(company_cf)
            data = company_cf
            data.drop(["reportedCurrency"], inplace=True)
            data.drop(["acceptedDate"], inplace=True)
            data.drop(["period"], inplace=True)
            data.drop(["link"], inplace=True)
            data.drop(["finalLink"], inplace=True)
            cols = data.select_dtypes(exclude='int').columns.to_list()
            data[cols] = data[cols].astype('str')
            data = data.replace(['None',"0",0], np.nan).dropna(how='all')
            categories = data.index.to_list()
            categories.remove("fillingDate")
            chart = st.checkbox("Visualize Cash Flow Statement Items")
            financial_statement_chart(chart, data, categories)









# Home Page Block
# Application Description in the main home page
def home():
    st.header("Equity Analyzer")
    image_1 = Image.open('Stock_3.jpeg')
    st.image(image_1,use_column_width=True)
    st.markdown(
        f"""
            Welcome to the Equity Analyzer. This is an Application for performing
            comprehnsive analysis of a particular stock. The application will provide
            real time Insight on a particular stock, associated industry and its peers
            to aid investment decisions. The Insight
            is generated leveraging both traditional and alternative data. Please use
            the drop down on the left hand side menu to perform the follwoing analysis
            mentioned below. Each analyss will provde addtional capabilities to generate
            user frindly reports to help investment decision.

            * Fundamental Analysis
            * Technical Analysis
            * Portfolio / Investment Optimisation
            * Correlation / Industry Analysis
            * Peer Comparison Analysis
            * Macroeconomic Indicators
            * News Sentiment, Call Report and 10 Q/K Analysis

        """
    )

# Main Application Block
# Side bar option functionality
def app():
    image_5 = Image.open('Stock_5.jpeg')
    st.sidebar.image(image_5, caption='', use_column_width=True)
    st.sidebar.title("Navigation")
    stock_element = st.sidebar.selectbox(
        "Choose a Type of Analysis",
        [
            "Home",
            "Fundamental Analysis",
            "Technical Analysis",
            "Portfolio / Investment Optimisation",
            "Correlation / Industry Analysis",
            "Peer Comparison Analysis",
            "Macro Indicators",
            "News Sentiment, Call Report and 10 Q/K Analysis"
        ],
    )

    if stock_element == "Home":
        home()

    if stock_element == "Fundamental Analysis":
        FundamentalAnalysis()




app()
