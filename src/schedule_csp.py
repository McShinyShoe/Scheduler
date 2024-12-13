import datetime
from time_slot import TimeSlot  
from typing import List, Dict, Callable, Tuple

# Main class for CSP Logic
class ScheduleCSP:
    # Initialize CSP class members
    def __init__(self, time_slots: List[Tuple[str, int]], events: Dict[str, int]):
        self.event_list = events.keys()
        self.time_slots = time_slots
        self.events = events
        self.constraints: List[Callable[[Dict[str, int]], bool]] = []
        self.no_overlap_constraints: List[Callable[[Dict[str, int]], bool]] = []
        self.event_order_constraints: List[Callable[[Dict[str, int]], bool]] = []

    # Method to add constraint
    def add_constraint(self, constraint: Callable[[Dict[str, int]], bool]):
        self.constraints.append(constraint)

    # To make sure no two events overlapped at the same time and day
    def add_no_overlap_constraint(self, event1: str, event2: str):
        def no_overlap(assignment: Dict[str, int]) -> bool:
            if event1 in assignment and event2 in assignment:
                times1 = assignment[event1]
                times2 = assignment[event2]
                if any(t1 == t2 for t1 in times1 for t2 in times2):
                    return False
            return True
        self.no_overlap_constraints.append(no_overlap)
    
    # To make sure no two events overlapped at the same day
    def add_no_overlap_day_constraint(self, event1: str, event2: str):
        def no_overlap(assignment: Dict[str, int]) -> bool:
            if event1 in assignment and event2 in assignment:
                times1 = assignment[event1]
                times2 = assignment[event2]
                date1, _ = times1[0]
                date2, _ = times2[0]
                print("Date: ")
                print(date1)
                return date1 != date2
            return True
        self.no_overlap_constraints.append(no_overlap)
    
    # To make sure no two events overlapped at the same week
    def add_no_overlap_week_constraint(self, event1: str, event2: str):
        def no_overlap(assignment: Dict[str, int]) -> bool:
            if event1 in assignment and event2 in assignment:
                times1 = assignment[event1]
                times2 = assignment[event2]
                
                date1, _ = times1[0]
                date2, _ = times2[0]

                datetime1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
                datetime2 = datetime.datetime.strptime(date2, "%Y-%m-%d")

                return datetime1.isocalendar()[1] != datetime2.isocalendar()[1]
            return True
        self.no_overlap_constraints.append(no_overlap)
    
    # To make sure no two events overlapped at the same month
    def add_no_overlap_month_constraint(self, event1: str, event2: str):
        def no_overlap(assignment: Dict[str, int]) -> bool:
            if event1 in assignment and event2 in assignment:
                times1 = assignment[event1]
                times2 = assignment[event2]
                
                date1, _ = times1[0]
                date2, _ = times2[0]

                datetime1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
                datetime2 = datetime.datetime.strptime(date2, "%Y-%m-%d")

                return datetime1.month != datetime2.month
            return True
        self.no_overlap_constraints.append(no_overlap)
    
    # To make sure no two events overlapped at the same year
    def add_no_overlap_year_constraint(self, event1: str, event2: str):
        def no_overlap(assignment: Dict[str, int]) -> bool:
            if event1 in assignment and event2 in assignment:
                times1 = assignment[event1]
                times2 = assignment[event2]
                
                date1, _ = times1[0]
                date2, _ = times2[0]

                datetime1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
                datetime2 = datetime.datetime.strptime(date2, "%Y-%m-%d")

                return datetime1.year != datetime2.year
            return True
        self.no_overlap_constraints.append(no_overlap)

    # To dictate in which order two event should be initialized
    def add_event_order_constraint(self, event1: str, event2: str, before: bool = True):
        def order_constraint(assignment: Dict[str, int]) -> bool:
            if event1 in assignment and event2 in assignment:
                times1 = assignment[event1]
                times2 = assignment[event2]
                
                date1, _ = times1[0]
                date2, _ = times2[0]
                if date1 == date2:
                    
                    time1 = times1[0][1]
                    time2 = times2[0][1]
                    if before:
                        return time1 < time2
                    else:
                        return time1 > time2
                else:
                    if before:
                        return date1 < date2
                    else:
                        return date1 > date2
            return True  
        self.event_order_constraints.append(order_constraint)

    # Constrain an event to start after the corresponding date
    def add_event_after_constraint(self, event: str, after_date: str):
        def after_constraint(assignment: Dict[str, int]) -> bool:
            if event in assignment:
                times = assignment[event]
                event_date, _ = times[0]
                
                event_datetime = datetime.datetime.strptime(event_date, "%Y-%m-%d")
                
                after_datetime = datetime.datetime.strptime(after_date, "%Y-%m-%d")
                return event_datetime > after_datetime  
            return True
        self.constraints.append(after_constraint)

    # Prohibits an event to start after the corresponding date
    def add_event_before_constraint(self, event: str, before_date: str):
        def before_constraint(assignment: Dict[str, int]) -> bool:
            if event in assignment:
                times = assignment[event]
                event_date, _ = times[0]
                
                event_datetime = datetime.datetime.strptime(event_date, "%Y-%m-%d")
                
                before_datetime = datetime.datetime.strptime(before_date, "%Y-%m-%d")
                return event_datetime < before_datetime
            return True
        self.constraints.append(before_constraint)

    # Check consistency from all of the constraints in the list
    def is_consistent(self, assignment: Dict[str, int]) -> bool:
        return all(constraint(assignment) for constraint in self.constraints) and \
               all(no_overlap(assignment) for no_overlap in self.no_overlap_constraints) and \
               all(order_constraint(assignment) for order_constraint in self.event_order_constraints)

    # Entrypoint for CSP solution finding recursive Metehod
    def find_solutions(self, num_solutions: int) -> List[Dict[str, int]]:
        solutions = []
        self._find_solutions_recursive({}, solutions, num_solutions)
        return solutions

    # CSP solution finding recursive Metehod
    def _find_solutions_recursive(self, assignment: Dict[str, int], solutions: List[Dict[str, int]], num_solutions: int):
        if len(assignment) == len(self.event_list):
            solutions.append(assignment.copy())
            return len(solutions) < num_solutions

        unassigned = [e for e in self.event_list if e not in assignment]
        first = unassigned[0]

        event_duration = self.events[first]

        for date, start_time in self.time_slots:
            if start_time + event_duration <= max(t[1] for t in self.time_slots) and all((date, time) not in assignment.values() for time in range(start_time, start_time + event_duration)):
                
                assignment[first] = [(date, time) for time in range(start_time, start_time + event_duration)]
                
                if self.is_consistent(assignment):
                    
                    if not self._find_solutions_recursive(assignment, solutions, num_solutions):
                        return False
                
                del assignment[first]

        return True

# Entrypoint for testing and debugging in case the given file ran as main
if __name__ == "__main__":
    time_slots = TimeSlot(start_date="2024-11-26", end_date="2024-11-30", start_hour=9, end_hour=18)

    time_slots.exclude_day_of_week(0)
    time_slots.exclude_day_of_week(1)

    events = {
        "Meeting1": 2,  
        "Meeting2": 3,  
        "Lecture": 1,
    }

    csp = ScheduleCSP(time_slots.generate_time_slots(), events)

    csp.add_event_after_constraint("Meeting1", "2024-11-20")
    csp.add_event_before_constraint("Meeting2", "2024-11-29")

    csp.add_event_order_constraint("Meeting1", "Meeting2", before=False)

    solutions = csp.find_solutions(3)

    for i, solution in enumerate(solutions, 1):
        print(f"Solution {i}:")
        for event, time_slots in solution.items():
            print(f"  Event: {event}")
            for time_slot in time_slots:
                date, time = time_slot
                print(f"    Time: {date} @ {time}")
        print()
