import csv
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from data_visualization.models import DataItem, Region, SubRegion


class Command(BaseCommand):
    help = 'Read data from csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to csv file')

    def handle(self, *args, **options):
        csv_path = options['csv_path']

        if not os.path.exists(csv_path):
            raise CommandError(f'File not found: {csv_path}')

        if not csv_path.lower().endswith('.csv'):
            self.stdout.write(
                self.style.WARNING(f'File not in .csv format: {csv_path}')
            )

        try:
            data = []
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                regions_to_create = []
                sub_regions_to_create = []
                for row in reader:
                    data.append(row)
                    regions_to_create.append(row[0])
                    sub_regions_to_create.append(row[1])

            with transaction.atomic():
                Region.objects.all().delete()
                SubRegion.objects.all().delete()
                DataItem.objects.all().delete()

                region_id_map = {}
                sub_region_id_map = {}

                for region_name in regions_to_create:
                    if region_name not in region_id_map:
                        region = Region(name=region_name)
                        region.save()
                        region_id_map.update({region.name: region.id})

                for sub_region_name in sub_regions_to_create:
                    if sub_region_name not in sub_region_id_map:
                        sub_region = SubRegion(name=sub_region_name)
                        sub_region.save()
                        sub_region_id_map.update({sub_region.name: sub_region.id})

                for data_item in data:
                    value = data_item[2]
                    region_id = region_id_map.get(data_item[0], None)
                    sub_region_id = sub_region_id_map.get(data_item[1], None)

                    try:
                        int(value)
                    except (ValueError, TypeError):
                        print(f"Error value in record {data_item}")

                    if region_id and sub_region_id:
                        DataItem.objects.create(region_id=region_id, sub_region_id=sub_region_id, value=value)

        except Exception as e:
            raise CommandError(f'Error: {e}')
