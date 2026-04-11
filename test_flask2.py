import sys
sys.path.insert(0, r'd:\fangtang\fangtang')

try:
    from app import app
    result = "Flask app loaded successfully!\n"
    
    with app.test_client() as client:
        resp = client.post('/dify-api/chat-messages',
            data='{"inputs":{},"query":"hello","response_mode":"streaming","user":"test"}',
            content_type='application/json',
            headers={'Authorization': 'Bearer app-l38yBomZ4wAiYktOqJ6kaXfp'})
        result += f"Dify proxy status: {resp.status_code}\n"
        result += f"Response: {resp.data[:500].decode('utf-8', errors='replace')}\n"
except Exception as e:
    result = f"Error: {e}\n"
    import traceback
    result += traceback.format_exc()

with open(r'd:\fangtang\test_result.txt', 'w', encoding='utf-8') as f:
    f.write(result)
