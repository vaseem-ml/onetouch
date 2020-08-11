# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
'''class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "corona_status"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []'''

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa.core.domain import Domain
import requests
import json



class ActionGreetUser(Action):
	def name(self) -> Text:
		return "action_greet_user"

	def run(self,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


		response = "Hello There!!! My name is friday. I am here to provide you information about coronavirus decease. I can tell you current corona status of any country and some safety steps and information."
		dispatcher.utter_message(text=response)
		return []




def _get_country_code(country):
	test_list = [{'india' : 'IN', 'usa' : 'US', 'pakistan' : 'PK'}]

	res = [ sub[country] for sub in test_list ]
	return res[0]
	



def _find_corona_status_by_country(country):

	country_code = _get_country_code(country)
	#print(country_code);
	
	url = 'https://api.thevirustracker.com/free-api?countryTotal={}'.format(country_code)
	response = requests.get(url)
	data = response.text
	parsed = json.loads(data)
	data = parsed['countrydata'][0]
	return data





class CoronaStatus(FormAction):

	def name(self) -> Text:

		return "corona_status"



	@staticmethod
	def required_slots(tracker: Tracker) -> List[Text]:
		"""A list of required slots that the form has to fill"""

		return ["country"]

	'''def validate(self,
				dispatcher: CollectingDispatcher,
				tracker: Tracker,
				domain: Dict[Text, Any]) -> List[Dict]:

		return []'''

	'''def _get_country_code(country):'''




	def submit(
		self,
		dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any],
	) -> List[Dict]:

		country = tracker.get_slot("country")
		#tracker.slots["total_patients"] = "2345"
		#total_patients  = tracker.get_slot("total_patients");
		#print(total_patients)

		'''url = "https://api.thevirustracker.com/free-api?countryTotal=IN"
		response = requests.get(url)
		data = response.text
		parsed = json.loads(data)
		print(parsed)'''

		data = _find_corona_status_by_country(country)
		total_patients = data['total_cases']
		total_recovered = data['total_recovered']
		total_deaths = data['total_deaths']
		newCaseToday = data['total_new_cases_today']
		#TotalNewDeatch = data[]
		#print(data)
		element={
					"custom": {
								"payload": "chart",
								"data":{
									"title":"Corona Patients in india",
									"labels":["Total Patients", "Total Recovered", "Total Death", "New Case Today"],
									"chartsData":[total_patients, total_recovered, total_deaths, newCaseToday],
									"backgrounColor": ["orange", "green","red", "blue"]
								}
							  }
				}

		result = "Total Cases: {}\nTotal Recovered: {}\nTotal Deatch: {}\nNew Case Today: {}".format(total_patients, total_recovered, total_deaths, newCaseToday)
		dispatcher.utter_message(json.dumps(element))
		return []
