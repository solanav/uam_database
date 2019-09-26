# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pprint import pprint
import time
import json
from tabulate import tabulate

hostName = "localhost"
serverPort = 8080

top_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <title>UAM DATABASE</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</head>
<body>
<style>
@media (min-width: 34em) {
    .card-columns {
        -webkit-column-count: 2;
        -moz-column-count: 2;
        column-count: 2;
    }
}

@media (min-width: 48em) {
    .card-columns {
        -webkit-column-count: 3;
        -moz-column-count: 3;
        column-count: 3;
    }
}

@media (min-width: 62em) {
    .card-columns {
        -webkit-column-count: 4;
        -moz-column-count: 4;
        column-count: 4;
    }
}

@media (min-width: 75em) {
    .card-columns {
        -webkit-column-count: 5;
        -moz-column-count: 5;
        column-count: 5;
    }
}
</style>
<div class="jumbotron">
    <a href="http://localhost:8080" style="color:black;text-decoration: none;"><h1>UAM Database</h1></a>
    <p>Log in to your moodle in other window to get images.</p>
</div>

<div class="card-columns">"""

card_html = '<div class="card"><img class="card-img-top" src="'
card_html2 = '" alt="Card image"><div class="card-body"><h6 class="card-title">'
card_html3 = '</h6></div></div>'

main_html = """</div>
<div class="container">
<form action="/give_me_action.php">
<div class="form-group">
<label for="text">Nombre:</label>
<input type="text" class="form-control style="width=30%" name="f">
</div>
<div class="form-group">
<label for="text">Apellido:</label>
<input type="text" class="form-control" style="width=30%" name="l">
</div>
<button type="submit" class="btn btn-primary">Search</button>
</form>
</div>"""

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes(top_html, "utf-8"))
        o = urlparse(self.path)

        if self.path != '/':
            query = parse_qs(o.query)

            try:
                name = ''.join(query['f']).lower()
            except:
                name = ""
            
            try:
                surname = ''.join(query['l']).lower()
            except:
                surname = ""

            results = {}

            with open("users.json") as user_list:
                data = json.load(user_list)
                sorted_data = sorted(data['users'], key=lambda kv:kv['surname'])
                for result in sorted_data:
                    other_id = result['id']
                    other_name = result['name'].lower()
                    other_surname = result['surname'].lower()

                    if (name and surname and name in other_name and surname in other_surname):
                        results[other_id] = [other_name.title(), other_surname.title(), result['image']]
                    elif (name and not surname and name in other_name):
                        results[other_id] = [other_name.title(), other_surname.title(), result['image']]
                    elif (not name and surname and surname in other_surname):
                        results[other_id] = [other_name.title(), other_surname.title(), result['image']]

            i = 0
            for line in results.items():
                self.wfile.write(bytes(card_html, "utf-8"))
                self.wfile.write(bytes(line[1][2], "utf-8"))
                self.wfile.write(bytes(card_html2, "utf-8"))
                self.wfile.write(bytes(line[1][0] + " " + line[1][1], "utf-8"))
                self.wfile.write(bytes(card_html3, "utf-8"))

                if (i >= 1000<z):
                    break
                
                i += 1

        else:
            self.wfile.write(bytes(main_html, "utf-8"))
        
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")