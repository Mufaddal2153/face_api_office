from config import face
from flask import render_template, request
import pymongo, time, datetime, json

try:
    client = pymongo.MongoClient("localhost", 27017)   
    db = client['face_recognition_office']
    collection = db.office_data
    print(collection)
    # print(client.test)
except Exception as e:
    print(e)


@face.route("/")
def index():
    return render_template("index.html")


@face.route("/api/update", methods = ['POST'])
def update():
    data = request.get_json()

    if data:
        status = {}
        print(data)
        if 'check' in data.keys():
            if data['check'] == "checkIn":
                print("Checked in")
                start = datetime.datetime.now()
                start_date = start.strftime("%d/%m/%Y")
                start_time = start.strftime("%H%M%S")
                query = {
                    "employee_id":data['ejamaat'],
                    "start_date":start_date
                }
                print(query)

                try:
                    ret = collection.find_one(query)
                    print("RET ", ret)
                    if not ret:
                        insert_data = {
                            "name": data['name'],
                            "start_date": start_date,
                            "check": "checkIn",
                            "end_time": None,
                            "employee_id": data['ejamaat'],
                            "start_time":start_time
                        }
                        print(insert_data)
                        collection.insert_one(insert_data)
                        print("inserted")
                        status["ok"] = "ok"
                    else:
                        print("You have already checked in")
                        status["exist"] = "checkIn, data exists"
                except Exception as e:
                    print("Insert or Find Error")
                    print(e)
            
            elif data['check'] == "checkOut":
                print("Checked out")
                start = datetime.datetime.now()
                start_date = start.strftime("%d/%m/%Y")
                end_time = start.strftime("%H%M%S")
                query = {
                    "employee_id": data["ejamaat"],
                    "start_date": start_date
                }
                try:
                    ret = collection.find(query)
                    if ret:
                        collection.update_one(
                            {
                                "employee_id": data['employee_id'],
                                "start_date": start_date
                            },
                            {
                                "$set": {
                                    "end_time": end_time
                                }
                            }
                        )
                        print("Checkout DONEE")
                        status["ok"] = "ok"
                    else:
                        print("You have not checked in")
                        status["exist"] = "checkIn, doesn't exist"
                except Exception as e:
                    print(e)
        elif "check" not in data.keys():
            print("No check")
            status["error"] = "No check"
        return json.dumps(status)

    else:
        print("Error")
        return "Error"


if __name__ == "__main__":
    face.run(debug=True)