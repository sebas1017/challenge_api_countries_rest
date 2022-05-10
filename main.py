import http.server
import socketserver
import json 
import requests
import pandas as pd 
import sqlite3
import time
import random
import os
import hashlib
import os


# Defining a HTTP request Handler class
class ServiceHandler(http.server.SimpleHTTPRequestHandler):
	# GET Method Defination
	def do_GET(self):
		if self.path == "/":
			# defining all the headers
			self.send_response(200)
			self.send_header('Content-type','application/json')
			self.end_headers()

			url = "https://restcountries.com/v3.1/all"
			url_countries_by_region = "https://restcountries.com/v3.1/region/{region}"

			headers = {
				'x-rapidapi-key': "921cfc17abmsh42834139575656fp12725cjsn8ce3ad10333d",
				'x-rapidapi-host': "restcountries-v1.p.rapidapi.com"
				}
			regions_data = []
			hash_languages =[]
			countries = []
			times=[]
			count_errors = 0
			data  = json.loads(requests.request("GET", url, headers=headers).text)
			try: 
				for information in data:
					if information["region"]  and not information["region"]  in regions_data:
						regions_data.append(information["region"])
						# only the different existing regions


				for region in regions_data:
					start_time = time.time()
					#We wait 2 seconds before making the next request to avoid ip blocks in the API
					time.sleep(2)
					response_by_region = json.loads(
						requests.request("GET", url_countries_by_region.format(region=region), headers=headers).text
					)
					# we consult the data requested by region
					country_option = random.randint(0,len(response_by_region)-1)
					countries.append(response_by_region[country_option]['name']['common'])
					key_language =  list(response_by_region[country_option]['languages'].keys())[0]
					hash_languages.append(hashlib.sha1(response_by_region[country_option]['languages'][str(key_language)].encode()).hexdigest())
					end_time = time.time()
					times.append(round((end_time-start_time)*1000,2))
			except KeyError as e:
				count_errors+=1
				data = {"message":"Error en API externa de paises recargar nuevamente"}
				with open('data.json', 'w', encoding='utf-8') as f:
					json.dump(data, f, ensure_ascii=False, indent=4)
				error_information = self.json_read()
				self.wfile.write(json.dumps(error_information).encode())
			if count_errors == 0:
				df = pd.DataFrame({
					"Region": regions_data,
					"Country": countries,
					"Language SHA1": hash_languages,
					"Time [ms]": times
				})


				statistics = {}
				statistics['total'] = df['Time [ms]'].sum()
				statistics['mean'] = df['Time [ms]'].mean()
				statistics['min'] = df['Time [ms]'].min()
				statistics['max'] = df['Time [ms]'].max()
				#  we build a dataframe and a data.json file with the results of the algorithm
				df.to_json(path_or_buf='data.json')
				# here we can return the answer in html format but I decided to leave the answer in json format
				data_information = self.json_read()
				self.insert_data(statistics)
				self.wfile.write(json.dumps(data_information).encode())

	def json_read(self):
		script_dir = os.path.dirname(__file__) # <-- absolute dir the script 
		rel_path = "data.json"
		abs_file_path = os.path.join(script_dir, rel_path)
		# open json file and give it to data variable as a dictionary
		with open(abs_file_path) as data_file:
			data_information = json.load(data_file)
		return data_information

	def insert_data(self,statistics):
		
		init_query = (f"""
						CREATE TABLE IF NOT EXISTS challenge_tangelo (
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						total_time REAL NOT NULL,
						mean_time REAL NOT NULL,
						min_time REAL NOT NULL,
						max_time REAL NOT NULL
						);
						INSERT INTO challenge_tangelo (total_time, mean_time, min_time, max_time)
						VALUES ({statistics['total']}, {statistics['mean']}, {statistics['min']}, {statistics['max']});""")
		
		
		script_dir_db = os.path.dirname(__file__) # <-- absolute dir the script 
		rel_path_db = "instance/tangelo_challenge.sqlite"
		abs_file_path_db = os.path.join(script_dir_db, rel_path_db)
		try:
			connection = sqlite3.connect(abs_file_path_db)
			cursor = connection.cursor()
			print("Successfully Connected to SQLite")
			cursor.executescript(init_query)
			print("FINISHED")
			cursor.close()

		except sqlite3.Error as error:
			print("Error while connecting to sqlite", error)
		finally:
			if (connection):
				connection.close()
				print("The SQLite connection is closed")


class ReuseAddrTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

PORT = int(os.environ.get('PORT', 8000))
myserver = ReuseAddrTCPServer(("",PORT),ServiceHandler)
myserver.daemon_threads = True
print(f"Server Started at http://127.0.0.1:{PORT}/" )
try:
    myserver.serve_forever()
except:
    print ("Closing the server.")
    myserver.server_close()
	
