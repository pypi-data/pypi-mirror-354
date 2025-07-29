from django.core.management.base import BaseCommand, CommandError
import polib
import csv


class Command(BaseCommand):
    help = "Converts .po files to .csv format"

    def add_arguments(self, parser):
        parser.add_argument("po_file", type=str, help="Path to the .po file")
        parser.add_argument("csv_file", type=str, help="Path to the .csv file to create")

    def handle(self, *args, **options):
        try:
            po = polib.pofile(options["po_file"])
            with open(options["csv_file"], mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["msgid", "msgstr", "comments"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for entry in po:
                    writer.writerow({"msgid": entry.msgid, "msgstr": entry.msgstr, "comments": entry.comment})

            self.stdout.write(self.style.SUCCESS("Successfully converted .po to .csv"))
        except Exception as e:
            raise CommandError(f"Error converting .po to .csv: {e}")
