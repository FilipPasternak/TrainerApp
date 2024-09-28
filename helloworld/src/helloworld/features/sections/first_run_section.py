import toga
import os
import csv

class FirstRunSection:
    def __init__(self, path):
        self.user_data = None
        self.next_page = None
        self.path = path

    def save_user_data_and_proceed(self, widget):
        import helloworld.common.actions as actions

        # Save data to user_data.csv
        headers, values = self.user_data[0], self.user_data[1]

        storage_dir = os.path.join(self.path, 'storage')
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        csv_path = os.path.join(storage_dir, 'user_data.csv')

        for i in range(len(values)):
            values[i] = values[i].value

        # Check if the file exists, and if not, create it with headers
        if not os.path.exists(csv_path):
            with open(csv_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.user_data)
        else:
            with open(self.path, mode='r', newline='') as file:
                reader = csv.reader(file)
                existing_data = list(reader)

            for i in range(len(headers)):
                existing_data[0].append(headers[i])
                existing_data[1].append(str(values[i]))

            with open(self.path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(existing_data)

        if self.next_page == 'user_gear':
            actions.go_to_first_run_user_gear_page(widget=widget)
