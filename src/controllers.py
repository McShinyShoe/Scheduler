from flask import render_template, request, jsonify
from time_slot import TimeSlot  
from schedule_csp import ScheduleCSP  
from datetime import datetime
import itertools

def index():
    result = None
    if request.method == "POST":
        try:
            form_data = request.get_json()
            
            start_date = str(form_data.get("startDate"))
            end_date = str(form_data.get("endDate"))
            start_hour = datetime.strptime(str(form_data.get("startTime", 0)), "%H:%M").time().hour
            end_hour = datetime.strptime(str(form_data.get("endTime", 0)), "%H:%M").time().hour

            events = {}
            for event in form_data.get('event', []):
                events[event['name']] = int(event['duration'])

            time_slots = TimeSlot(start_date=start_date, end_date=end_date, start_hour=start_hour, end_hour=end_hour)

            if not bool(form_data.get("weekdays").get("monday")):
                time_slots.exclude_day_of_week(0)
            if not bool(form_data.get("weekdays").get("tuesday")):
                time_slots.exclude_day_of_week(1)
            if not bool(form_data.get("weekdays").get("wednesday")):
                time_slots.exclude_day_of_week(2)
            if not bool(form_data.get("weekdays").get("thursday")):
                time_slots.exclude_day_of_week(3)
            if not bool(form_data.get("weekdays").get("friday")):
                time_slots.exclude_day_of_week(4)
            if not bool(form_data.get("weekdays").get("saturday")):
                time_slots.exclude_day_of_week(5)
            if not bool(form_data.get("weekdays").get("sunday")):
                time_slots.exclude_day_of_week(6)

            csp = ScheduleCSP(time_slots.generate_time_slots(), events)

            for constraint in form_data.get('constraint', []):
                constraintType = constraint['constraintType']
                var1 = constraint['var1']
                var2 = constraint['var2']
                if constraintType == "noOverlap":
                    csp.add_no_overlap_constraint(var1, var2)
                elif constraintType == "noOverlapDay":
                    csp.add_no_overlap_day_constraint(var1, var2)
                elif constraintType == "noOverlapWeek":
                    csp.add_no_overlap_week_constraint(var1, var2)
                elif constraintType == "noOverlapMonth":
                    csp.add_no_overlap_month_constraint(var1, var2)
                elif constraintType == "noOverlapYear":
                    csp.add_no_overlap_year_constraint(var1, var2)
                elif constraintType == "eventOrder":
                    csp.add_event_order_constraint(var1, var2)
                elif constraintType == "eventAfter":
                    csp.add_event_after_constraint(var1, var2)
                elif constraintType == "eventBefore":
                    csp.add_event_before_constraint(var1, var2)

            if bool(form_data.get('globalNoOverlap')):    
                keys = list(events.keys())
                for combination in itertools.combinations(keys, 2):
                    csp.add_no_overlap_constraint(combination[0], combination[1])

            results = csp.find_solutions(3)
            response_data = {
                "start_date": start_date,
                "end_date": end_date,
                "start_hour": start_hour,
                "end_hour": end_hour,
                "events": events,
                "results": results
            }
            return jsonify(response_data)
        except ValueError:
            results = "Invalid input. Please enter numbers only."
    
    return render_template("index.html")
