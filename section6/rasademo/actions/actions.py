# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

#from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


"""class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World!")

         return []"""

class ActionOrderPizza(Action):

     def name(self):
         return "action_order_pizza"

     def run(self, dispatcher=CollectingDispatcher,
             tracker=Tracker,
             domain=None):
         """
         # Add any action commands here to place the order in your system
         """
         """toppings = tracker.slots.get('topping')
         print(toppings)
         #dispatcher.utter_message(text="Your order has been placed!")
         if len(toppings) > 1:
             toppings_confirmed = ", ".join(toppings[0:-1]) + " and " + toppings[-1]
         else:
             toppings_confirmed = toppingss[0]"""
         return []#[SlotSet('toppings_confirmed', toppings_confirmed)]
