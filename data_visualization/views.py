from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from data_visualization.models import DataItem

CSV_PATH = settings.BASE_DIR.joinpath('data/input_data.csv')


@login_required(login_url='/users/login/')
def index(request):
    data = list(DataItem.objects.select_related('region', 'sub_region') \
                .order_by('region__name', 'sub_region__name') \
                .values_list('region__name', 'sub_region__name', 'value'))

    return render(request, 'data_visualisation/index.html', {'data': data})
