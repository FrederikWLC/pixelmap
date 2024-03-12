from flask import abort
import requests

class Etherscan:
	def __init__(self, api_key, server="main"):
		self.api_key = api_key
		self.server = server

	def get_transactions_of(self,address,startblock=0,endblock=99999999,sort="asc"):
		src = f"https://api{'-'+self.server if self.server != 'main' else ''}.etherscan.io/api?module=account&action=txlist&address={address}&startblock={startblock}&endblock={endblock}&sort=asc&apikey={self.api_key}"
		response = requests.get(src)
		return response.json()["result"] if int(response.status_code) == 200 else abort(response.status_code)

	def get_api_link_of(self,address,startblock=0,endblock=99999999,sort="asc"):
		return f"https://api{'-'+self.server if self.server != 'main' else ''}.etherscan.io/api?module=account&action=txlist&address={address}&startblock={startblock}&endblock={endblock}&sort=asc&apikey={self.api_key}"

	def get_address_link(self, address):
		return f"https://sepolia.etherscan.io/address/{address}"