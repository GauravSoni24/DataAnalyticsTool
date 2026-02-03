# Python in built in libraries :
import os
from typing import Any
from types import NoneType
from colorama import Fore

# Data analysis libraries :
from pandas._libs.tslibs.parsing import DateParseError
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# GUI Libraries :
import flet as ft
from flet import (Text, ElevatedButton, TextField, MainAxisAlignment, CrossAxisAlignment, Tabs, Tab, TabAlignment, Row,
                  Column, icons, Container, Switch, ControlEvent, ThemeMode, DatePicker, colors, IconButton, Icon,
                  AlertDialog, Dropdown, Divider, DataTable, DataCell, DataColumn, DataRow, border, FilePicker,
                  VerticalDivider, Image, Chip)


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
        return df

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

        print(new_record['selling_date'])

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
                cst_filter_only.loc[: ,'selling_date'] = pd.to_datetime(cst_filter_only['selling_date'])
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
                profit_filter_only.loc[:, 'selling_date'] = pd.to_datetime(profit_filter_only['selling_date'])
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

    def get_by_month_item_profit(self, month: int, item: str, profit_start: float, profit_end: float):
        self.read_date_file()
        if len(self.df) == 0:
            return False
        else:
            all_filters = self.get_by_month_and_item(month=month, item=item)
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
            labels: list[str] = ['\n'.join(i.split(' ', maxsplit=2)) if len(i) > 10 else i
                                 for i in vis_df['customer_name'].tolist()]

            if len(vis_df) >= 10:
                vis_df = vis_df.iloc[:10]
                labels = labels[:10]

            bars = ax.bar(labels, vis_df['profit'])
            ax.bar_label(bars, padding=1)

            ax.set_ylabel("Profit (₹)")
            ax.set_xlabel("Customers")
            ax.set_title("Total Profit for Top 10 Customers")
            ax.set_ylim(0, vis_df['profit'].max() + 1000)
            ax.legend().remove()
            plt.xticks(rotation=45)
            plt.tight_layout()

        elif options == 'Profit over Items':
            vis_df = self.df.groupby('item_name')['profit'].sum().sort_values(ascending=False).reset_index().copy()
            labels: list[str] = ['\n'.join(i.split(' ', maxsplit=2)) if len(i) > 10 else i
                                 for i in vis_df['item_name'].tolist()]
            if len(vis_df) >= 12:
                vis_df = vis_df.iloc[:12]
                labels = labels[:12]

            bars = ax.bar(labels, vis_df['profit'])
            ax.bar_label(bars, padding=1)
            ax.set_ylabel("Profit (₹)")
            ax.set_xlabel("Items")
            ax.set_title("Total Profit for Top 10 Items")
            ax.set_ylim(0, vis_df['profit'].max() + 1000)
            ax.legend().remove()
            plt.xticks(rotation=45, fontsize=8 if len(vis_df) >= 12 else 10)
            plt.tight_layout()

        elif options == 'Profit over Time (Month or Year)':
            periods = pd.to_datetime(self.df['selling_date']).dt.strftime('%Y-%m')
            my_df = self.df.copy()
            my_df['selling_date'] = periods.copy()
            my_df = my_df.groupby('selling_date').sum()['profit'] \
                .reset_index() \
                .sort_values(by=['selling_date', 'profit'])

            if len(my_df) >= 12:
                my_df['selling_date'] = pd.to_datetime(my_df['selling_date'])
                my_df['selling_date'] = my_df['selling_date'].dt.strftime('%Y')
                my_df = my_df.groupby('selling_date').sum()['profit'] \
                    .reset_index() \
                    .sort_values(by=['selling_date', 'profit'])

            labels: list[str] = [i for i in my_df['selling_date'].tolist()]
            bars = ax.bar(labels, my_df['profit'])
            ax.bar_label(bars, padding=1)
            ax.set_ylabel("Profit (₹)")
            ax.set_xlabel("Selling Date (YYYY-MM) / (YYYY)")
            ax.set_title("Total Profit Over Time")

            plt.xticks(rotation=45)
            plt.legend().remove()
            plt.tight_layout()

        elif options == 'Profit Margin over Items (%)':
            # Profit Margin (%) :
            my_df = self.df.copy()
            my_df['profit_margin'] = my_df['profit'] / my_df['gross_price'] * 100
            my_df = my_df.sort_values(by='profit_margin', ascending=False).copy()
            labels: list[str] = ['\n'.join(i.split(' ', maxsplit=1)) if len(i) > 10 else i
                                 for i in my_df['item_name'].tolist()]

            # Plot profit margin by item
            ax.bar(labels, my_df['profit_margin'])
            ax.set_title('Profit Margin by Item')
            ax.set_xlabel('Item Name')
            ax.set_ylabel('Profit Margin (%)')
            plt.xticks(rotation=45, fontsize=8 if len(my_df) >= 10 else 13)
            plt.tight_layout()

        elif options == 'Top Items counts based on selling':
            df1 = self.df['item_name'].value_counts().reset_index().copy()
            if len(df1) >= 17:
                df1 = df1[:16].copy()

            bars = df1.plot(kind='barh', x='item_name', y='count')
            plt.bar_label(bars.containers[0], padding=2)
            plt.legend().remove()
            plt.xlabel('Count')
            plt.ylabel('Item Name')
            plt.title('Top Items counts based on selling')
            plt.tight_layout()

        elif options == 'Regular Customer in Business':
            df1 = self.df['customer_name'].value_counts().reset_index().copy()
            if len(df1) >= 17:
                df1 = df1[:16].copy()

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


def main(page: ft.Page):
    page.window_maximized = True
    page.theme_mode = ThemeMode.DARK
    md: ManageData = ManageData(os.getcwd())
    page.title = "Business Product By Gaurav Soni"

    # page.theme = ft.theme.Theme(color_scheme_seed="blue")  # To set themes

    # Change Page theme to Dark / Light :
    def change_theme(e: ControlEvent):
        # Add Record Widgets :
        page.theme_mode = ThemeMode.DARK if dark_light_switch.value else ThemeMode.LIGHT
        cst_name.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        item_name.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        gross_price.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        net_price.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        date_text.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        customer_name_table.border = border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        item_name_table.border = border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')

        # Display Widgets :
        dsp_cst_name.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        dsp_item_name.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        drop_down_month.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        divider.color = colors.WHITE if page.theme_mode == ThemeMode.DARK else colors.BLACK
        searched_results.border = border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        searched_results.vertical_lines = border.BorderSide(1,
                                                            'white' if page.theme_mode == ThemeMode.DARK else 'black')
        searched_results.horizontal_lines = border.BorderSide(1,
                                                              'white' if page.theme_mode == ThemeMode.DARK else 'black')

        # Update Widgets :
        upd_divider.color = colors.WHITE if page.theme_mode == ThemeMode.DARK else colors.BLACK
        upd_month.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        upd_year.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        upd_record_table.border = border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        upd_record_table.vertical_lines = border.BorderSide(1,
                                                            'white' if page.theme_mode == ThemeMode.DARK else 'black')
        upd_record_table.horizontal_lines = border.BorderSide(1,
                                                              'white' if page.theme_mode == ThemeMode.DARK else 'black')
        upd_cst_input.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        upd_item_input.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        upd_gross_input.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        upd_net_input.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        upd_date_text.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        upd_update_form.border = ft.border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')

        # Analytics Widgets:
        categories.border_color = colors.BLUE_200 if page.theme_mode == ThemeMode.DARK else colors.BLACK
        describe_datatable.border = border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        describe_datatable.vertical_lines = border.BorderSide(1,
                                                              'white' if page.theme_mode == ThemeMode.DARK else 'black')
        describe_datatable.horizontal_lines = border.BorderSide(1,
                                                                'white' if page.theme_mode == ThemeMode.DARK else 'black')

        item_per_month.border = border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        item_per_month.vertical_lines = border.BorderSide(1, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        item_per_month.horizontal_lines = border.BorderSide(1,
                                                            'white' if page.theme_mode == ThemeMode.DARK else 'black')

        top_5_items.border = border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        top_5_items.vertical_lines = border.BorderSide(1, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        top_5_items.horizontal_lines = border.BorderSide(1, 'white' if page.theme_mode == ThemeMode.DARK else 'black')

        top_5_cst.border = border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        top_5_cst.vertical_lines = border.BorderSide(1, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        top_5_cst.horizontal_lines = border.BorderSide(1, 'white' if page.theme_mode == ThemeMode.DARK else 'black')

        profit_by_cst.border = border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        profit_by_cst.vertical_lines = border.BorderSide(1, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        profit_by_cst.horizontal_lines = border.BorderSide(1, 'white' if page.theme_mode == ThemeMode.DARK else 'black')

        profit_by_item.border = border.all(2, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        profit_by_item.vertical_lines = border.BorderSide(1, 'white' if page.theme_mode == ThemeMode.DARK else 'black')
        profit_by_item.horizontal_lines = border.BorderSide(1,
                                                            'white' if page.theme_mode == ThemeMode.DARK else 'black')
        divider_analytics.color = colors.WHITE if page.theme_mode == ThemeMode.DARK else colors.BLACK
        img_container.border = border.all(0, colors.WHITE)
        page.update()

    # Main Tab Switch For Theme :
    dark_light_switch: Switch = Switch(label="Dark Theme", value=True,
                                       on_change=change_theme)

    # ------------------------------- Add Record Widgets and Alerts ------------------------------- #
    def change_date(e: ControlEvent):
        # date_picker.pick_date()
        date_text.value = date_picker.value
        date_text.update()

    def submit_records(e: ControlEvent):
        """Validate Records and add to the CSV files"""

        # All fields must not be empty :
        has_empty_fields = all([cst_name.value == '',
                                item_name.value == '',
                                gross_price.value == '',
                                net_price.value == '',
                                date_text.value == ''])

        # Digits not allowed in names (Customer Name and Item Name) :
        has_names_strings = all([not cst_name.value.isdigit(), not item_name.value.isdigit()])

        # Gross Price and Net Price must not have strings
        has_prices_digits = all([gross_price.value.isdigit(), net_price.value.isdigit()])

        # Date Part should be correct :
        is_date = type(date_text.value) is datetime

        if not has_empty_fields and has_names_strings and has_prices_digits and is_date:
            # md: ManageData = ManageData(os.getcwd())
            profit: float = float(gross_price.value) - float(net_price.value)
            all_correct = md.add_record(record=[cst_name.value,
                                                item_name.value,
                                                float(gross_price.value),
                                                float(net_price.value),
                                                profit,
                                                date_text.value])

            if all_correct:
                print(Fore.GREEN + 'New Record added to the Data' + Fore.RESET)
                page.dialog = success_message
                success_message.open = True

                # Refreshing unique records of customer and item datatable :
                mydf: pd.DataFrame = md.read_date_file()
                customers: list = pd.Series(mydf['customer_name'].unique()).sort_values().tolist().copy()
                items: list = pd.Series(mydf['item_name'].unique()).sort_values().tolist().copy()

                cst_len = len(customers)
                item_len = len(items)
                if cst_len > item_len:
                    for _ in range(cst_len - item_len):
                        items.extend('-')
                elif cst_len < item_len:
                    for _ in range(item_len - cst_len):
                        customers.extend('-')

                customer_name_table.rows.clear()
                item_name_table.rows.clear()

                for i in customers:
                    customer_name_table.rows.append(
                        DataRow(cells=[DataCell(Text(i), on_tap=lambda _: copy_cst_cell(e))])
                    )

                for j in items:
                    item_name_table.rows.append(
                        DataRow(cells=[DataCell(Text(j), on_tap=lambda _: copy_item_cell(e))])
                    )

                add_main_column.scroll_to(offset=-1, duration=500)

                page.update()
                reset_records(e)

            else:
                # If data not correctly entered
                page.dialog = incorrect_add_record_error
                incorrect_add_record_error.open = True
                page.update()

        else:
            # Show Warning that shows error message
            page.dialog = add_record_error
            add_record_error.open = True
            page.update()

    def reset_records(e: ControlEvent):
        cst_name.value = ''
        item_name.value = ''
        gross_price.value = ''
        net_price.value = ''
        date_text.value = ''
        date_picker.value = ''
        page.update()

    # Inputs :
    cst_name: TextField = TextField(label="Customer Name", width=500,
                                    border_color=colors.BLUE_200)
    item_name: TextField = TextField(label="Item Name", width=500,
                                     border_color=colors.BLUE_200)
    gross_price: TextField = TextField(label="Gross (Total) Price of Item", width=500,
                                       border_color=colors.BLUE_200, prefix_text="₹ ")
    net_price: TextField = TextField(label="Net Price of Item", width=500,
                                     border_color=colors.BLUE_200, prefix_text="₹ ")
    date_picker: DatePicker = DatePicker(on_change=change_date)
    date_text: TextField = TextField(label="Selected Date",
                                     border_color=colors.BLUE_200)
    pick_icon_up: IconButton = IconButton(icon=icons.CALENDAR_MONTH,
                                          on_click=lambda _: date_picker.pick_date())
    submit_btn: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.ADD_ROUNDED),
                                                                      Text("Add Records")],
                                                            height=45),
                                                on_click=submit_records)
    reset_btn: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.REPEAT_ROUNDED),
                                                                     Text("Reset Input Fields")],
                                                           height=45),
                                               on_click=reset_records)

    def pickup_file(e: ft.FilePickerResultEvent):
        # Varify source and validate whether all values are having correct format as data.csv or not :

        file = e.files[0]
        if file.path.endswith('.csv'):
            path = file.path
            df = pd.read_csv(path)
            check_1: bool = df.columns.tolist() == ['customer_name', 'item_name',
                                                    'gross_price', 'net_price',
                                                    'profit', 'selling_date']
            check_2: bool = len(df) > 0
            check_3: bool = not df.isna().any().values.any()

            try:
                df['selling_date'] = pd.to_datetime(df['selling_date'])
                check_4: bool = True
            except (ValueError, pd._libs.tslibs.parsing.DateParseError):
                check_4 = False

            if check_1 and check_2 and check_3 and check_4:
                main_df = md.get_df_for_analysis()
                new_df = pd.concat([main_df, df], ignore_index=True).drop_duplicates()

                # Converting datetime intp str and pass it as datetime to normalize :
                new_df['selling_date'] = pd.to_datetime(new_df['selling_date'].astype(str).str.strip(' 00:00:00'))
                new_df.to_csv('./data.csv', index=False)

                page.dialog = bulk_success_alert
                bulk_success_alert.open = True
            else:
                page.dialog = invalid_file_data
                invalid_file_data.open = True

        page.update()

    add_bulk_records: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.ADD_ROUNDED),
                                                                            Text("Add Bulk Records")],
                                                                  height=45),
                                                      on_click=lambda _: picker.pick_files(allowed_extensions=['csv'],
                                                                                           dialog_title="Pickup csv "
                                                                                                        "file"
                                                                                                        " from desired "
                                                                                                        "folder",
                                                                                           allow_multiple=False))

    picker: FilePicker = FilePicker(pickup_file)

    # Invalid Alert :
    invalid_file_data: AlertDialog = AlertDialog(open=False,
                                                 title=Text("Warning"),
                                                 content=Row(controls=[
                                                     Icon(name=icons.REPORT_GMAILERRORRED, color=colors.RED, size=35),
                                                     Text("File's data are invalid to processed further\n"
                                                          ", Try to change file data. "
                                                          "(eg. Change YYYY-MM-DD format for selling_date column)",
                                                          size=20)],
                                                     width=900)
                                                 )

    bulk_success_alert: AlertDialog = AlertDialog(
        open=False,
        title=Text("Successfully Data Stored", size=22),
        content=Row(controls=[Icon(name=icons.CHECK_CIRCLE_ROUNDED, color=colors.GREEN, size=35),
                              Text("New Records Successfully Stored, \n"
                                   "You can now check \'Search Records\' tab", size=19)])
    )

    # Field Validation Error :
    add_record_error: AlertDialog = AlertDialog(
        open=False,
        title=Text("Warning"),
        content=Row(controls=[Icon(name=icons.REPORT_GMAILERRORRED, color=colors.RED, size=35),
                              Text("Some input fields has incorrect value or empty, Try to correct it", size=20)],
                    width=900)
    )

    # Data not added to the file Error :
    incorrect_add_record_error: AlertDialog = AlertDialog(
        open=False,
        title=Text("Warning"),
        content=Row(controls=[Icon(name=icons.REPORT_GMAILERRORRED, color=colors.RED, size=35),
                              Text("Data validated before but not added to the file yet (Contact Gaurav To Solve)",
                                   size=20)],
                    width=900),
    )

    # Successfully added to the file Message :
    success_message: AlertDialog = AlertDialog(
        open=False,
        title=Text("Successfully Data Stored"),
        content=Row(controls=[Icon(name=icons.CHECK_CIRCLE_ROUNDED, color=colors.GREEN, size=35),
                              Text("New Record Successfully Stored, "
                                   "You can now add new record here or display record")])
    )

    # Customer name list and Item name list DataTable :
    def copy_cst_cell(e: ControlEvent):
        cst_name.value = e.control.content.value
        add_main_column.scroll_to(offset=0, duration=100)
        page.update()

    def copy_item_cell(e: ControlEvent):
        item_name.value = e.control.content.value
        add_main_column.scroll_to(offset=0, duration=100)
        page.update()

    df: pd.DataFrame = md.read_date_file()
    unique_customers: list = pd.Series(df['customer_name'].unique()).sort_values().tolist().copy()
    unique_items: list = pd.Series(df['item_name'].unique()).sort_values().tolist().copy()

    cst_len = len(unique_customers)
    item_len = len(unique_items)
    if cst_len > item_len:
        for _ in range(cst_len - item_len):
            unique_items.extend('-')
    elif cst_len < item_len:
        for _ in range(item_len - cst_len):
            unique_customers.extend('-')

    customer_name_table = DataTable(
        columns=[
            DataColumn(Text("Customer name", weight=ft.FontWeight.BOLD)),
        ],
        rows=[
            DataRow(cells=[DataCell(Text(i), on_tap=copy_cst_cell)]) for i in unique_customers
        ],
        border=border.all(2, "white"),
        vertical_lines=ft.border.BorderSide(1, "white"),
        horizontal_lines=ft.border.BorderSide(1, "white")
    )

    item_name_table = DataTable(
        columns=[
            DataColumn(Text("Item name", weight=ft.FontWeight.BOLD)),
        ],
        rows=[
            DataRow(cells=[DataCell(Text(i), on_tap=copy_item_cell)]) for i in unique_items
        ],
        border=border.all(2, "white"),
        vertical_lines=ft.border.BorderSide(1, "white"),
        horizontal_lines=ft.border.BorderSide(1, "white")
    )

    add_main_column: Column = Column(controls=[
        Row(controls=[cst_name], alignment=MainAxisAlignment.CENTER, run_spacing=20),
        Row(controls=[item_name], alignment=MainAxisAlignment.CENTER),
        Row(controls=[gross_price], alignment=MainAxisAlignment.CENTER),
        Row(controls=[net_price], alignment=MainAxisAlignment.CENTER),
        Row(controls=[date_text, pick_icon_up], alignment=MainAxisAlignment.CENTER, spacing=20),
        Container(content=Row(controls=[submit_btn, reset_btn, add_bulk_records],
                              alignment=MainAxisAlignment.CENTER, spacing=20),
                  margin=10),
        Container(content=Row(controls=[
                            Text('Click below mentioned existing Customer Name and/or \n'
                                 'Item Name to add to the Add Record form.', size=23, weight=ft.FontWeight.BOLD)
                            ], alignment=MainAxisAlignment.CENTER),
                  margin=ft.margin.only(top=25)),
        Container(content=Row(controls=[customer_name_table, item_name_table],
                              alignment=MainAxisAlignment.CENTER, spacing=20),
                  margin=10),
    ], alignment=MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS)

    # Add Record Main container :
    add_record_main: Container = Container(content=add_main_column, margin=20)

    # ------------------------------- Search Record Widgets and Alerts ------------------------------- #
    def set_slider_text(e):
        min_value = profit_slider.start_value
        max_value = profit_slider.end_value
        slider_text.visible = True
        slider_text.value = (f"Range Selected \n"
                             f"Minimum Value : {min_value} & "
                             f"Maximum Value : {max_value}")
        page.update()

    def reset_input_fields(e):
        profit_slider.start_value = 80
        profit_slider.end_value = 200
        dsp_cst_name.value = ''
        dsp_item_name.value = ''
        drop_down_month.value = "-- Select --"
        slider_text.value = ''
        reset_datatable(e)
        page.update()

    def reset_datatable(k):
        searched_results.rows.clear()
        total_profit_chip.label = Text("Total Profit : ₹ 0.0", weight=ft.FontWeight.BOLD)
        searched_results.rows.append(
            DataRow(cells=[
                DataCell(Text("No results found")),
                DataCell(Text("No results found")),
                DataCell(Text("No results found")),
                DataCell(Text("No results found")),
                DataCell(Text("No results found")),
                DataCell(Text("No results found")),
                DataCell(Text("No results found"))
            ])
        )
        page.update()

    def search_record(e):
        month: int | str = drop_down_month.value
        month = int(month) if month.isdigit() else month
        item: str = dsp_item_name.value
        customer: str = dsp_cst_name.value
        range_start: float = float(profit_slider.start_value)
        range_end: float = float(profit_slider.end_value)

        # Field combinations:
        # All fields are empty -> (Error) (Covered under fields validations)
        # All fields are filled with some value -> (df)
        # Any one field has value -> (df)
        # ('Month', 'Item')
        # ('Month', 'Customer')
        # ('Month', 'Profit_Range')
        # ('Item', 'Customer')
        # ('Item', 'Profit_Range')
        # ('Customer', 'Profit_Range')
        # ('Month', 'Item', 'Customer')
        # ('Month', 'Customer', 'Profit')
        # ('Item', 'Customer', 'Profit')
        # ('Item', 'Month', 'Profit')

        all_empty: bool = (month == '-- Select --' and item == '' and customer == '' and 80 == range_start
                           and 200 == range_end)
        get_by_all_filters: bool = (month != '-- Select --' and item != "" and customer != "")

        get_by_item_only: bool = (month == '-- Select --' and item != "" and customer == "" and 80 == range_start
                                  and 200 == range_end)
        get_by_cst_name_only: bool = (month == '-- Select --' and item == "" and customer != "" and 80 == range_start
                                      and 200 == range_end)
        get_by_month_only: bool = (month != '-- Select --' and item == "" and customer == "" and 80 == range_start
                                   and 200 == range_end)
        get_by_profit_only: bool = (month == '-- Select --' and item == "" and customer == "")

        get_by_month_item: bool = (month != '-- Select --' and item != "" and customer == "" and 80 == range_start
                                   and 200 == range_end)
        get_by_month_cst: bool = (month != '-- Select --' and item == "" and customer != "" and 80 == range_start
                                  and 200 == range_end)
        get_by_month_profit: bool = (month != '-- Select --' and item == "" and customer == "")

        get_by_item_cst: bool = (month == '-- Select --' and item != "" and customer != "" and 80 == range_start
                                 and 200 == range_end)
        get_by_item_profit: bool = (month == '-- Select --' and item != "" and customer == "")

        get_by_cst_profit: bool = (month == '-- Select --' and item == "" and customer != "")

        get_by_month_item_cst: bool = (month != '-- Select --' and item != "" and customer != "" and 80 == range_start
                                       and 200 == range_end)

        get_by_item_cst_profit: bool = (month == '-- Select --' and item != "" and customer != "")

        get_by_month_cst_profit: bool = (month != '-- Select --' and item == "" and customer != "")

        get_by_month_item_profit: bool = (month != '-- Select --' and item != '')

        results: pd.DataFrame | None = None
        if all_empty:
            reset_datatable(e)
            # show_warning(e)
            print("All fields are empty, show error Message here.")
        elif get_by_item_only:
            results = md.get_by_item_name(item)
            print("Only Items are available")
        elif get_by_cst_name_only:
            results = md.get_by_customer_name(customer)
            print("Only Customers are available")
        elif get_by_month_only:
            results = md.get_by_month(month)
            print("Only Month are available")
        elif get_by_profit_only:
            results = md.get_by_profit(range_start, range_end)
        elif get_by_month_item:
            results = md.get_by_month_and_item(item=item, month=month)
        elif get_by_month_cst:
            results = md.get_by_month_and_cst(cst_name=customer, month=month)
        elif get_by_month_profit:
            results = md.get_by_month_and_profit(range_start, range_end, month)
        elif get_by_item_cst:
            results = md.get_by_item_and_cst(item, customer)
        elif get_by_item_profit:
            results = md.get_by_item_and_profit(item, range_start, range_end)
        elif get_by_cst_profit:
            results = md.get_by_cst_and_profit(customer, range_start, range_end)
        elif get_by_month_item_cst:
            results = md.get_by_month_item_cst(month=month, item_name=item, cst_name=customer)
        elif get_by_item_cst_profit:
            results = md.get_by_item_cst_profit(item_name=item, cst_name=customer,
                                                profit_start=range_start, profit_end=range_end)
        elif get_by_month_cst_profit:
            results = md.get_by_month_cst_profit(month=month, cst_name=customer,
                                                 profit_start=range_start, profit_end=range_end)
        elif get_by_month_item_profit:
            results = md.get_by_month_item_profit(month=month, item=item,
                                                  profit_start=range_start,
                                                  profit_end=range_end)
        else:
            if get_by_all_filters:
                results = md.get_by_all_filters(item_name=item,
                                                cst_name=customer,
                                                profit_start=range_start,
                                                profit_end=range_end,
                                                month=month)
                print("All fields are filled")
            else:
                print(Fore.RED + "Unusual fields input or results from python pandas" + Fore.RESET)

        # Update DataTable :
        if not isinstance(results, bool) and not isinstance(results, NoneType) and len(results) > 0:
            print(results)
            searched_results.rows.clear()
            results.loc[:, 'selling_date'] = pd.to_datetime(results['selling_date'])
            for index, each in results.iterrows():
                # print(each)
                searched_results.rows.append(
                    DataRow(cells=[DataCell(Text(index)),
                                   DataCell(Text(each['customer_name'])),
                                   DataCell(Text(each['item_name'])),
                                   DataCell(Text(each['gross_price'])),
                                   DataCell(Text(each['net_price'])),
                                   DataCell(Text(each['profit'])),
                                   DataCell(Text(each['selling_date'].strftime('%d-%m-%Y')))
                                   ])
                )
            total_profit_chip.label = Text("Total Profit : ₹ " + results['profit'].sum().round(2).astype(str),
                                           weight=ft.FontWeight.BOLD)
        else:
            reset_datatable(e)
        page.update()

    drop_down_month: Dropdown = Dropdown(width=500,
                                         label="Choose Month",
                                         options=[ft.dropdown.Option("-- Select --"),
                                                  *[ft.dropdown.Option(str(i)) for i in range(1, 13)]],
                                         border_color=colors.BLUE_200, on_change=search_record)

    drop_down_month.value = "-- Select --"

    dsp_item_name: TextField = TextField(label="Item Name", width=500,
                                         prefix_icon=icons.SHOPPING_CART,
                                         border_color=colors.BLUE_200, on_change=search_record)

    dsp_cst_name: TextField = TextField(label="Customer Name", width=500,
                                        prefix_icon=icons.PERSON_SEARCH,
                                        border_color=colors.BLUE_200, on_change=search_record)

    profit_slider = ft.RangeSlider(
        width=500,
        min=0,
        max=1500,
        start_value=80,
        divisions=int(1500 / 10),
        end_value=200,
        label="₹ {value}",
        on_change_end=set_slider_text,
        on_change=search_record,
        tooltip="Choose Profit range where you will find records available for your customer data for better targeting"
    )

    reset_slider_btn: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.REPEAT_ROUNDED),
                                                                            Text("Reset Input Fields")],
                                                                  height=45),
                                                      tooltip="Reset Input Fields",
                                                      on_click=reset_input_fields)

    slider_text: Text = Text(visible=False, width=600, weight=ft.FontWeight.BOLD, size=20)

    divider: Divider = Divider(height=5, color=colors.WHITE)

    searched_results = DataTable(
        columns=[
            DataColumn(Text("ID", weight=ft.FontWeight.BOLD)),
            DataColumn(Text("Customer name", weight=ft.FontWeight.BOLD)),
            DataColumn(Text("Item name", weight=ft.FontWeight.BOLD)),
            DataColumn(Text("Gross Price (₹)", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Net Price (₹)", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Profit (₹)", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Selling Date \n(DD-MM-YYYY)", weight=ft.FontWeight.BOLD))
        ],
        rows=[
            DataRow(
                cells=[
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found"))
                ],
            )
        ],
        border=border.all(2, "white"),
        vertical_lines=ft.border.BorderSide(1, "white"),
        horizontal_lines=ft.border.BorderSide(1, "white")
    )

    total_profit_chip: Chip = Chip(
        label=Text('Total Profit : ₹ 0.0', weight=ft.FontWeight.BOLD),
        on_select=lambda e: page.update(),
        border_side=ft.BorderSide(10, colors.LIGHT_BLUE),
    )

    # Display Record Main Container :
    search_record_main: Container = Container(content=Column(controls=[
        Row(controls=[drop_down_month], alignment=MainAxisAlignment.CENTER),
        Row(controls=[dsp_item_name], alignment=MainAxisAlignment.CENTER),
        Row(controls=[dsp_cst_name], alignment=MainAxisAlignment.CENTER),
        Row(controls=[Text("Select Profit Range :", width=200, size=20, weight=ft.FontWeight.BOLD),
                      profit_slider], alignment=MainAxisAlignment.CENTER),
        Row(controls=[slider_text], alignment=MainAxisAlignment.CENTER),
        Row(controls=[reset_slider_btn], alignment=MainAxisAlignment.CENTER),
        divider,
        Row(controls=[searched_results], alignment=MainAxisAlignment.CENTER),
        Row(controls=[total_profit_chip], alignment=MainAxisAlignment.CENTER),
    ], alignment=MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS), margin=20, padding=20)

    # -------------------------------------- Update / Delete Records -------------------------------------- #
    def get_records(e):
        year = upd_year.value
        year = int(year) if year.isdigit() else year
        month = upd_month.value
        month = int(month) if month.isdigit() else month
        results = md.upd_filter_records(month, year)

        if not isinstance(results, bool) and len(results) > 0:
            upd_record_table.rows.clear()
            results.loc[:, 'selling_date'] = pd.to_datetime(results['selling_date'])
            for index, each in results.iterrows():
                upd_record_table.rows.append(
                    DataRow(cells=[DataCell(Text(index)),
                                   DataCell(Text(each['customer_name'])),
                                   DataCell(Text(each['item_name'])),
                                   DataCell(Text(each['gross_price'])),
                                   DataCell(Text(each['net_price'])),
                                   DataCell(Text(each['profit'])),
                                   DataCell(Text(each['selling_date'].strftime('%d-%m-%Y')))
                                   ],
                            on_select_changed=show_update_delete_btn_one_record)
                )

            # update total profit :
            analytics_total_profit_chip.label = Text("Total Profit : ₹ " + results['profit'].sum().round(2).astype(str),
                                                     weight=ft.FontWeight.BOLD)

        else:
            upd_record_table.rows.clear()
            upd_delete_btn.visible = False
            upd_update_btn.visible = False
            upd_update_form.visible = False
            upd_record_table.rows.append(
                DataRow(cells=[
                    DataCell(Text('No results found')),
                    DataCell(Text('No results found')),
                    DataCell(Text('No results found')),
                    DataCell(Text('No results found')),
                    DataCell(Text('No results found')),
                    DataCell(Text('No results found')),
                    DataCell(Text('No results found'))
                ])
            )
            analytics_total_profit_chip.label = Text("Total Profit : ₹ 0.0", weight=ft.FontWeight.BOLD)

        page.update()

    deleted_alert: AlertDialog = AlertDialog(
        open=False,
        title=Text("Successfully Data Deleted"),
        content=Row(controls=[Icon(name=icons.CHECK_CIRCLE_ROUNDED, color=colors.GREEN, size=35),
                              Text("Selected Rows Successfully Deleted, "
                                   "You can now add new record here or display record", size=22)])
    )

    upd_month: Dropdown = Dropdown(label="Choose Month",
                                   options=[ft.dropdown.Option("-- Select --"),
                                            *[ft.dropdown.Option(str(i)) for i in range(1, 13)]],
                                   border_color=colors.BLUE_200,
                                   value='-- Select --')

    upd_year: Dropdown = Dropdown(label="Choose Year",
                                  options=[ft.dropdown.Option("-- Select --"),
                                           *[ft.dropdown.Option(str(i)) for i in range(2024, 2050)]],
                                  border_color=colors.BLUE_200,
                                  value='-- Select --')

    upd_search_record_btn: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.FIND_IN_PAGE_OUTLINED),
                                                                                 Text("Find Records")],
                                                                       height=45),
                                                           on_click=get_records)

    upd_divider: Divider = Divider(height=5, color=colors.WHITE)

    def deleted_successfully(e):
        page.dialog = deleted_alert
        deleted_alert.open = True
        get_records(e)
        upd_record_table.on_select_all = all_show_delete_btn
        upd_delete_btn.on_click = delete_all_rows
        upd_delete_btn.visible = False
        upd_update_btn.visible = False
        upd_update_form.visible = False
        page.update()

    def delete_all_rows(e: ControlEvent):
        """Use to delete all records which are filtered out by month and/or year"""

        ids_to_drop: list[int] = [i.cells[0].content.value for i in upd_record_table.rows]
        is_dropped = md.delete_record(ids_to_drop)
        if is_dropped:
            print("Successfully Records deleted :", ids_to_drop)
            deleted_successfully(e)
        page.update()

    def all_show_delete_btn(e):
        for i in upd_record_table.rows:
            i: DataRow
            i.selected = not i.selected

        if all([i.selected for i in upd_record_table.rows]):
            upd_delete_btn.visible = True
            upd_update_btn.visible = False
        elif not all([i.selected for i in upd_record_table.rows]):
            upd_update_form.visible = False
            upd_delete_btn.visible = False
            upd_update_btn.visible = False

        page.update()

    def show_update_delete_btn_one_record(e: ControlEvent):
        e.control.selected = not e.control.selected
        upd_delete_btn.visible = e.control.selected
        upd_update_btn.visible = e.control.selected

        if not any([i.selected for i in upd_record_table.rows]):
            upd_update_form.visible = False

        if e.control.selected:
            upd_delete_btn.on_click = lambda _: deleted_one_record(e, e.control.cells[0].content.value)

        page.update()

        upd_dlt_main_column.scroll_to(offset=-1, duration=100)

    def deleted_one_record(e: ControlEvent, index: int):
        is_deleted = md.delete_record(index)
        if is_deleted:
            deleted_successfully(e)
            page.update()
        print(index, ": deleted 😏")

    def update_success(e: ControlEvent):
        page.dialog = update_success_msg
        update_success_msg.open = True
        upd_update_form.visible = False
        upd_update_btn.visible = False
        upd_delete_btn.visible = False

        for i in upd_record_table.rows:
            if i.selected:
                i.selected = False

        get_records(e)
        page.update()

    def update_failed(e: ControlEvent):
        page.dialog = update_failed_msg
        update_failed_msg.open = True
        upd_update_form.visible = False

        for i in upd_record_table.rows:
            if i.selected:
                i.selected = False

        get_records(e)
        show_update_form(e)
        page.update()

    def show_update_form(e: ControlEvent):
        upd_update_form.visible = True
        for each in upd_record_table.rows:
            if each.selected:
                # print([i.content.value for i in each.cells])

                # Update form values as in selected row :
                upd_cst_input.value = each.cells[1].content.value
                upd_item_input.value = each.cells[2].content.value
                upd_gross_input.value = each.cells[3].content.value
                upd_net_input.value = each.cells[4].content.value
                upd_date_text.value = datetime.strptime(each.cells[6].content.value, '%d-%m-%Y')
                break

        upd_dlt_main_column.scroll_to(offset=-1, duration=100)

        page.update()

    def update_record(e: ControlEvent):
        """Get records from form and update record at respected index in df : """
        customer = str(upd_cst_input.value)
        item = str(upd_item_input.value)
        gross = str(upd_gross_input.value)
        net = str(upd_net_input.value)
        selling_date = upd_date_text.value

        def is_float(value):
            try:
                float(value)
                return True
            except ValueError:
                return False

        # All fields must not be empty :
        has_empty_fields = all([customer == '',
                                item == '',
                                gross == '',
                                net == '',
                                selling_date == ''])

        # Digits not allowed in names (Customer Name and Item Name) :
        has_names_strings: bool = not customer.isdigit() and not item.isdigit()

        # Net Price and Gross Price must be float or int :
        has_price_floats: bool = is_float(gross) and is_float(net)

        # Date Part should be correct :
        is_date: bool = type(selling_date) is datetime

        if has_price_floats:
            gross = float(gross)
            net = float(net)

        print(type(gross), gross)
        print(type(net), net)
        print(has_price_floats)

        if not has_empty_fields and has_names_strings and has_price_floats and is_date:
            try:
                data = {'ID': [int(i.cells[0].content.value) for i in upd_record_table.rows if i.selected][0],
                        'customer_name': customer,
                        'item_name': item,
                        'gross_price': gross,
                        'net_price': net,
                        'profit': gross - net,
                        'selling_date': selling_date}
            except IndexError:
                update_failed(e)
            else:
                is_updated: bool = md.update_record(data=data)
                update_success(e) if is_updated else update_failed(e)

        else:
            update_failed(e)
            upd_update_form.visible = False
            upd_update_btn.visible = False
            upd_delete_btn.visible = False
            print("Input fields has issue")
            print(customer, item, gross, net, selling_date)
            page.update()

    def upd_change_date_text(e: ControlEvent):
        upd_date_text.value = upd_date_picker.value
        page.update()

    update_failed_msg: AlertDialog = AlertDialog(
        open=False,
        title=Text("Data Updated Failed"),
        content=Row(controls=[Icon(name=icons.REPORT_GMAILERRORRED, color=colors.RED, size=35),
                              Text("Input fields have some issues, Please try to correct it before update", size=20)])
    )

    update_success_msg: AlertDialog = AlertDialog(
        open=False,
        title=Text("Data Updated !"),
        content=Row(controls=[Icon(name=icons.CHECK_CIRCLE_ROUNDED, color=colors.GREEN, size=35),
                              Text("Selected Record Successfully Updated")])
    )

    upd_cst_input: TextField = TextField(label="Customer Name", width=500,
                                         border_color=colors.BLUE_200)
    upd_item_input: TextField = TextField(label="Item Name", width=500,
                                          border_color=colors.BLUE_200)
    upd_gross_input: TextField = TextField(label="Gross Price", width=500,
                                           border_color=colors.BLUE_200, prefix_text="₹ ")
    upd_net_input: TextField = TextField(label="Net Price", width=500,
                                         border_color=colors.BLUE_200, prefix_text="₹ ")

    upd_date_picker: DatePicker = DatePicker(on_change=upd_change_date_text)
    upd_date_text: TextField = TextField(label="Selected Date",
                                         border_color=colors.BLUE_200)
    upd_pick_icon_up: IconButton = IconButton(icon=icons.CALENDAR_MONTH,
                                              on_click=lambda _: upd_date_picker.pick_date())
    upd_submit_btn: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.SEND),
                                                                          Text("Submit")],
                                                                height=45),
                                                    on_click=update_record)

    upd_update_form: Container = Container(content=Column(
        controls=[Text("Update Form", size=25, weight=ft.FontWeight.BOLD),
                  upd_cst_input,
                  upd_item_input,
                  upd_gross_input,
                  upd_net_input,
                  Row(controls=[upd_date_text, upd_pick_icon_up], alignment=MainAxisAlignment.CENTER),
                  upd_submit_btn],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    ),
        visible=False,
        margin=20, padding=20,
        border=ft.border.all(2, 'white'),
        border_radius=ft.border_radius.all(5)
    )

    upd_delete_btn: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.DELETE_SHARP,
                                                                               color=colors.RED_400),
                                                                          Text("Delete Selected Rows",
                                                                               color=colors.RED_400,
                                                                               size=16)],
                                                                height=45),
                                                    on_click=delete_all_rows,
                                                    visible=False)

    upd_update_btn: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.SETTINGS_BACKUP_RESTORE,
                                                                               color=colors.ORANGE),
                                                                          Text("Update Selected Row",
                                                                               color=colors.ORANGE,
                                                                               size=16)],
                                                                height=45),
                                                    on_click=show_update_form,
                                                    visible=False)

    upd_record_table = DataTable(
        columns=[
            DataColumn(Text("ID", weight=ft.FontWeight.BOLD)),
            DataColumn(Text("Customer name", weight=ft.FontWeight.BOLD)),
            DataColumn(Text("Item name", weight=ft.FontWeight.BOLD)),
            DataColumn(Text("Gross Price (₹)", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Net Price (₹)", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Profit (₹)", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Selling Date \n(DD-MM-YYYY)", weight=ft.FontWeight.BOLD))
        ],
        rows=[
            DataRow(
                cells=[
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found"))
                ],
            )
        ],
        on_select_all=all_show_delete_btn,
        show_checkbox_column=True,
        border=border.all(2, "white"),
        vertical_lines=ft.border.BorderSide(1, "white"),
        horizontal_lines=ft.border.BorderSide(1, "white"),
    )

    analytics_total_profit_chip: Chip = Chip(
        label=Text('Total Profit : ₹ 0.0', weight=ft.FontWeight.BOLD),
        on_select=lambda e: page.update(),
        border_side=ft.BorderSide(10, colors.LIGHT_BLUE),
    )

    upd_dlt_main_column: Column = Column(controls=[
        Row(controls=[upd_month, upd_year], alignment=MainAxisAlignment.CENTER),
        Row(controls=[upd_search_record_btn], alignment=MainAxisAlignment.CENTER),
        upd_divider,
        Row(controls=[upd_record_table], alignment=MainAxisAlignment.CENTER),
        Row(controls=[analytics_total_profit_chip], alignment=MainAxisAlignment.CENTER),
        Row(controls=[upd_update_form], alignment=MainAxisAlignment.CENTER),
        Row(controls=[upd_update_btn, upd_delete_btn], alignment=MainAxisAlignment.CENTER),
    ],
        alignment=MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ALWAYS,
    )

    upd_dlt_record_main: Container = Container(
        content=upd_dlt_main_column,
        margin=20, padding=40)

    # ----------------------------------- Analytics Widgets ----------------------------------- #
    """
    -> Basic Analytics in special text (MEAN, STD, MAX, MIN, Total Profit(Rs.)) [Done]
    -> Most sold items  (Item has max profit) [Done]
    -> Regular Customer (Multiple occurances for same customer)  [Done]
    -> Season Time for selling (Time Series Analysis)  [Done]
    -> Maximum profit from which customer  [Done]
    -> Maximum profit from which item  [Done]  """

    def get_describe(df: pd.DataFrame) -> pd.DataFrame:
        describe = df.loc[:, ['gross_price', 'net_price', 'profit']].describe().round(2)
        cols = ['mean', 'min', '25%', '50%', '75%', 'max']
        describe = describe.loc[cols, :]
        describe.reset_index(names=['terms'], inplace=True)
        return describe

    def get_frequent_month(df: pd.DataFrame) -> pd.DataFrame:
        frequent_months: pd.DataFrame = pd.to_datetime(df['selling_date']) \
            .dt.strftime('%B') \
            .value_counts(ascending=False) \
            .reset_index()
        return frequent_months

    def show_basic_analytics_error(e):
        page.dialog = basic_analytics_alert
        basic_analytics_alert.open = True
        page.update()

    def show_graph_error(e):
        page.dialog = graphs_display_alert
        graphs_display_alert.open = True
        page.update()

    def refresh_analytics(e):
        df = md.get_df_for_analysis()
        if len(df) >= 5:
            basic_analytics_container.visible = True
            describe: pd.DataFrame = get_describe(df)
            frequent_months: pd.DataFrame = get_frequent_month(df)
            popular_items: pd.DataFrame = df['item_name'].value_counts(ascending=False).reset_index().iloc[:5]
            regular_customer: pd.DataFrame = df['customer_name'].value_counts(ascending=False).reset_index().iloc[:5]

            max_profit_cst: pd.DataFrame = df.loc[:, ['customer_name', 'profit']] \
                                               .groupby(by='customer_name').sum() \
                                               .sort_values(by='profit', ascending=False) \
                                               .reset_index().iloc[:5]

            max_profit_item: pd.DataFrame = df.loc[:, ['item_name', 'profit']] \
                                                .groupby(by='item_name').sum() \
                                                .sort_values(by='profit', ascending=False) \
                                                .reset_index().iloc[:5]

            # Render Datatable :
            describe_datatable.rows.clear()
            for index, each in describe.iterrows():
                describe_datatable.rows.append(
                    DataRow(cells=[DataCell(Text(each['terms'])),
                                   DataCell(Text(each['gross_price'])),
                                   DataCell(Text(each['net_price'])),
                                   DataCell(Text(each['profit'])),
                                   ])
                )

            item_per_month.rows.clear()
            for index, each in frequent_months.iterrows():
                item_per_month.rows.append(
                    DataRow(cells=[DataCell(Text(each['selling_date'])),
                                   DataCell(Text(each['count']))
                                   ])
                )

            top_5_items.rows.clear()
            for index, each in popular_items.iterrows():
                top_5_items.rows.append(
                    DataRow(cells=[DataCell(Text(each['item_name'])),
                                   DataCell(Text(each['count']))
                                   ])
                )

            top_5_cst.rows.clear()
            for index, each in regular_customer.iterrows():
                top_5_cst.rows.append(
                    DataRow(cells=[DataCell(Text(each['customer_name'])),
                                   DataCell(Text(each['count']))
                                   ])
                )

            profit_by_cst.rows.clear()
            for index, each in max_profit_cst.iterrows():
                profit_by_cst.rows.append(
                    DataRow(cells=[DataCell(Text(each['customer_name'])),
                                   DataCell(Text(each['profit']))
                                   ])
                )

            profit_by_item.rows.clear()
            for index, each in max_profit_item.iterrows():
                profit_by_item.rows.append(
                    DataRow(cells=[DataCell(Text(each['item_name'])),
                                   DataCell(Text(each['profit']))
                                   ])
                )

            main_analytics_column.scroll_to(offset=-1 if not graph_image.visible else 10, duration=100)
        else:
            show_basic_analytics_error(e)
            # print("Not enough data to display, Try to add some more records using Add Record Tab")
        page.update()

    def hide_analytics(e):
        # All controls should be visible = False at this place
        basic_analytics_container.visible = False
        describe_datatable.rows.clear()
        item_per_month.rows.clear()
        top_5_items.rows.clear()
        top_5_cst.rows.clear()
        profit_by_cst.rows.clear()
        profit_by_item.rows.clear()
        main_analytics_column.scroll_to(offset=1, duration=100)
        page.update()

    basic_analytics_alert: AlertDialog = AlertDialog(
        open=False,
        title=Text("Data not Fetched Properly"),
        content=Row(controls=[Icon(name=icons.REPORT_GMAILERRORRED, color=colors.RED, size=35),
                              Text("Not enough data to show analytics, Try to add some more records", size=20)])
    )

    graphs_display_alert: AlertDialog = AlertDialog(
        open=False,
        title=Text("Data not Fetched Properly"),
        content=Row(controls=[Icon(name=icons.REPORT_GMAILERRORRED, color=colors.RED, size=35),
                              Text("Invalid selection, Try to change options from drop down", size=20)])
    )

    describe_datatable: DataTable = DataTable(
        columns=[
            DataColumn(Text("Calculations", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Gross Price (₹)", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Net Price (₹)", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Profit (₹)", weight=ft.FontWeight.BOLD), numeric=True),
        ],
        rows=[
            DataRow(
                cells=[
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found"))
                ],
            )
        ],
        border=border.all(2, "white"),
        vertical_lines=ft.border.BorderSide(1, "white"),
        horizontal_lines=ft.border.BorderSide(1, "white"),
    )

    item_per_month: DataTable = DataTable(
        columns=[
            DataColumn(Text("Month", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Items Count", weight=ft.FontWeight.BOLD), numeric=True),
        ],
        rows=[
            DataRow(
                cells=[
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found"))
                ],
            )
        ],
        border=border.all(2, "white"),
        vertical_lines=ft.border.BorderSide(1, "white"),
        horizontal_lines=ft.border.BorderSide(1, "white"),
    )

    top_5_items: DataTable = DataTable(
        columns=[
            DataColumn(Text("Item Name", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Item Count", weight=ft.FontWeight.BOLD), numeric=True),
        ],
        rows=[
            DataRow(
                cells=[
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found"))
                ],
            )
        ],
        border=border.all(2, "white"),
        vertical_lines=ft.border.BorderSide(1, "white"),
        horizontal_lines=ft.border.BorderSide(1, "white"),
    )

    top_5_cst: DataTable = DataTable(
        columns=[
            DataColumn(Text("Customer Name", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Customer Count", weight=ft.FontWeight.BOLD), numeric=True),
        ],
        rows=[
            DataRow(
                cells=[
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found"))
                ],
            )
        ],
        border=border.all(2, "white"),
        vertical_lines=ft.border.BorderSide(1, "white"),
        horizontal_lines=ft.border.BorderSide(1, "white"),
    )

    profit_by_cst: DataTable = DataTable(
        columns=[
            DataColumn(Text("Customer Name", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Profit (₹)", weight=ft.FontWeight.BOLD), numeric=True),
        ],
        rows=[
            DataRow(
                cells=[
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found"))
                ],
            )
        ],
        border=border.all(2, "white"),
        vertical_lines=ft.border.BorderSide(1, "white"),
        horizontal_lines=ft.border.BorderSide(1, "white"),
    )

    profit_by_item: DataTable = DataTable(
        columns=[
            DataColumn(Text("Item Name", weight=ft.FontWeight.BOLD), numeric=True),
            DataColumn(Text("Profit (₹)", weight=ft.FontWeight.BOLD), numeric=True),
        ],
        rows=[
            DataRow(
                cells=[
                    DataCell(Text("No results found")),
                    DataCell(Text("No results found"))
                ],
            )
        ],
        border=border.all(2, "white"),
        vertical_lines=ft.border.BorderSide(1, "white"),
        horizontal_lines=ft.border.BorderSide(1, "white"),
    )

    refresh_analytics_btn: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.REFRESH_SHARP),
                                                                                 Text("Refresh Basic Analytics")],
                                                                       height=45),
                                                           on_click=refresh_analytics)
    hide_analytics_btn: ElevatedButton = ElevatedButton(content=
                                                        Row(controls=[Icon(name=icons.CANCEL_PRESENTATION_OUTLINED),
                                                                      Text("Hide Analytics")],
                                                            height=45),
                                                        on_click=hide_analytics)

    basic_analytics_container: Container = Container(
        visible=False,
        content=Column(
            controls=[
                Row(controls=[
                    Column(controls=[
                        Text('Description of Data', size=23, weight=ft.FontWeight.BOLD),
                        Row(controls=[describe_datatable])
                    ])
                ], alignment=MainAxisAlignment.CENTER),
                Divider(height=5, color=colors.WHITE),
                Row(controls=[
                    Column(controls=[
                        Text('Top 5 selling item', size=23, weight=ft.FontWeight.BOLD),
                        Row(controls=[top_5_items]),
                    ]),
                    VerticalDivider(width=5, color=colors.WHITE),
                    Column(controls=[
                        Text('Top 5 regular customer', size=23, weight=ft.FontWeight.BOLD),
                        Row(controls=[top_5_cst]),
                    ]),
                    VerticalDivider(width=5, color=colors.WHITE),
                    Column(controls=[
                        Text('Product selling per month', size=23, weight=ft.FontWeight.BOLD),
                        Row(controls=[item_per_month])
                    ])
                ], alignment=MainAxisAlignment.CENTER),
                Divider(height=5, color=colors.WHITE),
                Row(controls=[
                    Column(controls=[
                        Text('Top 5 Customers Total Profit', size=23, weight=ft.FontWeight.BOLD),
                        Row(controls=[profit_by_cst]),
                    ]),
                    VerticalDivider(width=5, color=colors.WHITE),
                    Column(controls=[
                        Text('Top 5 Items Total Profit', size=23, weight=ft.FontWeight.BOLD),
                        Row(controls=[profit_by_item]),
                    ])
                ], alignment=MainAxisAlignment.CENTER),
            ])
    )

    def get_graph(e):
        current = os.listdir('./assets')
        if len(current) > 0:
            # Delete the file
            current = os.listdir('./assets')
            for i in current:
                os.remove('assets/' + i)

        # Will create graph :
        fig_num: int | None = md.get_plot(options=categories.value)
        if fig_num is not None:
            img_container.visible = True
            graph_image.clean()
            graph_image.src = f'assets/plot{fig_num}.png'
            main_analytics_column.scroll_to(offset=-1, duration=100)
        else:
            show_graph_error(e)
            print("Show error message of graph not generated at this stage")

        page.update()

    def reset_graph(e):
        img_container.visible = False
        graph_image.src = ''
        graph_image.clean()
        categories.value = '-- Select --'
        if os.path.exists('assets/plot1.png'):
            # Delete the file
            os.remove('assets/plot1.png')
        page.update()

    plotting_options: list[str] = ['Profit over Customer',
                                   'Profit over Items',
                                   'Profit over Time (Month or Year)',
                                   'Profit Margin over Items (%)',
                                   'Top Items counts based on selling',
                                   'Regular Customer in Business']

    categories: Dropdown = Dropdown(width=500,
                                    label="Choose Plotting Options",
                                    options=[ft.dropdown.Option("-- Select --"),
                                             *[ft.dropdown.Option(i) for i in plotting_options]],
                                    border_color=colors.BLUE_200)

    selected_option_btn: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.FIND_IN_PAGE_OUTLINED),
                                                                               Text("Get Graph")],
                                                                     height=45),
                                                         on_click=get_graph)

    reset_graph_btn: ElevatedButton = ElevatedButton(content=Row(controls=[Icon(name=icons.REPEAT_ROUNDED),
                                                                           Text("Reset Graph")],
                                                                 height=45),
                                                     on_click=reset_graph)

    graph_image: Image = Image(src='assets/plot1.png', width=750, height=590, fit=ft.ImageFit.CONTAIN)
    img_container: Container = Container(
        visible=False,
        content=graph_image,
        margin=20, padding=40,
        shadow=ft.BoxShadow(blur_radius=20,
                            color=ft.colors.BLUE_GREY_300,
                            offset=ft.Offset(0, 0),
                            blur_style=ft.ShadowBlurStyle.OUTER),
        border_radius=10,
        bgcolor=colors.WHITE,
        border=border.all(0, colors.WHITE)
    )

    divider_analytics: Divider = Divider(height=5, color=colors.WHITE)
    main_analytics_column: Column = Column(controls=[
        Row(controls=[basic_analytics_container], alignment=MainAxisAlignment.CENTER),
        Row(controls=[refresh_analytics_btn, hide_analytics_btn], alignment=MainAxisAlignment.CENTER),
        divider_analytics,
        Row(controls=[categories], alignment=MainAxisAlignment.CENTER),
        Row(controls=[selected_option_btn, reset_graph_btn], alignment=MainAxisAlignment.CENTER),
        Row(controls=[img_container], alignment=MainAxisAlignment.CENTER),
    ], scroll=ft.ScrollMode.ADAPTIVE)

    analytics_main: Container = Container(
        content=main_analytics_column,
        margin=10, padding=10
    )

    # ----------------------------------- Main Page Tabs ----------------------------------- #
    main_tab: Tabs = Tabs(
        selected_index=0,
        animation_duration=300,
        tab_alignment=TabAlignment.CENTER,
        tabs=[
            Tab(text="Add Records",
                icon=icons.PERSON_ADD_ROUNDED,
                content=add_record_main),
            Tab(text="Search Records",
                icon=icons.VIEW_LIST,
                content=search_record_main),
            Tab(text="Update \\ Delete Records",
                icon=icons.UPDATE,
                content=upd_dlt_record_main),
            Tab(text="Analytics",
                icon=icons.AUTO_GRAPH_ROUNDED,
                content=analytics_main),
            Tab(text="Dark Theme",
                tab_content=dark_light_switch)
        ],
        expand=True
    )

    page.overlay.append(date_picker)
    page.overlay.append(upd_date_picker)
    page.overlay.append(picker)  # Add Record Tab

    page.add(main_tab)
    cst_name.focus()  # Add Records Tab
    dsp_cst_name.focus()  # Search Records


# if __name__ == '__main__':
ft.app(target=main, assets_dir='assets')
