import sys
sys.path.insert(0, r'd:\fangtang\fangtang')

try:
    from app import app
    print("Flask app loaded successfully!")
    
    with app.test_client() as client:
        resp = client.post('/dify-api/chat-messages',
            data='{"inputs":{},"query":"hello","response_mode":"streaming","user":"test"}',
            content_type='application/json',
            headers={'Authorization': 'Bearer app-l38yBomZ4wAiYktOqJ6kaXfp'})
        print(f"Dify proxy status: {resp.status_code}")
        print(f"Response: {resp.data[:500]}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
