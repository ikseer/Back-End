# from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
# @csrf_exempt
# def predict(request):
#     if request.method == 'POST':
#         try:
#             print(request.bod)
#             array = json.loads(request.body)
#             predicted_disease = get_predicted_value(array)  # Pass the array to text_extraction
#             description, precaution, medication, diet, wrkout = get_all_information(predicted_disease)
#             return JsonResponse({
#                 'predicted_disease': predicted_disease,
#                 'description': description,
#                 'precaution': precaution,
#                 'medication': medication,
#                 'diet': diet,
#                 'workout': wrkout
#             })
#         except (json.JSONDecodeError, KeyError) as e:
#             print(e)
#             return JsonResponse({'error': str(e)}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)
from django.views import View

# Create your views here.
from .RS import get_all_information, get_predicted_value


# @csrf_exempt
# @permission_classes([IsAuthenticated, IsDoctor])
class PredictView(View):
    # permission_classes=[IsAuthenticated, IsDoctor]
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                # print(request.user)
                array = json.loads(request.body)
                predicted_disease = get_predicted_value(array)  # Pass the array to text_extraction
                description, precaution, medication, diet, wrkout = get_all_information(predicted_disease)
                return JsonResponse({
                    'predicted_disease': predicted_disease,
                    'description': description,
                    'precaution': precaution,
                    'medication': medication,
                    'diet': diet,
                    'workout': wrkout
                })
            except (json.JSONDecodeError, KeyError) as e:
                print(e)  # Print error for debugging purposes
                return JsonResponse({'error': str(e)}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
