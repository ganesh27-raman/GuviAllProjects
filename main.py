import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class StockAnalysis:
    def __init__(self, csv_folder, sector_file, output_folder):
        self.csv_folder = csv_folder
        self.sector_file = sector_file
        self.output_folder = output_folder

    def read_stock_data(self, file):
        stock_data = pd.read_csv(os.path.join(self.csv_folder, file))
        if 'date' not in stock_data.columns:
            print(f"File {file} is missing 'date' column. Available columns: {stock_data.columns}")
            return None
        if 'close' not in stock_data.columns:
            print(f"File {file} is missing 'close' column.")
            return None
        
        stock_data['date'] = pd.to_datetime(stock_data['date'], errors='coerce')
        stock_data.set_index('date', inplace=True)
        return stock_data


    def calculate_volatility(self):
        st.header("Stock Volatility Analysis")
        files = [f for f in os.listdir(self.csv_folder) if f.endswith('.csv')]
        volatility_data = {}

        for file in files:
            stock_data = self.read_stock_data(file)
            if stock_data is None:
                continue
            stock_data['Daily_Return'] = stock_data['close'].pct_change()
            stock_data['Volatility'] = stock_data['Daily_Return'].rolling(window=30).std() * np.sqrt(252)
            stock_symbol = file.split('.')[0]
            volatility_data[stock_symbol] = stock_data['Volatility'].iloc[-1]

        volatility_df = pd.DataFrame(list(volatility_data.items()), columns=['Stock', 'Volatility'])
        volatility_df = volatility_df.sort_values(by='Volatility', ascending=False)
        output_file = os.path.join(self.output_folder, "nifty_50_volatility.csv")
        volatility_df.to_csv(output_file, index=False)
        input_result = st.number_input("Enter the number of stocks to display:", min_value=1, max_value=len(volatility_df), value=10)
        top_result = volatility_df.head(input_result)
        # plt.figure(figsize=(14, 7))
        # plt.bar(top_10['Stock'], top_10['Volatility'], color='orange')
        # plt.title("Volatility of Nifty 50's Top 10 Stocks")
        # plt.xlabel('Annualized Volatility')
        # plt.ylabel('Stock Symbol')
        # plt.xticks(rotation=45)
        # plt.show()

        fig, ax = plt.subplots(figsize=(14, 7))
        ax.bar(top_result['Stock'], top_result['Volatility'], color='orange')
        ax.set_title("Volatility of Nifty 50's Top 10 Stocks")
        ax.set_xlabel('Stock Symbol')
        ax.set_ylabel('Annualized Volatility')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)


    def calculate_cumulative(self):
        st.header("Stock Cummulative Analysis")
        files = [f for f in os.listdir(self.csv_folder) if f.endswith('.csv')]
        cumulative_returns_data = {}

        for file in files:
            stock_data = self.read_stock_data(file)
            if stock_data is None:
                continue
            stock_data['Daily_Return'] = stock_data['close'].pct_change()
            stock_data['Cumulative_Return'] = (1 + stock_data['Daily_Return']).cumprod() - 1
            stock_symbol = file.split('.')[0]
            cumulative_returns_data[stock_symbol] = stock_data['Cumulative_Return'].iloc[-1]

        cumulative_returns_data_df = pd.DataFrame(list(cumulative_returns_data.items()), columns=['Stock', 'Cumulative'])
        cumulative_returns_data_df = cumulative_returns_data_df.sort_values(by='Cumulative', ascending=False)
        output_file = os.path.join(self.output_folder, "nifty_50_cumulative.csv")
        cumulative_returns_data_df.to_csv(output_file, index=False)
        input_result = st.number_input("Enter the number of stocks to display:", min_value=1, max_value=len(cumulative_returns_data_df), value=5)
        top_result = cumulative_returns_data_df.head(input_result)
        #top_5 = cumulative_returns_data_df.head(5)
        # plt.figure(figsize=(14, 7))
        # plt.bar(top_5['Stock'], top_5['Cumulative'], color='orange')
        # plt.title("Cumulative of Nifty 50's Top 5 Stocks")
        # plt.xlabel('Annualized Cumulative')
        # plt.ylabel('Stock Symbol')
        # plt.xticks(rotation=45)
        # plt.show()

        fig, ax = plt.subplots(figsize=(14, 7))
        ax.bar(top_result['Stock'], top_result['Cumulative'], color='orange')
        ax.set_title("Cumulative of Nifty 50's Top 5 Stocks")
        ax.set_xlabel('Stock Symbol')
        ax.set_ylabel('Annualized Cumulative')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    def calculate_sectorwise(self):
        st.header("Sectorwise Analysis")
        if not self.sector_file:
            print("Sector file not provided.")
            return

        sector_data = pd.read_csv(self.sector_file)
        files = [f for f in os.listdir(self.csv_folder) if f.endswith('.csv')]
        sectorwise_returns_data = []

        for file in files:
            stock_name = file.split('.')[0]
            matched_sectors = sector_data[sector_data['Symbol'].str[:2] == stock_name[:2]]
            if matched_sectors.empty:
                print(f"Skipping file {file} due to missing sector data")
                continue

            stock_data = self.read_stock_data(file)
            if stock_data is None:
                continue

            start_price = stock_data['close'].iloc[0]
            end_price = stock_data['close'].iloc[-1]
            sectorwise_returns = ((end_price - start_price) / start_price)
            sector = matched_sectors['sector'].iloc[0]
            sectorwise_returns_data.append({
                'Stock': stock_name,
                'Sector': sector,
                'Yearly_Return': sectorwise_returns
            })

        sectorwise_returns_df = pd.DataFrame(sectorwise_returns_data)
        avg_sectorwise_returns = sectorwise_returns_df.groupby('Sector')['Yearly_Return'].mean().reset_index()
        avg_sectorwise_returns = avg_sectorwise_returns.sort_values(by='Yearly_Return', ascending=False)
        output_file = os.path.join(self.output_folder, "nifty_50_avg_sectorwise.csv")
        avg_sectorwise_returns.to_csv(output_file, index=False)


        input_result = st.number_input("Enter the number of stocks to display:", min_value=1, max_value=len(avg_sectorwise_returns), value=5)
        top_result = avg_sectorwise_returns.head(input_result)
        #top_5 = avg_sectorwise_returns.head(5)
        # plt.figure(figsize=(14, 7))
        # plt.bar(top_result['Sector'], top_result['Yearly_Return'], color='orange')
        # plt.title("Top 5 Sectors by Yearly Return")
        # plt.xlabel('Sector')
        # plt.ylabel('Yearly Return')
        # plt.xticks(rotation=45)
        # plt.show()

        fig, ax = plt.subplots(figsize=(14, 7))
        ax.bar(top_result['Sector'], top_result['Yearly_Return'], color='orange')
        ax.set_title("Top 5 Sectors by Yearly Return")
        ax.set_xlabel('Sector')
        ax.set_ylabel('Yearly Return')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)


    def calculate_correlation(self):
        st.header("Monthly Gainers and Losers Analysis")
        files = [f for f in os.listdir(self.csv_folder) if f.endswith('.csv')]

        #selected_stocks = st.text_input("Search for a stock symbol:", "")

        selected_stocks = st.multiselect(
        "Select Stocks for Correlation Analysis:",
        options=[f.split('.')[0] for f in files if f.endswith('.csv')], help="Choose one or more stocks to calculate correlation.")
        
        if not selected_stocks:
            st.warning("Please select at least one stock to proceed.")
            return

        correlation_returns_data = {}
        for file in files:
            stock_name = file.split('.')[0]
            if selected_stocks and stock_name not in selected_stocks:
                continue

            stock_data = self.read_stock_data(file)
            if stock_data is None:
                continue

            correlation_returns_data[stock_name] = stock_data['close'].values

        if not correlation_returns_data:
            st.warning("No data available for selected stocks.")
            return

        stock_df_combined = pd.DataFrame(correlation_returns_data)
        correlation_matrix = stock_df_combined.corr()


        # plt.figure(figsize=(14, 10))
        # sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
        # plt.title("Stock Price Correlation Heatmap")
        # plt.xticks(rotation=45, ha='right')
        # plt.yticks(rotation=0)
        # plt.tight_layout()
        # plt.show()

        fig, ax = plt.subplots(figsize=(14, 10))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax)
        ax.set_title("Stock Price Correlation Heatmap")
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        st.pyplot(fig)

    def calculate_monthly_gainers_losers(self):
        st.header("Stock Correlation Analysis")
        files = [f for f in os.listdir(self.csv_folder) if f.endswith('.csv')]
        all_stock_data = {}

        for file in files:
            stock_name = file.split('.')[0]
            stock_data = self.read_stock_data(file)

            monthly_data = stock_data['close'].resample('ME').last()  # Monthly closing price

            monthly_return = monthly_data.pct_change() * 100
            all_stock_data[stock_name] = monthly_return


        monthly_returns_df = pd.DataFrame(all_stock_data)

        if monthly_returns_df.empty:
            print("No data available for plotting.")
            return

        months = monthly_returns_df.index
        num_months = len(months)
        num_rows = (num_months + 5) // 6

        fig, axes = plt.subplots(num_rows, 6, figsize=(20, 10))
        axes = axes.flatten()

        for i, month in enumerate(months):
            month_data = monthly_returns_df.loc[month]      
            gainers = month_data.nlargest(5)
            losers = month_data.nsmallest(5) 

            gainers_losers_df = pd.DataFrame({
                'Gainers': gainers,
                'Losers': losers
            })
            output_file = os.path.join(self.output_folder, f"{month.strftime('%Y_%m')}_gainers_losers.csv")
            gainers_losers_df.to_csv(output_file)

            # axes[i].bar(gainers.index, gainers.values, color='green', label='Top Gainers')
            # axes[i].bar(losers.index, losers.values, color='red', label='Top Losers')

            # axes[i].set_title(f'Month: {month.strftime("%b %Y")}')
            # axes[i].set_xlabel('Stocks')
            # axes[i].set_ylabel('Percentage Return')
            # axes[i].tick_params(axis='x', rotation=45)
            # axes[i].legend()

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(gainers.index, gainers.values, color='green', label='Top Gainers')
            ax.bar(losers.index, losers.values, color='red', label='Top Losers')
            ax.set_title(f"Gainers and Losers for {month.strftime('%B %Y')}")
            ax.set_xlabel('Stock')
            ax.set_ylabel('Percentage Return')
            ax.tick_params(axis='x', rotation=45)
            ax.legend()
            st.pyplot(fig)


    def run_analysis(self):

        st.sidebar.header("Stock Analysis Dashboard")
        options = ["Volatility Analysis", "Cumulative Return Analysis", "Sectorwise Return Analysis", "Stock Correlation Analysis", "Monthly Gainers and Losers"]
        choice = st.sidebar.selectbox("Select Analysis", options)

        if choice == 'Volatility Analysis':
            self.calculate_volatility()
        elif choice == 'Cumulative Return Analysis':
            self.calculate_cumulative()
        elif choice == 'Sectorwise Return Analysis':
            self.calculate_sectorwise()
            
        elif choice == 'Stock Correlation Analysis':
            self.calculate_correlation()
        elif choice == 'Monthly Gainers and Losers':
            self.calculate_monthly_gainers_losers()
        else:
            print("Invalid choice. Please try again.")

# Example usage
csv_folder = "C:/Users/ganes/Documents/DataScienceLearnings/Guvi/Project_2 Data-Driven Stock Analysis/Input/Data-20241230T123422Z-001/Data_csv_Combined"
sector_file = "C:/Users/ganes/Documents/DataScienceLearnings/Guvi/Project_2 Data-Driven Stock Analysis/Input/Data-20241230T123422Z-001/Data/sector.csv"
output_folder = "C:/Users/ganes/Documents/DataScienceLearnings/Guvi/Project_2 Data-Driven Stock Analysis/Input/Data-20241230T123422Z-001/results"
obj = StockAnalysis(csv_folder, sector_file, output_folder)
obj.run_analysis()