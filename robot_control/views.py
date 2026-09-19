import json
import urllib.request
import urllib.error
import urllib.parse

from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    """Render the robot control page."""
    return render(request, 'robot_control/index.html')


def proxy_command(request):
    """Proxy a command to the robot's HTTP interface and return its JSON response.

    Expects parameters: 'state' and 'robot_ip' via GET or POST.
    """
    state = request.GET.get('state') or request.POST.get('state')
    robot_ip = request.GET.get('robot_ip') or request.POST.get('robot_ip')
    if not state or not robot_ip:
        return JsonResponse({'error': 'Missing state or robot_ip'}, status=400)

    url = f'http://{robot_ip}/?State={urllib.parse.quote_plus(state)}'
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            body = resp.read().decode(errors='replace')
            try:
                data = json.loads(body)
            except Exception:
                data = {'raw': body}
            return JsonResponse({'ok': True, 'robot': data})
    except urllib.error.URLError as e:
        return JsonResponse({'error': str(e)}, status=502)
