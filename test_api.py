"""
Simple test script to verify the API works
Run after starting the server with: uv run python manage.py runserver
"""
import requests
import json

API_URL = "http://localhost:8000/api/analyze/"

# Sample transcript
test_data = {
    "transcript": [
        {
            "timestamp": "2025-10-27T10:00:00Z",
            "role": "assistant",
            "text": "Hola! Me gustaría saber cómo te sientes hoy o si hay algo en particular que te gustaría platicar?"
        },
        {
            "timestamp": "2025-10-27T10:00:05Z",
            "role": "user",
            "text": "Claro, me gustaría contarte sobre mi día y una tarea que tengo que hacer"
        },
        {
            "timestamp": "2025-10-27T10:00:10Z",
            "role": "assistant",
            "text": "Por supuesto, te gustaría dar mas detalles sobre tu día?"
        },
        {
            "timestamp": "2025-10-27T10:15:00Z",
            "role": "user",
            "text": "Si tuve mucha Felicidad cuando me confirmaron un proyecto y comienzo pronto con el nuevo team, ayudame a hacer una lista de pendientes que necesito, podrías darme algun consejo para hacer mejor mis pendientes?, te escribo una lista?"
        },
        {
            "timestamp": "2025-10-27T10:15:30Z",
            "role": "assistant",
            "text": "Felicidades! Son grandes noticias, ahora me podrías compartir sobre la tarea y pendientes que tienes?. "
        }
    ]
}

def test_analyze_endpoint():
    print("Testing /api/analyze/ endpoint...")
    print(f"\nSending request to: {API_URL}")
    print(f"Payload: {json.dumps(test_data, indent=2)}\n")
    
    try:
        response = requests.post(API_URL, json=test_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("\n✅ Test passed! API is working correctly.")
        else:
            print("\n❌ Test failed. Check the response above.")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server.")
        print("Make sure the Django server is running:")
        print("  uv run python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_analyze_endpoint()
