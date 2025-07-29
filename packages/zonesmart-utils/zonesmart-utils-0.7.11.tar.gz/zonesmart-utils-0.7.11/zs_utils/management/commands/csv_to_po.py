from django.core.management.base import BaseCommand, CommandError
import polib
import csv


class Command(BaseCommand):
    help = "Converts .csv files back to .po format"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the .csv file")
        parser.add_argument("po_file", type=str, help="Path to the .po file to create")

    def handle(self, *args, **options):
        try:
            po = polib.POFile()
            po.metadata["Content-Type"] = "text/plain; charset=UTF-8"
            po.metadata["Content-Transfer-Encoding"] = "8bit"
            po.metadata["Plural-Forms"] = "nplurals=2; plural=(n != 1);"
            with open(options["csv_file"], mode="r", newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    entry = polib.POEntry(msgid=row["msgid"], msgstr=row["msgstr"], comment=row["comments"])
                    po.append(entry)

            po.save(options["po_file"])
            self.stdout.write(self.style.SUCCESS("Successfully converted .csv to .po"))
        except Exception as e:
            raise CommandError(f"Error converting .csv to .po: {e}")
