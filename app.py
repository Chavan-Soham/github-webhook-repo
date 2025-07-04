# Flask a web framework is helpful in creating a web application and APIs faster.
# to connect to MongoDB, I am using pymongo library.
# for the date and time operations, I am using datetime library.
# for testing outputs on console, I am using json library for pretty print.
# for proper date format as suggested in the assessment task document, I am using dateutil and pytz library

from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from dateutil import parser
import pytz
import json
from bson.json_util import dumps

app = Flask(__name__) # Flask app created

client = MongoClient("mongodb://localhost:27017/") # MongoDB client created
db = client["github-actions"] # Database created
collection = db["workflows"] # Collection created


# to get the day with the suffix
def get_day_with_suffix(day):
    if 11 <= day <= 13:
        return f"{day}th"
    suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return f"{day}{suffix}"



def handle_push(data):
    
    
    # if it is a push event then below code will execute.
    
        # I am tring to fetch the author, to branch and the timestamp of the push event.
        try:
            author = data["pusher"]["name"]
            branch = data["ref"].split("/")[-1]
            timestamp_push = data["commits"][0]["timestamp"]

            # Parse timestamp string
            parsed_time_push = parser.parse(timestamp_push)

            # Converting to UTC
            utc_time_push = parsed_time_push.astimezone(pytz.utc)

            # Creating final formatted string
            day_with_suffix_push = get_day_with_suffix(utc_time_push.day)
            formatted_time_push = f"{day_with_suffix_push} {utc_time_push.strftime('%B %Y - %I:%M %p')} UTC"

           
            
            
            # I am formatting the message to be displayed.
            formatted_message_push = f"{author} pushed to {branch} at {formatted_time_push}"
            print("Formatted message: ", formatted_message_push)
        
            # I am creating a dictionary so that I can store the data in the database later.
            doc_push = {
                "event": "push",
                "author": author,
                "branch": branch,
                "timestamp": datetime.utcnow(),
            }
            
            try: # I am trying to store the data in the mongodb database and inside workflows collection that I already created.
                result_push = collection.insert_one(doc_push)
                print(f"Document inserted with ID: {result_push.inserted_id}")
            except Exception as db_error:
                print("MongoDB Insert Error:", db_error)
            
            # I am printing if this is successfull
            return jsonify({"message": "Push event received and stored", "data": formatted_message_push}), 200
        
        except Exception as e:
            return jsonify({"message": "Error processing push event", "error": str(e)}), 500


def handle_pull_request(data):
    
    # Getting each details like base branch, head branch, author and timestamp
    try:
        to_branch = data['pull_request']['base']['ref']
        from_branch = data['pull_request']['head']['ref']
        author = data["pull_request"]["user"]["login"]
        timestamp_pull = data["pull_request"]["created_at"]
        
        # Parse timestamp string
        parsed_time_pull = parser.parse(timestamp_pull)

        # Converting to UTC
        utc_time_pull = parsed_time_pull.astimezone(pytz.utc)

        # Creating final formatted string
        day_with_suffix = get_day_with_suffix(utc_time_pull.day)
        formatted_time_pull = f"{day_with_suffix} {utc_time_pull.strftime('%B %Y - %I:%M %p')} UTC"
        
        formatted_message_pull = f"{author} has submitted a pull request from {from_branch} to {to_branch} on {formatted_time_pull}"
        print(formatted_message_pull)
        
        doc_pull = {
            "event": "pull_request",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp_pull
        }
        
        try:
            result_pull = collection.insert_one(doc_pull)
            print(f"Document inserted with ID: {result_pull.inserted_id}")
        except Exception as db_error:
            print("MongoDB Insert Error:", db_error)
            
        
        
    except Exception as e:
        return jsonify({"message": "Error processing pull request event", "error": str(e)}), 500
    
    
    return "this is pull request"



def handle_merge(data):
    try:
        # The user who performed the merge
        author = data['sender']['login']

        # The merged pull request details
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']

        # Merge timestamp
        timestamp_merge = data['pull_request']['merged_at']

        if not timestamp_merge:
            return jsonify({"message": "Merge event received but not yet merged"}), 200

        # Parse and format timestamp
        parsed_time_merge = parser.parse(timestamp_merge)
        utc_time_merge = parsed_time_merge.astimezone(pytz.utc)
        day_with_suffix = get_day_with_suffix(utc_time_merge.day)
        formatted_time_merge = f"{day_with_suffix} {utc_time_merge.strftime('%B %Y - %I:%M %p')} UTC"

        # Console log
        formatted_message_merge = f"{author} merged branch {from_branch} to {to_branch} on {formatted_time_merge}"
        print(formatted_message_merge)

        # I am creating a document to store in MongoDB
        doc_merge = {
            "event": "merge",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp_merge
        }

        try:
            result_merge = collection.insert_one(doc_merge)
            print(f"Document inserted with ID: {result_merge.inserted_id}")
        except Exception as db_error:
            print("MongoDB Insert Error:", db_error)

        return jsonify({"message": "Merge event received and stored", "data": formatted_message_merge}), 200

    except Exception as e:
        return jsonify({"message": "Error processing merge event", "error": str(e)}), 500


# I am creating this route as home page with minimal welcoming UI
@app.route("/")
def home():
    return render_template("home.html")




# I am creating a route to get the push events from the GitHub.
@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    #type of event is retrieved using a header that is sent by Github for any type of action
    event = request.headers.get('X-GitHub-Event')
    print(event)
        
    # I will read the JSON payload containing the event data from the request body and convert it into a dictionary.
    data = request.get_json()
    """ print(json.dumps(data, indent=4)) """ # just to see the keys and values so that I can use them
    
    try:
        if event == "push":
            return handle_push(data)
        elif event == "pull_request":
            # GitHub sends "pull_request" for both PR open and merge events and accordingly I am caling the merge function
            if data.get('action') == "closed" and data['pull_request'].get("merged"):
                return handle_merge(data)
            else:
                return handle_pull_request(data)
        else:
            return jsonify({"message": "Event processed"}), 200

    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    






@app.route("/events", methods=['GET'])
def events_to_display():
    
    # I am getting all the events
    all_events = list(collection.find({"event": {"$in": ["push", "pull_request", "merge"]}}))

    for event in all_events:
        ts = event['timestamp']
        if isinstance(ts, str):
            dt = parser.parse(ts)
        else:
            dt = ts

        # Making sure it's timezone-aware in UTC
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        else:
            dt = dt.astimezone(pytz.utc)

        event['timestamp'] = dt

    # All timestamps are UTC-aware, so sorting according to latest time
    sorted_events = sorted(all_events, key=lambda e: e['timestamp'], reverse=True)

    # I will render the html document with the UI
    return render_template("events.html", events=sorted_events)

    

# I am running the app on port 5000 with debugging option set to true.
if __name__ == "__main__":
    app.run(debug=True, port=5000)