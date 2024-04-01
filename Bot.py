import json
import datetime
import time

def validate(slots):
    
    if not slots['Name']:
       
        return{
            'isValid': False,
            'violatedSlot': 'Name'
            
        }

    valid_cities = ['mumbai','delhi','banglore','nagpur','bhubaneswar']
    
    if not slots['Location']:
        print("Inside Empty Location")
        return {
        'isValid': False,
        'violatedSlot': 'Location'
        }        
        
    if slots['Location']['value']['originalValue'].lower() not in  valid_cities:
        
        print("Not Valid location")
        
        return {
        'isValid': False,
        'violatedSlot': 'Location',
        'message': 'We currently  support only {} as a valid destination.'.format(", ".join(valid_cities))
        }
        
    if not slots['CheckInDate']:
        
        return {
        'isValid': False,
        'violatedSlot': 'CheckInDate',
    }
        
    if not slots['Nights']:
        return {
        'isValid': False,
        'violatedSlot': 'Nights'
    }
        
    if not slots['RoomType']:
        return {
        'isValid': False,
        'violatedSlot': 'RoomType'
    }

    return {'isValid': True}
    
def lambda_handler(event, context):
    
  
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event['invocationSource'])
    print(slots)
    print(intent)
    validation_result = validate(event['sessionState']['intent']['slots'])
    print(validation_result)
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            
            if 'message' in validation_result:
            
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                        }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": validation_result['message']
                    }
                ]
               } 
            else:
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                        }
                }
               } 
    
            return response
           
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name':intent,
                    'slots': slots
                    
                    }
        
            }
        }
            return response
    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        
        
        response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name':intent,
                'slots': slots,
                'state':'Fulfilled'
                
                }
    
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Your resevation has been made. \nHave a Wonderfull Day \nFeel free to reach us at info@hotelbisleri.com or +91 9898985167 "
            }
        ]
    }
            
        return response