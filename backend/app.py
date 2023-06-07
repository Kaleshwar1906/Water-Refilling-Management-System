from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify

# jsonify will convert array to json


app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["watermanagement"]

CORS(app)  # prevent cors error


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users/employees", methods=["GET"])
def empdata():
    # data = db["employee"].find_one({"fname":"Raj"})
    allData = db["employee"].find()
    dataJson = []
    for data in allData:
        id = data["_id"]

        dataDict = {
            "id": str(id),
            "fname": data["fname"],
            "lname": data["lname"],
            "gender": data["gender"],
            "contact": data["contact"],
            "email": data["email"],
            "address": data["address"],
            "uname": data["uname"],
            "type": data["type"],
        }

        dataJson.append(dataDict)
    return jsonify(dataJson)


@app.route("/users/addEmp/<string:val>", methods=["POST"])
def addEmp(val):
    emp = eval(val)
    emp["_id"] = emp.pop("id")
    emp["_id"] = int(emp["_id"])
    emp["password"] = "password"
    # print(emp)
    db["employee"].insert_one(emp)
    return "Success"


@app.route("/users/editEmp/<string:val>", methods=["PUT"])
def editEmp(val):
    emp = eval(val)
    emp["_id"] = emp.pop("id")
    emp["_id"] = int(emp["_id"])
    # emp["password"] = "password"
    # print(emp)
    db["employee"].update_one(
        {"_id": emp["_id"]},
        {
            "$set": {
                "fname": emp["fname"],
                "lname": emp["lname"],
                "email": emp["email"],
                "type": emp["type"],
                "address": emp["address"],
                "contact": emp["contact"],
            },
        },
    )
    return "Success"


@app.route("/users/addCust/<string:val>", methods=["POST"])
def addCust(val):
    emp = eval(val)
    emp["_id"] = emp.pop("id")
    emp["_id"] = int(emp["_id"])
    emp["password"] = "password"
    # print(emp)
    db["customer"].insert_one(emp)
    return "Success"


@app.route("/users/editCust/<string:val>", methods=["PUT"])
def editCust(val):
    emp = eval(val)
    emp["_id"] = emp.pop("id")
    emp["_id"] = int(emp["_id"])
    # emp["password"] = "password"
    # print(emp)
    db["customer"].update_one(
        {"_id": emp["_id"]},
        {
            "$set": {
                "fname": emp["fname"],
                "lname": emp["lname"],
                "email": emp["email"],
                "address": emp["address"],
                "contact": emp["contact"],
            },
        },
    )
    return "Success"


@app.route("/users/deleteEmp/<int:id>", methods=["DELETE"])
def deleteEmp(id):
    db["employee"].delete_one({"_id": id})
    return "Success"


@app.route("/users/deleteCust/<int:id>", methods=["DELETE"])
def deleteCust(id):
    db["customer"].delete_one({"_id": id})
    return "Success"


@app.route("/users", methods=["POST", "GET"])
def data():
    if request.method == "POST":
        body = request.json
        firstName = body["firstName"]
        lastName = body["lastName"]
        emailId = body["emailId"]

        db["users"].insert_one(
            {"firstName": firstName, "lastName": lastName, "emailId": emailId}
        )

        return jsonify(
            {
                "status": "Successsss posting data to mongo",
                "firstName": firstName,
                "lastName": lastName,
                "emailId": emailId,
            }
        )

    if request.method == "GET":
        allData = db["customer"].find()
        dataJson = []
        for data in allData:
            id = data["_id"]
            dataDict = {
                "id": str(id),
                "fname": data["fname"],
                "lname": data["lname"],
                "gender": data["gender"],
                "contact": data["contact"],
                "email": data["email"],
                "address": data["address"],
                "uname": data["uname"],
                # "type": data["type"],
            }

            dataJson.append(dataDict)
        return jsonify(dataJson)


@app.route("/users/container", methods=["GET"])
def containerData():
    allData = db["container"].find()
    dataJson = []
    for data in allData:
        id = data["_id"]

        dataDict = {
            "id": str(id),
            "quantity": data["quantity"],
            "quantity_left": data["quantity_left"],
            "threshold": data["threshold"],
        }

        dataJson.append(dataDict)
    return jsonify(dataJson)


@app.route("/users/container/<int:val>", methods=["PUT"])
def updateContainer(val):
    # print(val,"HIIIIIIIIIIIIIIIIIIIIIIIII")
    # print(type(val))
    db["container"].update_one(
        {"_id": 1},
        {
            "$set": {"quantity_left": val},
        },
    )
    return "Updated Container"


@app.route("/users/getProducts", methods=["GET"])
def getProducts():
    allData = db["products"].find()
    dataJson = []
    for data in allData:
        id = data["_id"]
        dataDict = {
            "id": id,
            "name": data["name"],
            "imageSrc": data["imageSrc"],
            "imageAlt": data["imageAlt"],
            "price": data["price"],
        }
        dataJson.append(dataDict)
    # print(dataJson)
    return jsonify(dataJson)


@app.route("/users/getReviews", methods=["GET"])
def getReviews():
    allData = db["reviews"].find()
    dataJson = []
    for data in allData:
        cust = db["customer"].find_one(
            {"_id": data["customer_id"]}, {"fname", "lname", "email", "gender"}
        )
        # print(cust)
        dataDict = {
            "_id": str(data["_id"]),
            "review": data["review"],
            "name": cust["fname"] + " " + cust["lname"],
            "email": cust["email"],
            "gender": cust["gender"],
        }
        dataJson.append(dataDict)
    return jsonify(dataJson)


@app.route("/users/addReview/<int:id>/<string:review>", methods=["POST"])
def addReview(id, review):
    # print(review)
    rev = {"review": review, "customer_id": id}
    db["reviews"].insert_one(rev)
    return "Success"


@app.route("/users/saveOrders/<int:id>/<string:val>/<int:price>", methods=["POST"])
def saveOrders(id, val, price):
    orders = eval(val)
    qty = 0
    for order in orders:
        # print(order["qty"]*order["id"])
        qty += order["qty"] * order["id"]
    wall = db["wallet"].find_one({"customer_id": id})
    qtyl = db["container"].find_one({"_id": 1})
    if wall is None:
        db["wallet"].insert_one({"customer_id": id, "amount": 0})
    else:
        if price > wall["amount"]:
            return "false"
        else:
            db["wallet"].update_one(
                {"customer_id": id}, {"$set": {"amount": wall["amount"] - price}}
            )
            d = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            db["transactions"].insert_one(
                {
                    "customer_id": id,
                    "products": orders,
                    "date": d,
                    "amount": price,
                }
            )
            temp = db["transactions"].find_one({"date": d})
            db["payments"].insert_one(
                {
                    "transaction_id": temp["_id"],
                    "customer_id": id,
                    "to": "HYDRA .TE",
                    "date": d,
                    "amount": price,
                }
            )
            db["container"].update_one(
                {"_id": 1}, {"$set": {"quantity_left": qtyl["quantity_left"] - qty}}
            )
            temp1 = db["customer"].find_one({"_id": id})
            db["delivery"].insert_one(
                {
                    "date": d,
                    "transaction_id": temp["_id"],
                    "employee_id": 0,
                    "employee_name": "NA",
                    "customer_id": id,
                    "customer_name": temp1["fname"] + " " + temp1["lname"],
                    "address": temp1["address"],
                    "quantity": qty,
                    "amount": price,
                    "delivered": "no",
                    "delivered_on": "",
                }
            )
            return "true"
    return "Success"


@app.route("/users/delivery", methods=["GET"])
def delivery():
    allData = db["delivery"].find()
    dataJson = []
    for data in allData:
        # print(data["_id"])
        dataDict = {
            "id": str(data["_id"]),
            "date": data["date"],
            "employee_id": data["employee_id"],
            "employee_name": data["employee_name"],
            "transaction_id": str(data["transaction_id"]),
            "customer_id": data["customer_id"],
            "customer_name": data["customer_name"],
            "address": data["address"],
            "quantity": data["quantity"],
            "amount": data["amount"],
            "delivered": data["delivered"],
            "delivered_on": data["delivered_on"],
        }
        dataJson.append(dataDict)
    return jsonify(dataJson)


@app.route("/users/deliverypersons", methods=["GET"])
def deliveryPersons():
    allData = db["employee"].find({"type": "delivery"})
    dataJson = []
    for data in allData:
        dataDict = {"id": data["_id"], "name": data["fname"] + " " + data["lname"]}
        dataJson.append(dataDict)
    return jsonify(dataJson)


@app.route("/users/setdelivery/<string:id>/<int:eid>/<string:ename>", methods=["PUT"])
def setDelivery(id, eid, ename):
    # print(id, eid, ename)
    db["delivery"].update_one(
        {"_id": ObjectId(id)}, {"$set": {"employee_id": eid, "employee_name": ename}}
    )
    # print(db["delivery"].find_one({"employee_id": eid}))
    return "Success"


@app.route("/users/setdelivery/<string:id>/<string:val>", methods=["PUT"])
def deliveryYes(id, val):
    # print(id,eid,ename)
    if val == "yes":
        db["delivery"].update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "delivered": "yes",
                    "delivered_on": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                }
            },
        )
    else:
        db["delivery"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {"employee_id": "", "employee_name": "NA"}},
        )
    # print(db["delivery"].find_one({"employee_id": eid}))
    return "Success"


@app.route("/users/checkSubscription/<int:id>", methods=["GET"])
def checkSubscribe(id):
    temp = db["subscriptionUsers"].find_one({"customer_id": id})
    if temp:
        return temp["plan"]
    else:
        return "NONE"


@app.route("/users/deleteSubscription/<int:id>", methods=["DELETE"])
def deleteSubscribe(id):
    db["subscriptionUsers"].delete_one({"customer_id": id})
    return "SUCCESS"


@app.route("/users/subscribe/<int:id>/<string:name>", methods=["POST"])
def subscribe(id, name):
    qtyl = db["container"].find_one({"_id": 1})
    price = 0
    orders = []
    qty = 0
    if name == "Hydrate Every Day":
        price = 500
        qty = 100
        orders = [{"id": 20, "name": "20 liters", "price": 50, "qty": 10}]
    if name == "Hydrate Regularly":
        qty = 500
        price = 1000
        orders = [{"id": 50, "name": "50 liters", "price": 100, "qty": 10}]
    temp = db["subscriptionUsers"].find_one({"customer_id": id})
    if temp:
        db["subscriptionUsers"].update_one(
            {"customer_id": id},
            {
                "$set": {
                    "plan": name,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                }
            },
        )
    else:
        db["subscriptionUsers"].insert_one(
            {
                "customer_id": id,
                "plan": name,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )
    wall = db["wallet"].find_one({"customer_id": id})
    db["transactions"].insert_one(
        {
            "customer_id": id,
            "products": orders,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "amount": price,
        }
    )
    d = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    temp = db["transactions"].find_one({"date": d})
    db["payments"].insert_one(
        {
            "transaction_id": temp["_id"],
            "customer_id": id,
            "to": "HYDRA .TE",
            "date": d,
            "amount": price,
        }
    )
    db["container"].update_one(
        {"_id": 1}, {"$set": {"quantity_left": qtyl["quantity_left"] - qty}}
    )
    temp1 = db["customer"].find_one({"_id": id})
    db["delivery"].insert_one(
        {
            "date": d,
            "transaction_id": temp["_id"],
            "employee_id": 0,
            "employee_name": "NA",
            "customer_id": id,
            "customer_name": temp1["fname"] + " " + temp1["lname"],
            "address": temp1["address"],
            "quantity": qty,
            "amount": price,
            "delivered": "no",
            "delivered_on":""
        }
    )
    db["wallet"].update_one(
        {"customer_id": id}, {"$set": {"amount": wall["amount"] - price}}
    )
    return "Success"


@app.route("/users/getRechargeHistory", methods=["GET"])
def getRehargeHistory():
    allData = db["recharge"].find()
    dataJson = []
    for data in allData:
        temp = db["customer"].find_one({"_id": data["customer_id"]})
        wall = db["wallet"].find_one({"customer_id": data["customer_id"]})
        dataDict = {
            "id": str(data["_id"]),
            "customer_id": data["customer_id"],
            "name": temp["fname"] + " " + temp["lname"],
            "date": data["date"],
            "amount": data["amount"],
            "bal": wall["amount"],
            "status": data["status"],
        }
        dataJson.append(dataDict)
    # print(dataJson)
    return jsonify(dataJson)


@app.route("/users/getBalance/<int:id>", methods=["GET"])
def getBalance(id):
    wall = db["wallet"].find_one({"customer_id": id})
    if wall is None:
        db["wallet"].insert_one({"customer_id": id, "amount": 0})
    else:
        return str(wall["amount"])
    return "Success"


@app.route("/users/setBalance/<int:id>/<int:amt>/<int:rech>", methods=["PUT"])
def setBalance(id, amt, rech):
    # print(amt)
    db["wallet"].update_one({"customer_id": id}, {"$set": {"amount": amt}})
    db["recharge"].insert_one(
        {
            "customer_id": id,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "amount": rech,
            "status": "Success",
        }
    )
    return "Success"


@app.route("/users/getPayments", methods=["GET"])
def getPayments():
    allData = db["payments"].find()
    dataJson = []
    for data in allData:
        t = db["customer"].find_one({"_id": data["customer_id"]})
        name = t["fname"] + " " + t["lname"]
        dataDict = {
            "id": str(data["_id"]),
            "transaction_id": str(data["transaction_id"]),
            "customer_id": data["customer_id"],
            "name": name,
            "to": data["to"],
            "date": data["date"][:10],
            "time": data["date"][11:],
            "amount": data["amount"],
            "status": "Success",
        }
        dataJson.append(dataDict)
    return jsonify(dataJson)


@app.route("/users/getRecharge/<int:id>", methods=["GET"])
def getRecharge(id):
    # print(id)
    temp = db["recharge"].find({"customer_id": id})
    dataJson = []
    for data in temp:
        dataDict = {
            "id": str(data["_id"]),
            "date": data["date"][:10],
            "time": data["date"][11:],
            "amount": data["amount"],
            "status": data["status"],
        }
        dataJson.append(dataDict)
    # print(dataJson)
    return jsonify(dataJson)


@app.route("/users/getTransactions/<int:id>", methods=["GET"])
def getTransactions(id):
    # print(id)
    temp = db["transactions"].find({"customer_id": id})
    dataJson = []
    for data in temp:
        dataDict = {
            "id": str(data["_id"]),
            "products": data["products"],
            "date": data["date"][:10],
            "time": data["date"][11:],
            "amount": data["amount"],
        }
        dataJson.append(dataDict)
    # print(dataJson)
    return jsonify(dataJson)


@app.route("/users/getTransactions", methods=["GET"])
def getAllTransactions():
    # print("Hellop")
    temp = db["transactions"].find()
    dataJson = []
    for data in temp:
        t = db["customer"].find_one({"_id": data["customer_id"]})
        name = t["fname"] + " " + t["lname"]
        dataDict = {
            "id": str(data["_id"]),
            "customer_id": data["customer_id"],
            "name": name,
            "products": data["products"],
            "date": data["date"][:10],
            "time": data["date"][11:],
            "amount": data["amount"],
        }
        dataJson.append(dataDict)
    # print(dataJson)
    return jsonify(dataJson)


@app.route("/users/getSubscriptions", methods=["GET"])
def getSubscriptions():
    # print("Hellop")
    temp = db["subscriptions"].find()
    dataJson = []
    for data in temp:
        dataDict = {
            "id": str(data["_id"]),
            "name": data["name"],
            "src": data["src"],
            "alt": data["alt"],
            "title": data["title"],
            "desc": data["desc"],
            "price": data["price"],
        }
        dataJson.append(dataDict)
    # print(dataJson)
    return jsonify(dataJson)


@app.route("/users/<string:id>", methods=["POST", "GET", "PUT", "DELETE"])
def onedata(id):
    if request.method == "GET":
        role = id[6:]
        data = db[role].find_one({"_id": int(id[0:6])})
        # id = data['_id']
        # fname = data['fname']
        # lname = data['lname']
        # email = data['email']

        # dataDict = {
        #         "id" : data['_id'],
        #         "fname":data['fname'],
        #         "lname" : data['lname'],
        #         "email" : data['email'],
        #         "contact" : data['contact'],
        #         "gender" : data['gender'],
        #         "uname" : data['uname'],
        #         "password" : data['password']
        #     }
        return data

    if request.method == "DELETE":
        db["users"].delete_one({"_id": ObjectId(id)})
        return jsonify({"status": "Deleted successfully" + id})

    if request.method == "PUT":
        body = request.json
        firstName = body["firstName"]
        lastName = body["lastName"]
        emailId = body["emailId"]

        db["users"].update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "firstName": firstName,
                    "lastName": lastName,
                    "emailId": emailId,
                }
            },
        )


@app.route("/users/statistics", methods=["GET"])
def statistics():
    c_count = db["customer"].count_documents({})
    # e_count=db["employee"].count_documents({})
    amount = 0
    for doc in db["transactions"].aggregate(
        [{"$group": {"_id": 0, "sum_val": {"$sum": "$amount"}}}]
    ):
        amount = doc["sum_val"]
    pipeline1 = [
        {"$unwind": "$products"},
        {
            "$group": {
                "_id": None,
                "qty": {"$sum": {"$multiply": ["$products.qty", "$products.id"]}},
            }
        },
    ]
    pipeline2 = [
        {"$unwind": "$products"},
        {"$group": {"_id": None, "cont": {"$sum": "$products.qty"}}},
    ]
    # for doc in db["transactions"].aggregate([{"$project":{"qty":{"$sum":"$products.qty*$product.id"}}}]):
    #     qty = doc["qty"]
    qty = list(db["transactions"].aggregate(pipeline1))
    cont = list(db["transactions"].aggregate(pipeline2))
    # print(res[0]["qty"])
    trans = db["transactions"].find().limit(4)
    temp1 = []
    for doc in trans:
        dic = {"id": doc["customer_id"], "amount": doc["amount"]}
        temp1.append(dic)

    trans = db["recharge"].find().limit(4)
    # trans = db["recharge"].find().sort({ "_id": -1 }).limit(4)
    temp2 = []
    for doc in trans:
        dic = {"id": doc["customer_id"], "amount": doc["amount"]}
        temp2.append(dic)

    trans = db["wallet"].find().limit(4)
    temp3 = []
    for doc in trans:
        dic = {"id": doc["customer_id"], "amount": doc["amount"]}
        temp3.append(dic)

    stat = {
        "c_count": c_count,
        "cont": cont[0]["cont"],
        "qty": qty[0]["qty"],
        "amount": amount,
        "trans": temp1,
        "recharge" : temp2,
        "wallet" : temp3
    }

    return stat


if __name__ == "__main__":
    app.debug = True
    app.run()
