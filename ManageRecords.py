import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Any

"""
datetime.datetime.strftime() : Use to format strings to datetime object (string -> datetime)
datetime.datetime.strptime() : Use to parse datetime object to string object  (datetime -> string)
--------- example ---------

>>> string = datetime.strptime(datetime.now().strftime('%d - %m - %Y'), '%d - %m - %Y')
>>> string
datetime.datetime(2024, 6, 16, 0, 0)
>>> type(string)
<class 'datetime.datetime'>
"""


"""
Method to build flet app (No need of any other libraries)
- pip install pyinstaller
- go to current working directory where file is stored eg. main.py
- flet pack main.py
"""

class ManageData:
    def __init__(self, path: str):
        self.path = path + r'\data.csv'
        self.file_exists = os.path.isfile(self.path)
        self.df = None

    def read_date_file(self) -> pd.DataFrame:
        if self.file_exists:
            df = pd.read_csv(self.path)
        else:
            with open('data.csv', mode='w') as file:
                file.write('customer_name,item_name,gross_price,net_price,profit,selling_date')

            df = pd.read_csv(self.path + '/data.csv')

        self.df = df
        # if len(self.df) > 0:
        #     self.df.selling_date = pd.to_datetime(self.df.selling_date)
        #     self.df.to_csv('./data.csv', index=False)

        return df

    def prepare_to_display(self):
        """Use to prepare record in a way that it easily display on screen with container"""
        pass

    def add_record(self, record: list[Any]):
        """
        Use to Append new record to the existing ones and If file is not created It will create fresh one with columns
        Record Must be Followed with below items as value :
        customer_name, item_name, gross_price, net_price, profit, selling_date
        """

        df = self.read_date_file()
        new_record: dict = {'customer_name': record[0],
                            'item_name': record[1],
                            'gross_price': record[2],
                            'net_price': record[3],
                            'profit': record[4],
                            'selling_date': record[5].strftime('%Y-%m-%d')}

        before_len = len(df)
        df.loc[len(df.index)] = new_record
        after_len = len(df)
        df.drop_duplicates(ignore_index=True, inplace=True)
        df.to_csv('./data.csv', index=False)
        self.df = df
        return 0 if before_len == after_len else 1

    def get_by_item_name(self, item_name_by_user: str) -> pd.DataFrame | bool:
        """Use to return results based on item names only"""
        self.read_date_file()
        # print(self.df)
        if len(self.df) == 0:
            return False
        else:
            items_filtered: pd.DataFrame = self.df[self.df.item_name.str.contains(item_name_by_user.lower()) |
                                                   self.df.item_name.str.contains(item_name_by_user.upper()) |
                                                   self.df.item_name.str.contains(item_name_by_user.capitalize())]
            if len(items_filtered) == 0:
                return False

            return items_filtered if len(items_filtered) != 0 else False

    def get_by_customer_name(self, customer_name_by_user: str) -> pd.DataFrame | bool:
        """Use to return results based on customer names only"""
        self.read_date_file()
        if len(self.df) == 0:
            print("No value available for customer name : ")
            return False
        else:
            names_filtered: pd.DataFrame = self.df[self.df.customer_name.str.contains(customer_name_by_user.lower()) |
                                                   self.df.customer_name.str.contains(customer_name_by_user.upper()) |
                                                   self.df.customer_name.str.contains(customer_name_by_user.capitalize()
                                                                                      )]
            return names_filtered if len(names_filtered) != 0 else False

    def get_by_month(self, month: int) -> pd.DataFrame | bool:
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            self.df.selling_date = pd.to_datetime(self.df.selling_date)
            # results = pd.Series([f'{x} of {x.month}' for x in self.df.selling_date.to_list()])
            results: pd.DataFrame | None = self.df[self.df.selling_date.dt.month == month]
            return results

    def get_by_profit(self, start_value: float, end_value: float) -> pd.DataFrame | bool:
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            profit_results = self.df[(self.df.profit >= start_value) & (self.df.profit <= end_value)]
            return profit_results if len(profit_results) != 0 else False

    def get_by_month_and_item(self, item: str, month: int):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            item_filter_only = self.get_by_item_name(item)
            if not isinstance(item_filter_only, bool):
                item_filter_only['selling_date'] = pd.to_datetime(item_filter_only['selling_date'])
                mix_filter: pd.DataFrame = item_filter_only[item_filter_only.selling_date.dt.month == month]
                return mix_filter if len(mix_filter) != 0 else False
            else:
                return False

    def get_by_month_and_cst(self, cst_name: str, month: int):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            cst_filter_only = self.get_by_customer_name(cst_name)
            if not isinstance(cst_filter_only, bool):
                cst_filter_only['selling_date'] = pd.to_datetime(cst_filter_only['selling_date'])
                mix_filter: pd.DataFrame = cst_filter_only[cst_filter_only.selling_date.dt.month == month]
                return mix_filter if len(mix_filter) != 0 else False
            else:
                return False

    def get_by_month_and_profit(self, profit_start: float, profit_end: float, month: int):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            profit_filter_only = self.get_by_profit(profit_start, profit_end)
            if not isinstance(profit_filter_only, bool):
                profit_filter_only['selling_date'] = pd.to_datetime(profit_filter_only['selling_date'])
                mix_filter: pd.DataFrame = profit_filter_only[profit_filter_only.selling_date.dt.month == month]
                return mix_filter if len(mix_filter) != 0 else False
            else:
                return False

    def get_by_item_and_cst(self, item_name: str, cst_name: str):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            item_and_cst = self.df[(self.df.customer_name.str.contains(cst_name.lower()) |
                                    self.df.customer_name.str.contains(cst_name.upper()) |
                                    self.df.customer_name.str.contains(cst_name.capitalize())) &
                                   (self.df.item_name.str.contains(item_name.lower()) |
                                    self.df.item_name.str.contains(item_name.upper()) |
                                    self.df.item_name.str.contains(item_name.capitalize()))]
            return item_and_cst if len(item_and_cst) != 0 else False

    def get_by_item_and_profit(self, item_name: str, profit_start: float, profit_end: float):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            item_and_profit = self.df[((self.df.profit >= profit_start) & (self.df.profit <= profit_end)) &
                                      (self.df.item_name.str.contains(item_name.lower()) |
                                       self.df.item_name.str.contains(item_name.upper()) |
                                       self.df.item_name.str.contains(item_name.capitalize()))]
            return item_and_profit if len(item_and_profit) != 0 else False

    def get_by_cst_and_profit(self, cst_name: str, profit_start: float, profit_end: float):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            cst_and_profit = self.df[((self.df.profit >= profit_start) & (self.df.profit <= profit_end)) &
                                     (self.df.customer_name.str.contains(cst_name.lower()) |
                                      self.df.customer_name.str.contains(cst_name.upper()) |
                                      self.df.customer_name.str.contains(cst_name.capitalize()))]
            return cst_and_profit if len(cst_and_profit) != 0 else False

    def get_by_all_filters(self, item_name: str, cst_name: str, profit_start: float, profit_end: float, month: int):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            all_filters = self.get_by_item_and_cst(item_name=item_name, cst_name=cst_name)
            print("After item and cst filters")
            print(all_filters)
            if not isinstance(all_filters, bool):
                all_filters['selling_date'] = pd.to_datetime(all_filters['selling_date'])
                all_filters: pd.DataFrame | None = all_filters[((all_filters.profit >= profit_start) &
                                                                (all_filters.profit <= profit_end)
                                                                ) &
                                                               (all_filters.selling_date.dt.month == month)]
                return all_filters if len(all_filters) != 0 else False
            else:
                return False

    def get_by_month_item_cst(self, item_name: str, cst_name: str, month: int):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            all_filters = self.get_by_item_and_cst(item_name=item_name, cst_name=cst_name)
            print("After item and cst filters")
            print(all_filters)
            if not isinstance(all_filters, bool):
                all_filters['selling_date'] = pd.to_datetime(all_filters['selling_date'])
                all_filters: pd.DataFrame | None = all_filters[all_filters.selling_date.dt.month == month]
                return all_filters if len(all_filters) != 0 else False
            else:
                return False

    def get_by_item_cst_profit(self, item_name: str, cst_name: str, profit_start: float, profit_end: float):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            all_filters = self.get_by_item_and_cst(item_name=item_name, cst_name=cst_name)
            print("After item and cst filters")
            print(all_filters)
            if not isinstance(all_filters, bool):
                all_filters: pd.DataFrame | None = all_filters[all_filters.profit.between(profit_start, profit_end)]
                return all_filters if len(all_filters) != 0 else False
            else:
                return False

    def get_by_month_cst_profit(self, cst_name: str, profit_start: float, profit_end: float, month: int):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            all_filters = self.get_by_month_and_cst(month=month, cst_name=cst_name)
            print("After month and cst filters")
            print(all_filters)
            if not isinstance(all_filters, bool):
                all_filters: pd.DataFrame | None = all_filters[all_filters.profit.between(profit_start, profit_end)]
                return all_filters if len(all_filters) != 0 else False
            else:
                return False

    def upd_filter_records(self, month: int, year: int) -> pd.DataFrame | None:
        """Use to return dataframe with filters and used for both operations Update and Delete"""

        self.read_date_file()
        self.df['selling_date'] = pd.to_datetime(self.df['selling_date'])

        today = datetime.now()
        year_mask = self.df['selling_date'].dt.year == year
        month_mask = self.df['selling_date'].dt.month == month
        month_mask_current_year = ((self.df['selling_date'].dt.month == today.month) &
                                   (self.df['selling_date'].dt.year == today.year))
        year_month_mask = (year_mask & month_mask)

        filtered_by_params = None
        if month != '-- Select --' and year != '-- Select --':
            filtered_by_params = self.df[year_month_mask]
        elif month == '-- Select --' and year != '-- Select --':
            filtered_by_params = self.df[year_mask]
        elif month != '-- Select --' and year == '-- Select --':
            filtered_by_params = self.df[month_mask]
        elif month == '-- Select --' and year == '-- Select --':
            filtered_by_params = self.df[month_mask_current_year]

        print(filtered_by_params)

        return filtered_by_params if filtered_by_params is not None else False

    def update_record(self, data: dict) -> bool:
        try:
            self.read_date_file()
            self.df['selling_date'] = pd.to_datetime(self.df['selling_date'])

            # Pop ID so that it can create a series based on df :
            index = data.pop('ID')
            data['selling_date'] = data['selling_date'].strftime('%Y-%m-%d')

            updated_series: pd.Series = pd.Series(data)
            self.df.iloc[index] = updated_series
            print(self.df.iloc[index])

            self.df.to_csv('./data.csv', index=False)
            return True

        except Exception:
            return False

    def delete_record(self, ids_to_drop: list[int] | int) -> bool:
        # Use to delete whole month record :
        self.read_date_file()
        if isinstance(ids_to_drop, list) and len(ids_to_drop) == 0:
            return False

        if isinstance(ids_to_drop, int | list):
            self.df.drop(ids_to_drop, axis=0, inplace=True)
            self.df.drop_duplicates(inplace=True, ignore_index=True)
            self.df.to_csv('./data.csv', index=False)
            return True

        return False

    def get_df_for_analysis(self) -> pd.DataFrame:
        return self.read_date_file()

    def get_plot(self, options: str):
        self.read_date_file()

        """
        'Profit over Customer',  [DONE]
        'Profit over Items',  [DONE]
        'Profit over Time (Month or Year)',  [DONE]
        'Profit Margins of Items (%)',  [DONE]
        'Top Items counts based on selling',  [DONE]
        'Regular Customer in Business'  [DONE]
        """

        fig, ax = plt.subplots(constrained_layout=True)
        if options is None or options == '-- Select --' or options == '':
            return None
        elif options == 'Profit over Customer':
            vis_df = self.df.groupby('customer_name')['profit'].sum().sort_values(ascending=False).reset_index().copy()
            if len(vis_df) >= 10:
                vis_df = vis_df.iloc[:10]
            labels: list[str] = ['\n'.join(i.split(' ', maxsplit=2)) if len(i) > 10 else i
                                 for i in vis_df['customer_name'].tolist()]
            bars = ax.bar(labels, vis_df['profit'])
            ax.bar_label(bars, padding=1)

            ax.set_ylabel("Profit (₹)")
            ax.set_xlabel("Customers")
            ax.set_title("Total Profit for Top 10 Customers")
            ax.set_ylim(0, vis_df['profit'].max() + 1000)
            ax.legend().remove()
            plt.xticks(rotation=30)
            plt.tight_layout()

        elif options == 'Profit over Items':
            vis_df = self.df.groupby('item_name')['profit'].sum().sort_values(ascending=False).reset_index().copy()
            labels: list[str] = ['\n'.join(i.split(' ', maxsplit=2)) if len(i) > 10 else i
                                 for i in vis_df['item_name'].tolist()]
            if len(vis_df) >= 10:
                vis_df = vis_df.iloc[:10]

            bars = ax.bar(labels, vis_df['profit'])
            ax.bar_label(bars, padding=1)
            ax.set_ylabel("Profit (₹)")
            ax.set_xlabel("Items")
            ax.set_title("Total Profit for Top 10 Items")
            ax.set_ylim(0, vis_df['profit'].max() + 1000)
            ax.legend().remove()
            plt.xticks(rotation=30)
            plt.tight_layout()

        elif options == 'Profit over Time (Month or Year)':
            periods = pd.to_datetime(self.df['selling_date']).dt.strftime('%Y-%m')
            my_df = self.df.copy()
            my_df['selling_date'] = periods.copy()
            my_df = my_df.groupby('selling_date').sum()['profit']  \
                                                 .reset_index()  \
                                                 .sort_values(by=['selling_date', 'profit'])

            bars = ax.bar(my_df['selling_date'].values.tolist(), my_df['profit'])
            ax.bar_label(bars, padding=1)
            ax.set_ylabel("Profit (₹)")
            ax.set_xlabel("Selling Date (YYYY-MM)")
            ax.set_title("Total Profit Over Time (YYYY-MM)")

            plt.xticks(rotation=30)
            plt.legend().remove()
            plt.bar_label(ax.containers[0])

        elif options == 'Profit Margin over Items (%)':
            # Profit Margin (%) :
            my_df = self.df.copy()
            my_df['profit_margin'] = my_df['profit'] / my_df['gross_price'] * 100
            labels: list[str] = ['\n'.join(i.split(' ', maxsplit=2)) if len(i) > 10 else i
                                 for i in my_df['item_name'].tolist()]
            # Plot profit margin by item
            ax.bar(labels, my_df['profit_margin'])
            ax.set_title('Profit Margin by Item')
            ax.set_xlabel('Item Name')
            ax.set_ylabel('Profit Margin (%)')
            plt.xticks(rotation=30)
            plt.tight_layout()

        elif options == 'Top Items counts based on selling':
            df1 = self.df['item_name'].value_counts(ascending=True).reset_index().copy()
            bars = df1.plot(kind='barh', x='item_name', y='count')
            plt.bar_label(bars.containers[0], padding=2)
            plt.legend().remove()
            plt.xlabel('Count')
            plt.ylabel('Item Name')
            plt.title('Top Items counts based on selling')
            plt.tight_layout()

        elif options == 'Regular Customer in Business':
            df1 = self.df['customer_name'].value_counts(ascending=True).reset_index().copy()
            bars = df1.plot(kind='barh', x='customer_name', y='count')
            plt.bar_label(bars.containers[0], padding=2)
            plt.legend().remove()
            plt.xlabel('Count')
            plt.ylabel('Customer Name')
            plt.title('Regular Customer Of All Time')
            plt.tight_layout()

        rand_int = random.randint(1, 1_00_000)
        plt.savefig(f'./assets/plot{rand_int}.png')
        return rand_int

