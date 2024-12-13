import datetime
from typing import List, Tuple

# Helper class to generate Time Slots
class TimeSlot:
    # Initialize TimeSlot class memberes
    def __init__(self, start_date: str, end_date: str, start_hour: int, end_hour: int):
        self.start_date = start_date
        self.end_date = end_date
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.excluded_days: List[int] = []  
        self.excluded_time_ranges: List[Tuple[int, int, int]] = []  
    
    # Added an exception for day of the week
    def exclude_day_of_week(self, day_of_week: int):
        if day_of_week not in self.excluded_days:
            self.excluded_days.append(day_of_week)
    
    # Exclude a time range
    def exclude_time_range(self, day_of_week: int, start_hour: int, end_hour: int):
        self.excluded_time_ranges.append((day_of_week, start_hour, end_hour))
    
    # Method to generate the time slot
    def generate_time_slots(self) -> List[Tuple[str, int]]:
        time_slots = []
        current_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(self.end_date, "%Y-%m-%d")
        
        while current_date <= end_date:
            weekday = current_date.weekday()  
            if weekday not in self.excluded_days:  
                for hour in range(self.start_hour, self.end_hour):
                    
                    excluded = False
                    for excluded_day, excluded_start, excluded_end in self.excluded_time_ranges:
                        if weekday == excluded_day and excluded_start <= hour < excluded_end:
                            excluded = True
                            break
                    
                    if not excluded:
                        time_slots.append((current_date.strftime("%Y-%m-%d"), hour))
            current_date += datetime.timedelta(days=1)
        
        return time_slots
