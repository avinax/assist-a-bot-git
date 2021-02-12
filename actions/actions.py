# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
import actions.executions as jira_exec
import requests 
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionCreateIssue(Action):

    def name(self) -> Text:
        return "action_create_issue"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project='DMPP'
        summary='Access to OneDNA Dashboards for ' + str(tracker.get_slot('first_last_name'))
        description='Email ID:' + ' ' + str(tracker.get_slot('email_id'))
        assignee='avimanur0'
        #call create issue api
        issue_id=jira_exec.create_issue(project,summary,description,assignee)
        dispatcher.utter_message(text="Issue created with issue id {}".format(issue_id))

        return []

class ActionShowIssues(Action):

    def name(self) -> Text:
        return "action_show_issues"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        project='DMPP'
        #call show  issues api
        issues=jira_exec.get_issues(project)
        buttons=[]
        for issue in issues:
            payload='/enter_data{"issue_id":"'+issue+'"}'
            buttons.append({"title":issue,"payload":payload})

        dispatcher.utter_message(text="Please select one of the issues for more details",buttons=buttons)
        return []

class ActionShowIssueDetails(Action):

    def name(self) -> Text:
        return "action_show_issue_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project='DMPP'
        issue_id=tracker.get_slot('issue_id')
        print("captured slot {}".format(issue_id))
        #call show  issues api
        issue_details=jira_exec.get_issue_detail(issue_id)
        dispatcher.utter_custom_json(issue_details)
        #dispatcher.utter_message(text="Issue details are as below")
        return []
    
    
class ActionRespondCoroanStateCity(Action):
    def name(self):
      return "action_quick_stats"

    def run(self, dispatcher, tracker, domain):
        # last_message = tracker.latest_message.get("text", "")
        response = requests.get("https://api.covid19india.org/data.json").json()
        print("Length ", len(response["statewise"]))
        message = "Please enter correct STATE name"
        

        entities = tracker.latest_message['entities']
        print("Last Message Now ", entities)
        state = None
        for e in entities:
                if e['entity'] == "state":
                    state = e['value']
        
        print("State ", state) 
        #state = state.lower()     
        print("State ", state) 
        if state == "corona":
            state = "Total"
        if state == "india":
            state = "Total"   

        # print("State ", state.title())   
        message = "Please enter correct STATE name"
        if(state != None):
            message = "Please enter correct STATE name"
            for data in response["statewise"]:
                if data["state"] == state.title():
                    print(data)
                    message = "Active: "+data["active"] +" Confirmed: " + data["confirmed"] +" Recovered: " + data["recovered"] +" On "+data["lastupdatedtime"]

        dispatcher.utter_message(message)
        return []
    

class ActionRespondCoroanStateCity_insights(Action):
    def name(self):
      return "action_quick_insights"

    def run(self, dispatcher, tracker, domain):
        # last_message = tracker.latest_message.get("text", "")
        response = requests.get("https://api.covid19india.org/data.json").json()
        print("Length ", len(response["statewise"]))
        message = "Please enter correct STATE name"
        

        entities = tracker.latest_message['entities']
        print("Last Message Now ", entities)
        state = None
        for e in entities:
                if e['entity'] == "state":
                    state = e['value']
        
        print("State ", state) 
        #state = state.lower()     
        print("State ", state) 
        if state == "corona":
            state = "Total"
        if state == "india":
            state = "Total"   

        # print("State ", state.title())   
        message = "Please enter correct STATE name"
        if(state != None):
            message = "Please enter correct STATE name"
            for data in response["statewise"]:
                if data["state"] == state.title():
                    print(data)
                    message = "Quick_Insights : "+data["statenotes"]
        dispatcher.utter_message(message)
        return []   