# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from matplotlib import image

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict

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


f = open('./data/pizza_options.json', encoding="utf8")
pizza_data = json.load(f)
class ActionShowPizzaTypes(Action):
    def name(self) -> Text:
        return "action_show_pizza_types"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        buttons = []
        # print(pizza_option_data["Menu"])
        for option in pizza_data['Menu']:
            buttons.append({'title': option['type'],  'payload': '/choose_pizza_type{"pizza_type": "' + option['type'] + '"}'})
        dispatcher.utter_message(text= 'Menu pizza: ', buttons=buttons)
        return []

class ActionShowPizzaFromType(Action):
    def name(self) -> Text:
        return "action_show_pizza_from_type"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        buttons = []
        slot_pizza_type = tracker.get_slot('pizza_type')
        for pizza in pizza_data['Menu']:
            if pizza['type'] == slot_pizza_type:
                for p in pizza['pizza']: 
                    buttons.append({'title': p['name'],  'payload': '/choose_pizza{"pizza": "' + p['name'] + '"}'})
                break
        dispatcher.utter_message(text='các loại pizza {}:'.format(slot_pizza_type), buttons = buttons)
        return[]

class ActionShowPizzaDetail(Action):
    def name(self) -> Text:
        return "action_show_pizza_detail"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        slot_pizza_type = tracker.get_slot('pizza_type')
        for pizza in pizza_data['Menu']:
            if pizza['type'] == slot_pizza_type: 
                for p in pizza['pizza']: 
                    if p['name'] == tracker.get_slot('pizza'):
                            dispatcher.utter_message(image='{}'.format(p['image']))
                            dispatcher.utter_message(text='Mô tả: {}'.format(p['description']))
                            dispatcher.utter_message(text='Giá tiền: {}'.format(p['price']))
                            return[]


class ActionShowPizzaTopping(Action):
    def name(self) -> Text:
        return "action_show_pizza_toppings"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        buttons = []
        for topping in pizza_data['Topping']:
            buttons.append({'title': topping['name'],  'payload': '/choose_topping{"topping": "' + topping['name'] + '"}'})
        dispatcher.utter_message(text='có các loại toppings: ', buttons = buttons)
        return []

class ActionShowPizzaSize(Action):
    def name(self) -> Text:
        return "action_show_pizza_size"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        buttons = []
        for size in pizza_data["Size"]:
            buttons.append({'title' : size['name'], 'payload': '/choose_pizza_size{"pizza_size": "' + size['name'] + '"}'})
        dispatcher.utter_message(text='bạn muốn chọn kích cỡ nào cho pizza của bạn ? ', buttons = buttons)
        return []

class ActionGetUserAddress(Action):
    def name(self) -> Text:
        return "action_get_user_address"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        return []

class ActionShowDrinkOptions(Action):
    def name(self) -> Text:
        return "action_show_drink_options"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        buttons = []
        for drink in pizza_data["Drink"]:
            buttons.append({'title' : drink['name'], 'payload': '/choose_drink{"drink": "' + drink['name'] + '"}'})
        dispatcher.utter_message(text='danh sách đồ uống', buttons = buttons)
        return []

#validate name
class ValidateCustomerForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_customer_form"

    def validate_customer_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Kiểm tra `customer_name` ."""

        # If the name is super short, it might be wrong.
        print(f"Tên được nhập vào = {slot_value} độ dài = {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"Mời nhập lại.")
            return {"customer_name": None}
        else:
            return {"customer_name": slot_value}
    
    def validate_customer_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Kiểm tra `customer_phone` ."""

        # If the name is super short, it might be wrong.
        print(f"SDT = {slot_value} độ dài = {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"Mời nhập lại.")
            return {"customer_phone": None}
        else:
            return {"customer_phone": slot_value}
    
    def validate_customer_address(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Kiểm tra `customer_address` ."""

        # If the name is super short, it might be wrong.
        print(f"Địa chỉ = {slot_value} độ dài = {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"Mời nhập lại.")
            return {"customer_address": None}
        else:
            return {"customer_address": slot_value}

# #validate phone
# class ValidatePhoneForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_customer_phone_form"

# #validate address
# class ValidateAddressForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_customer_address_form"

#GetName
class ActionGetName(Action):
    """Processes Delivery Form"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_customer_name_in_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""
        cus_name = tracker.get_slot("customer_name")
        dispatcher.utter_message(f"Order placed for {cus_name}")
        return [SlotSet("customer_name", cus_name)]

#Get PhoneNumber
class ActionGetPhone(Action):
    """Processes Delivery Form"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_customer_phone_in_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""
        cus_phone = tracker.get_slot("customer_phone")
        dispatcher.utter_message(f"Order placed for {cus_phone}")
        return [SlotSet("customer_phone", cus_phone)]



#validate address
class ValidateAddressForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_customer_address_form"
    def validate_customer_address(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
        ) -> Dict[Text, Any]:
            """Kiểm tra `customer_address` ."""

            # If the name is super short, it might be wrong.
            print(f"Địa chỉ = {slot_value} độ dài = {len(slot_value)}")
            if len(slot_value) <= 2:
                dispatcher.utter_message(text=f"Mời nhập lại.")
                return {"customer_address": None}
            else:
                return {"customer_address": slot_value}    

