import toga
import os
import csv

class CommonPage:
    def __init__(self, path):
        self.user_data = None
        self.next_page = None
        self.path = path

    def save_user_data_and_proceed(self, widget):
        '''
        Saves self.user data to user_data.csv file
        self.user data needs to be in form:
        [['header1', 'header2', ...], [val1, val2, ...]]
        :param widget: Button widget
        :return: None
        '''
        import helloworld.common.actions as actions

        # Save data to user_data.csv
        headers, values = self.user_data[0], self.user_data[1]

        storage_dir = os.path.join(self.path, 'storage')
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        csv_path = os.path.join(storage_dir, 'user_data.csv')
        for i in range(len(values)):
            if isinstance(values[i], str) or isinstance(values[i], list):
                values[i] = str(values[i])
            else:
                values[i] = values[i].value

        # Check if the file exists, and if not, create it with headers
        if not os.path.exists(csv_path):
            with open(csv_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.user_data)
        else:
            with open(csv_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

            for i in range(len(headers)):
                if headers[i] not in existing_data[0]:
                    existing_data[0].append(headers[i])
                    existing_data[1].append(str(values[i]))
                else:
                    existing_header_index = existing_data[0].index(headers[i])
                    existing_data[1][existing_header_index] = str(values[i])

            with open(csv_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(existing_data)

        if self.next_page == 'user_place':
            actions.go_to_first_run_user_place_page(widget=widget)
        elif self.next_page == 'user_gear':
            actions.go_to_user_gear_page(widget=widget)
        elif self.next_page == 'user_goal':
            actions.go_to_user_goal_page(widget=widget)
        elif self.next_page == 'dev_page':
            actions.go_to_dev_page(widget=widget)


