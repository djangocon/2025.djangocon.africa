import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from grants.models import GrantApplication
from django.utils import timezone
import pytz


class Command(BaseCommand):
    help = "Import grant applications from a preprocessed CSV file, updating existing records for duplicate emails, or revert imports"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="Path to the preprocessed CSV file"
        )
        parser.add_argument(
            "--revert",
            action="store_true",
            help="Revert the import by deleting records from the CSV file",
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        revert = kwargs["revert"]

        if revert:
            self.revert_import(csv_file)
        else:
            self.import_applications(csv_file)

    def import_applications(self, csv_file):
        valid_grant_types = ["TRAVEL", "TICKET", "FULL", "SPEAKER"]

        try:
            with open(csv_file, "r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                self.stdout.write(
                    self.style.WARNING(f"CSV Headers: {reader.fieldnames}")
                )

                for row in reader:
                    try:
                        # Normalize headers and values
                        normalized_row = {}
                        for key, value in row.items():
                            if key is not None:
                                normalized_key = key.strip() if key else ""
                                normalized_row[normalized_key] = (
                                    value if value is not None else ""
                                )

                        # Check required columns
                        required_keys = [
                            "Timestamp",
                            "FullName",
                            "Email",
                            "TicketOnly",
                            "GrantType",
                            "Budget",
                        ]
                        for key in required_keys:
                            if key not in normalized_row:
                                raise KeyError(
                                    f"Column '{key}' not found in row for email {normalized_row.get('Email', 'unknown')}"
                                )

                        # Debug: Print row data
                        self.stdout.write(
                            self.style.WARNING(
                                f"Row data for {normalized_row.get('Email', 'unknown')}: {normalized_row}"
                            )
                        )

                        # Parse timestamp (make timezone-aware)
                        naive_timestamp = datetime.strptime(
                            normalized_row["Timestamp"], "%m/%d/%Y %H:%M:%S"
                        )
                        timestamp = timezone.make_aware(naive_timestamp, pytz.UTC)

                        # Map ticket_only
                        ticket_only = normalized_row["TicketOnly"].strip()
                        ticket_only = "YES" if ticket_only.lower() == "yes" else "NO"

                        # Map grant_type
                        grant_type = normalized_row["GrantType"].strip().upper()
                        if not grant_type or grant_type not in valid_grant_types:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Invalid or blank grant_type '{grant_type}' for {normalized_row.get('Email', 'unknown')}, defaulting to SPEAKER"
                                )
                            )
                            grant_type = "SPEAKER"

                        # Handle blank budget
                        budget = (
                            normalized_row["Budget"].strip()
                            if normalized_row["Budget"].strip()
                            else ""
                        )

                        # Create or update grant application
                        GrantApplication.objects.update_or_create(
                            email=normalized_row["Email"],
                            defaults={
                                "timestamp": timestamp,
                                "full_name": normalized_row["FullName"],
                                "ticket_only": ticket_only,
                                "grant_type": grant_type,
                                "budget_details": budget,
                                "status": "PENDING",
                            },
                        )

                        self.stdout.write(
                            self.style.SUCCESS(f"Imported {normalized_row['Email']}")
                        )
                    except KeyError as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"KeyError importing {row.get('Email', 'unknown')}: {e}"
                            )
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Error importing {row.get('Email', 'unknown')}: {e}"
                            )
                        )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {csv_file} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading CSV: {e}"))

    def revert_import(self, csv_file):
        try:
            with open(csv_file, "r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                if "Email" not in reader.fieldnames:
                    self.stdout.write(
                        self.style.ERROR("CSV file must contain an 'Email' column")
                    )
                    return

                emails = [
                    row["Email"].strip() for row in reader if row["Email"].strip()
                ]
                if not emails:
                    self.stdout.write(
                        self.style.WARNING("No valid emails found in CSV")
                    )
                    return

                # Delete GrantApplication records matching the emails
                deleted_count, _ = GrantApplication.objects.filter(
                    email__in=emails
                ).delete()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Reverted import: deleted {deleted_count} records"
                    )
                )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {csv_file} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during revert: {e}"))
