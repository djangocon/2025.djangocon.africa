import csv
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Preprocess a CSV file by replacing the header with standardized names, excluding Motivation'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str, help='Path to the input CSV file')
        parser.add_argument('output_file', type=str, help='Path to the output CSV file')

    def handle(self, *args, **kwargs):
        input_file = kwargs['input_file']
        output_file = kwargs['output_file']

        # Define new header (matches GrantApplication fields, no Motivation)
        new_header = [
            'Timestamp', 'Column1', 'FullName', 'Email', 'Profession', 'Country',
            'City', 'TicketOnly', 'GrantType', 'Budget'
        ]

        try:
            with open(input_file, 'r', encoding='utf-8-sig') as infile:
                reader = csv.DictReader(infile)
                # Debug: Print original headers
                self.stdout.write(self.style.WARNING(f"Original CSV Headers: {reader.fieldnames}"))

                # Map original columns to new header
                old_to_new = {
                    'Timestamp': 'Timestamp',
                    'Column1': 'Column1',
                    'FullName': 'FullName',
                    'Email': 'Email',
                    'Profession': 'Profession',
                    'CountryOrigin': 'Country',
                    'CityTravelingFrom': 'City',
                    'YourNeed': 'TicketOnly',
                    'TypeofGrant': 'GrantType',
                    'Budget': 'Budget',
                }

                # Verify all expected columns exist
                missing_cols = [col for col in old_to_new if col not in reader.fieldnames]
                if missing_cols:
                    self.stdout.write(
                        self.style.WARNING(f"Missing columns in CSV: {missing_cols}")
                    )

                rows = []
                for row_num, row in enumerate(reader, 1):
                    new_row = {}
                    for new_col in new_header:
                        # Find the original column name that maps to this new column
                        old_col = next((k for k, v in old_to_new.items() if v == new_col), None)
                        if old_col:
                            value = row.get(old_col, '').strip()  # Use empty string for blank values, strip whitespace
                            new_row[new_col] = value
                        else:
                            self.stdout.write(
                                self.style.WARNING(f"Row {row_num}: No mapping for new column {new_col}")
                            )
                            new_row[new_col] = ''
                    # Debug: Check Budget specifically
                    if not new_row.get('Budget'):
                        self.stdout.write(
                            self.style.WARNING(f"Row {row_num}: Budget is empty or missing")
                        )
                    rows.append([new_row[col] for col in new_header])

            # Validate row lengths
            header_len = len(new_header)
            for i, row in enumerate(rows, 1):
                if len(row) != header_len:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Row {i+1} has {len(row)} columns, expected {header_len}"
                        )
                    )

            # Write new CSV
            with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(new_header)
                writer.writerows(rows)

            self.stdout.write(
                self.style.SUCCESS(f"Preprocessed CSV saved as {output_file}")
            )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Input file {input_file} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error preprocessing CSV: {e}"))