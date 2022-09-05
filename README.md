# cscoffeechat_matching

CS Coffee Chat is a program that facilitates mentorship at UBC. It has matched 150+ lower year to upper year Computer Science students for monthly coffee chats.

This script was written to consume CSV table data from survey forms and generate matching based on preferences.

## Usage

```shell
python3 ./matching.py --input coffee-2020-02.csv --output February_2020_matching.csv
```

### Input file

You'll need a "input" CSV file containing 1 row per student who wants to be matched. There must be a header in row 1 with columns that corresponds to the values in `column_names` inside [signup_students.py](./signup_students.py).

The file needs to be placed inside the `signup_data` folder. Pass in the name of the file inside `signup_data` using the `--input` flag.

The CSV should have exactly 1 header row and all subsequent rows should contain data.

### Output file

A specific output filename can be optionally set using the `--output` flag. Files will be saved in the `matching_data` folder.

### Past matches folder

A folder with past matches can be supplied using the `--past-matches` flag. Entries here will be used to avoid duplicate matches. You can choose to point this flag towards the `matching_data` folder (`--past-matches matching_data`) to simply reuse output from previous executions of the script.

## Authentication

Make sure you have a credentials.json file containing your Google Sheets API credentials, according to [this guide](https://developers.google.com/sheets/api/quickstart/python).

Make sure you have a sendgrid.env file containing your Sendgrid credentials, according to [this guide](https://github.com/sendgrid/sendgrid-python#setup-environment-variables).
