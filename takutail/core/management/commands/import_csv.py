import csv
import os
from django.core.management.base import BaseCommand
from core.models import Sake, Wari, Other
from cocktails.models import Cocktail, CocktailName
from django.conf import settings

class Command(BaseCommand):
    help = 'Import CSV data into the database'

    def handle(self, *args, **kwargs):
        self.import_sake()
        self.import_wari()
        self.import_other()
        self.import_cocktail()
        self.import_cocktail_name()

    def get_csv_path(self, filename):
        return os.path.join(settings.BASE_DIR, 'core', 'management', 'commands', 'csv', filename)

    def import_sake(self):
        with open(self.get_csv_path('sake.csv'), newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Sake.objects.create(
                    name=row['name'],
                    color=row['color'],
                    aroma=row['aroma'],
                    sweetness=row['sweetness'],
                    bitterness=row['bitterness'],
                    sourness=row['sourness'],
                    alcohol_content=row['alcohol_content'],
                    
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported sake data'))

    def import_wari(self):
        with open(self.get_csv_path('wari.csv'), newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Wari.objects.create(
                    name=row['name'],
                    color=row['color'],
                    aroma=row['aroma'],
                    sweetness=row['sweetness'],
                    bitterness=row['bitterness'],
                    sourness=row['sourness'],
                    exclude=row['exclude'] == '除外',
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported wari data'))

    def import_other(self):
        with open(self.get_csv_path('other.csv'), newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Other.objects.create(
                    name=row['name'],
                    exclude=row['exclude'] == '除外',
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported other data'))

    def import_cocktail(self):
        with open(self.get_csv_path('cocktail.csv'), newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Cocktail.objects.create(
                    name=row['name'],
                    generated_name=row.get('generated_name', ''),
                    base=row['base'],
                    base_amount=row['base_amount'],
                    ingredient1=row.get('ingredient1', ''),
                    amount1=row.get('amount1', ''),
                    ingredient2=row.get('ingredient2', ''),
                    amount2=row.get('amount2', ''),
                    ingredient3=row.get('ingredient3', ''),
                    amount3=row.get('amount3', ''),
                    ingredient4=row.get('ingredient4', ''),
                    amount4=row.get('amount4', ''),
                    ingredient5=row.get('ingredient5', ''),
                    amount5=row.get('amount5', ''),
                    note=row.get('note', ''),
                    recipe=row.get('recipe', ''),
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported cocktail data'))

    def import_cocktail_name(self):
        with open(self.get_csv_path('cocktail_name2.csv'), newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                CocktailName.objects.create(
                    name=row['name'],
                    base=row['base'],
                    ingredient1=row['ingredient1'],
                    ingredient2=row['ingredient2'] if row['ingredient2'] else None,
                    ingredient3=row['ingredient3'] if row['ingredient3'] else None,
                    ingredient4=row['ingredient4'] if row['ingredient4'] else None,
                    top=row['top'] == '1',
                    middle=row['middle'] == '1',
                    bottom=row['bottom'] == '1',
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported cocktail name data'))
