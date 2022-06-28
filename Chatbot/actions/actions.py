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
import re

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
                            dispatcher.utter_message(text='Mô tả: {}'.format(p['description']), image='{}'.format(p['image']))
                            return[]

class ActionShowPizzaPrice(Action):
    def name(self) -> Text:
        return "action_show_pizza_price"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        slot_pizza_type = tracker.get_slot('pizza_type')
        for pizza in pizza_data['Menu']:
            if pizza['type'] == slot_pizza_type: 
                for p in pizza['pizza']: 
                    if p['name'] == tracker.get_slot('pizza'):
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

# #validate name
class ValidateCustomerForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_customer_info_form"

    def has_numbers(self,inputString):
            return any(char.isdigit() for char in inputString)
    def validate_customer_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Kiểm tra `customer_name` ."""
        # If the name is super short, it might be wrong.
        # print(f"Tên được nhập vào = {slot_value} độ dài = {len(slot_value)}")

        

        if  len(slot_value)>=2 and len(slot_value)<=30 and not self.has_numbers(slot_value):
            # validation success
            return {"customer_name": slot_value}
        else:
            # validation failed, set this slot to None
            dispatcher.utter_message(text=f"tên không hợp lệ mời nhập lại!!")
            return {"customer_name": None} 
    
    def validate_customer_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Kiểm tra `customer_phone` ."""
        # If the name is super short, it might be wrong.
        # print(f"SDT = {slot_value} độ dài = {len(slot_value)}")
        if  len(slot_value)>=10 and slot_value.isdigit():    
            return {"customer_phone": slot_value}
        else:
            dispatcher.utter_message(text=f"số điện thoại không đúng với số điện thoại Việt Nam mời nhập lại!!")
            return {"customer_phone": None}
    
    def validate_customer_address(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Kiểm tra `customer_address` ."""
        # If the name is super short, it might be wrong.
        # print(f"Địa chỉ = {slot_value} độ dài = {len(slot_value)}")
        if len(slot_value) >=5 and self.has_numbers(slot_value) and re.search('[a-zA-Z]', slot_value):
            return {"customer_address": slot_value}
        else:
            dispatcher.utter_message(text=f"địa chỉ không hợp lệ mời nhập lại!!")
            return {"customer_address": None}

# #validate phone
# class ValidatePhoneForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_customer_phone_form"

# #validate address
# class ValidateAddressForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_customer_address_form"

#GetName

class ActionGetCustomerAddress(Action):
    def name(self) -> Text:
        return "action_get_customer_address"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        return [SlotSet("customer_address", tracker.latest_message) ]
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
        if (cus_name != None):
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
        if (cus_phone != None):
            dispatcher.utter_message(f"Order placed for {cus_phone}")
            return [SlotSet("customer_phone", cus_phone)]

class ValidatePhoneNumber(Action):
    def name(self) -> Text:
        return "validate_customer_phone"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        value = tracker.current_slot_values(value,dispatcher,tracker,domain)
        self.validate_customer_phone()

        return []
    def validate_customer_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate phonenumber value."""
        if  len(slot_value)==10 and slot_value.isdecimal():
            # validation success
            return {"customer_phone": slot_value}
        else:
            # validation failed, set this slot to None
            return {"customer_phone": None}

class ValidateCustomerName(Action):
    def name(self) -> Text:
        return "validate_customer_name"
    def has_numbers(inputString):
        return any(char.isdigit() for char in inputString)
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        value = tracker.current_slot_values
        self.validate_customer_name(value,dispatcher,tracker,domain)
        return []
    def validate_customer_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate customer name value."""
        if  len(slot_value)>=2 and len(slot_value)<30 and not self.has_numbers(slot_value):
            # validation success
            return {"customer_name": slot_value}
        else:
            # validation failed, set this slot to None
            return {"customer_name": None} 

   
#validate address
# class ValidateAddressForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_customer_address_form"
#     def validate_customer_address(
#             self,
#             slot_value: Any,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: DomainDict,
#         ) -> Dict[Text, Any]:
#             """Kiểm tra `customer_address` ."""

#             # If the name is super short, it might be wrong.
#             print(f"Địa chỉ = {slot_value} độ dài = {len(slot_value)}")
#             if len(slot_value) <= 2:
#                 dispatcher.utter_message(text=f"Mời nhập lại.")
#                 return {"customer_address": None}
#             else:
#                 return {"customer_address": slot_value}    

class ActionSubmitCustomerInfo(Action):
    def name(self) -> Text:
        return "action_submit_customer_info"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        dispatcher.utter_message('Cảm ơn bạn đã gửi thông tin cho cửa hàng\nMình sẽ gửi đơn hàng của bạn đến cửa hàng pizza RCB gần nhất!!')
        return []
class ActionClearAllCustomerInfo(Action):
    def name(self) -> Text:
        return "action_clear_customer_info"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Xóa thông tin cũ của khách hàng...")
        # return [ 
        #     SlotSet("customer_phone", None), 
        #     SlotSet("customer_name", None), 
        #     SlotSet("customer_address", None), 
        #     SlotSet("redo_form", True)
        #     ]
        return[]
class ActionClearCustomerName(Action):
    def name(self) -> Text:
        return "action_clear_customer_name"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        return [SlotSet("customer_name", None)]
class ActionClearCustomerPhone(Action):
    def name(self) -> Text:
        return "action_clear_customer_phone"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        return [SlotSet("customer_phone", None)]
class ActionClearCustomerAddress(Action):
    def name(self) -> Text:
        return "action_clear_customer_address"
    def run(self, dispatcher: "CollectingDispatcher", tracker: Tracker, domain: "DomainDict") -> List[Dict[Text, Any]]:
        return [SlotSet("customer_address", None)]
