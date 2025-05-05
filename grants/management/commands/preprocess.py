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
                    'Column 1': 'Column1',
                    'Full Name': 'FullName',
                    'Email': 'Email',
                    'Profession / Occupation': 'Profession',
                    'Country of Origin': 'Country',
                    'City or Town You Are Traveling From': 'City',
                    'Do you only need a conference ticket?': 'TicketOnly',
                    'Type of Grant': 'GrantType',
                    'How much financial assistance would you need to attend DjangoCon Africa 2025. Please itemize below: (eg. Flight, lodging, ground transportation, Visa, incidence) etc.': 'Budget',
                }

                rows = []
                for row in reader:
                    new_row = []
                    for new_col in new_header:
                        old_col = next((k for k, v in old_to_new.items() if v == new_col), None)
                        value = row.get(old_col, '')  # Use empty string for blank values
                        new_row.append(value)
                    rows.append(new_row)

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