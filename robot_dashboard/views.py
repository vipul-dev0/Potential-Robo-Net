from django.shortcuts import render


def home(request):
    context = {
        'title': 'Potential Robot',
        'tagline': 'Remote control meets autonomous robotics intelligence.',
        'stats': [
            {'label': 'Sensor Nodes', 'value': '1+', 'detail': 'NodeMCU-ready hardware integration'},
            {'label': 'Telemetry', 'value': 'Real-time', 'detail': 'HS-SR04 ultrasonic distance reporting'},
            {'label': 'Control', 'value': 'Dual', 'detail': 'Remote commands + autonomous logic'},
        ],
    }
    return render(request, 'robot_dashboard/home.html', context)
