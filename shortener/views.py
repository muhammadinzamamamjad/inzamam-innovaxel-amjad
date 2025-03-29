import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import ShortURL
from django.shortcuts import redirect
@csrf_exempt
def create_short_url(request):
    """
    POST /shorten/
    Body: {"url": "https://www.example.com/some/long/url"}
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            original_url = data.get('url')
            if not original_url:
                return HttpResponseBadRequest(json.dumps({"error": "URL is required"}), content_type="application/json")

            short_url_obj = ShortURL.objects.create(url=original_url)
            response_data = {
                "id": str(short_url_obj.id),
                "url": short_url_obj.url,
                "shortCode": short_url_obj.shortCode,
                "createdAt": short_url_obj.createdAt.isoformat(),
                "updatedAt": short_url_obj.updatedAt.isoformat()
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({"error": str(e)}), content_type="application/json")

    return HttpResponseBadRequest(json.dumps({"error": "Invalid method"}), content_type="application/json")


def retrieve_original_url(request, short_code):
    """
    GET /shorten/<short_code>/
    """
    if request.method == 'GET':
        try:
            short_url_obj = ShortURL.objects.get(shortCode=short_code)
            # Increase access count whenever URL is retrieved
            short_url_obj.accessCount += 1
            short_url_obj.save()

            response_data = {
                "id": str(short_url_obj.id),
                "url": short_url_obj.url,
                "shortCode": short_url_obj.shortCode,
                "createdAt": short_url_obj.createdAt.isoformat(),
                "updatedAt": short_url_obj.updatedAt.isoformat()
            }
            return JsonResponse(response_data, status=200)
        except ShortURL.DoesNotExist:
            return HttpResponseNotFound(json.dumps({"error": "Short URL not found"}), content_type="application/json")

    return HttpResponseBadRequest(json.dumps({"error": "Invalid method"}), content_type="application/json")


@csrf_exempt
def update_short_url(request, short_code):
    """
    PUT /shorten/<short_code>/update/
    Body: {"url": "https://www.example.com/some/updated/url"}
    """
    if request.method == 'PUT':
        try:
            short_url_obj = ShortURL.objects.get(shortCode=short_code)
            data = json.loads(request.body)
            updated_url = data.get('url')
            if not updated_url:
                return HttpResponseBadRequest(json.dumps({"error": "URL is required"}), content_type="application/json")

            short_url_obj.url = updated_url
            short_url_obj.save()

            response_data = {
                "id": str(short_url_obj.id),
                "url": short_url_obj.url,
                "shortCode": short_url_obj.shortCode,
                "createdAt": short_url_obj.createdAt.isoformat(),
                "updatedAt": short_url_obj.updatedAt.isoformat()
            }
            return JsonResponse(response_data, status=200)
        except ShortURL.DoesNotExist:
            return HttpResponseNotFound(json.dumps({"error": "Short URL not found"}), content_type="application/json")
        except Exception as e:
            return HttpResponseBadRequest(json.dumps({"error": str(e)}), content_type="application/json")

    return HttpResponseBadRequest(json.dumps({"error": "Invalid method"}), content_type="application/json")


@csrf_exempt
def delete_short_url(request, short_code):
    """
    DELETE /shorten/<short_code>/delete/
    """
    if request.method == 'DELETE':
        try:
            short_url_obj = ShortURL.objects.get(shortCode=short_code)
            short_url_obj.delete()
            # Return 204 No Content
            return JsonResponse({}, status=204)
        except ShortURL.DoesNotExist:
            return HttpResponseNotFound(json.dumps({"error": "Short URL not found"}), content_type="application/json")

    return HttpResponseBadRequest(json.dumps({"error": "Invalid method"}), content_type="application/json")



def redirect_url(request, short_code):
    """
    Redirect the user to the original URL based on the short code.
    """
    try:
        short_url_obj = ShortURL.objects.get(shortCode=short_code)
        short_url_obj.accessCount += 1  # Increment access count
        short_url_obj.save()  # Save the updated access count
        return redirect(short_url_obj.url)  # Redirect to the original URL
    except ShortURL.DoesNotExist:
        return HttpResponseNotFound("Short URL not found.")

def get_url_statistics(request, short_code):
    """
    GET /shorten/<short_code>/stats/
    """
    if request.method == 'GET':
        try:
            short_url_obj = ShortURL.objects.get(shortCode=short_code)
            response_data = {
                "id": str(short_url_obj.id),
                "url": short_url_obj.url,
                "shortCode": short_url_obj.shortCode,
                "createdAt": short_url_obj.createdAt.isoformat(),
                "updatedAt": short_url_obj.updatedAt.isoformat(),
                "accessCount": short_url_obj.accessCount
            }
            return JsonResponse(response_data, status=200)
        except ShortURL.DoesNotExist:
            return HttpResponseNotFound(json.dumps({"error": "Short URL not found"}), content_type="application/json")

    return HttpResponseBadRequest(json.dumps({"error": "Invalid method"}), content_type="application/json")
