
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from mcp_adapter import list_tickets, create_ticket, get_ticket, update_ticket, delete_ticket, get_project_progress

class MCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request = json.loads(post_data)

        method = request.get("method")
        params = request.get("params")
        id = request.get("id")

        if method == "list_tickets":
            result = list_tickets()
        elif method == "create_ticket":
            result = create_ticket(**params)
        elif method == "get_ticket":
            result = get_ticket(**params)
        elif method == "update_ticket":
            result = update_ticket(**params)
        elif method == "delete_ticket":
            result = delete_ticket(**params)
        elif method == "get_project_progress":
            result = get_project_progress(**params)
        else:
            result = {"error": "Method not found"}

        response = {
            "jsonrpc": "2.0",
            "result": result,
            "id": id
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

import os

def run(server_class=HTTPServer, handler_class=MCPHandler):
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting MCP server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
