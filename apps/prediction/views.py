import re
import os

from iBird import settings
from apps.prediction.neural_network.predict_server import NeuralNetwork
from apps.utils.decorator import RequiredMethod, RequiredParameters
from apps.utils.response_processor import process_response
from apps.utils.response_status import ResponseStatus
from apps.prediction import models as prediction_models

# 识别网络
net = NeuralNetwork(settings.MODEL_PATH, settings.CLASSES_PATH)


@RequiredMethod('POST')
@RequiredParameters('path')
def predict(request):
    json_data = request.json_data

    path = json_data['path']
    if len(path) > 100 or re.search(r'\.\.', path) or path[:9] != '/' + settings.PICTURE_PATH \
            or not os.path.exists('.' + path):
        return process_response(request, ResponseStatus.IMAGE_PATH_NOT_FOUND_ERROR)

    report = prediction_models.Report.objects.filter(path=path).first()
    if not report:
        report = prediction_models.Report(path=path)
        report.result = net.predicted('.' + path)
        report.save()

    request.data = report.transform_into_serialized_data()

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('GET')
def get_report(request):
    sequence = request.GET.get('sequence')
    if not sequence:
        return process_response(request, ResponseStatus.SEQUENCE_REQUIRED_ERROR)

    report = prediction_models.Report.objects.filter(id=sequence).first()
    if not report:
        return process_response(request, ResponseStatus.REPORT_NOT_EXISTED_ERROR)

    request.data = report.transform_into_serialized_data()

    return process_response(request, ResponseStatus.OK)