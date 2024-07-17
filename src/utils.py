import re
import math
from datetime import datetime

def is_all_items_valid(items):
    """
    Check if items data in a receipt is valid
    Return True if all items are valid based on requirements, otherwise Flase
    """

    for item in items:
        if not isinstance(item, dict):
            return False
        
        shortDescription = item.get("shortDescription")
        price = item.get("price")

        if not shortDescription or not price:
            return False
        if not isinstance(shortDescription, str) or not re.match(r'^[\w\s\-]+$', shortDescription):
            return False
        if not isinstance(price, str) or not re.match(r'^\d+\.\d{2}$', price):
            return False
    return True

def validate_receipt(receipt):
    """
    Validate content of receipt data
    Return Tuple (is_valid, validation_errors)
    """

    validation_errors = []

    if not receipt and not isinstance(receipt, dict):
        return False
    
    retailer = receipt.get('retailer')
    purchaseDate = receipt.get('purchaseDate')
    purchaseTime = receipt.get('purchaseTime')
    items = receipt.get('items')
    total = receipt.get('total')

    if not isinstance(retailer, str) or not re.match(r'^[\w\s\-&]+$', retailer):
        validation_errors.append("Invalid retailer")
    try:
        datetime.strptime(purchaseDate, '%Y-%m-%d')
    except ValueError:
        validation_errors.append("Invalid purchase date")
    try:
        datetime.strptime(purchaseTime, '%H:%M')
    except ValueError:
        validation_errors.append("Invalid purchase time")
    if not isinstance(total, str) or not re.match(r'^\d+\.\d{2}$', total):
        validation_errors.append("Invalid total")
    if not isinstance(items, list) or len(items) == 0 or not is_all_items_valid(items):
        validation_errors.append("Invalid items")
    
    isValid = len(validation_errors) == 0
    return isValid, validation_errors

def calculate_points(receipt):
    """
    Calculate the points for a given receipt based on specified rules.
    Return Integer representing the calculated points
    """
    points = 0
    retailer = receipt.get('retailer', '')
    total = receipt.get('total', '')
    items = receipt.get('items', [])
    purchaseDate = receipt.get('purchaseDate', '')
    purchaseTime = receipt.get('purchaseTime', '')

    # One point for every alphanumeric character in the retailer name.
    points += sum(c.isalnum() for c in retailer)

    # 50 points if the total is a round dollar amount with no cents.
    if float(total).is_integer():
        points += 50
    
    # 25 points if the total is a multiple of 0.25
    if float(total) % 0.25 == 0:
        points += 25
    
    # 5 points for every two items on the receipt
    points += (len(items) // 2) * 5

    # If the trimmed length of the item description is a multiple of 3, 
    # multiply the price by 0.2 and round up to the nearest integer
    item_points = 0
    for item in items:
        description = item.get("shortDescription", "")
        trimmed_description = description.strip()
        if len(trimmed_description) % 3 == 0 and len(description) > 0:
            price = float(item.get("price","0"))
            points +=  math.ceil(price * 0.2)
            item_points += math.ceil(price * 0.2)
    
    # 6 points if the day in the purchase date is odd
    purchaseDate = datetime.strptime(purchaseDate, "%Y-%m-%d")
    if purchaseDate.day % 2 != 0:
        points += 6
    
    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    purchaseTime = datetime.strptime(purchaseTime, "%H:%M")
    if (purchaseTime.hour == 14 and purchaseTime.minute > 0) or (15 <= purchaseTime.hour < 16):
        points += 10
    
    return points