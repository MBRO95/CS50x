import datetime

def get_suggested_activities(window_name):
    activities = {
        "Wake Window": ["Practice gratitude journaling.", "Prepare a glass of water.", "Stretch gently."],
        "Intimacy Window": ["Engage in self-care or intimacy.", "Focus on connection.", "Plan bonding activities."],
        "Early Morning Light Exposure": ["Go for a short walk outside.", "Sit by a sunny window.", "Drink a glass of water."],
        "Breakfast": ["Eat a protein-rich meal.", "Avoid sugary drinks.", "Enjoy a calm, distraction-free meal."],
        "Morning Productivity": ["Work on deep-focus tasks.", "Write a to-do list.", "Brainstorm creative ideas."],
        "Lunch": ["Eat a balanced meal.", "Go for a short walk after eating.", "Avoid heavy or greasy foods."],
        "Afternoon Productivity": ["Plan meetings or collaborative work.", "Take short breaks.", "Organize your workspace."],
        "Non-Sleep Deep Rest": ["Meditate or practice mindfulness.", "Take a short nap.", "Do a breathing exercise."],
        "Workout": ["Strength training or cardio.", "Stretch to cool down.", "Track your progress."],
        "Dinner": ["Eat a light, nutritious meal.", "Enjoy a family or social meal.", "Avoid caffeine or alcohol."],
        "Evening Wind-Down": ["Dim lights and relax.", "Read a book or journal.", "Avoid screens before bed."],
        "Sleep": ["Maintain a cool, dark bedroom.", "Avoid late-night snacks.", "Practice deep breathing."]
    }
    return activities.get(window_name, ["No specific activities available."])

def round_to_nearest_15(minutes):
    """Round a timedelta object to the nearest 15 minutes."""
    rounded_minutes = round(minutes / 15) * 15
    return datetime.timedelta(minutes=rounded_minutes)

def generate_optimized_schedule(data):
    wake_time = datetime.datetime.strptime(data['wake_time'], '%H:%M')
    bedtime = datetime.datetime.strptime(data['bedtime'], '%H:%M')
    sleep_duration = int(data.get('sleep_duration', 8))  # Default to 8 hours
    include_intimacy = data.get('include_intimacy', False)

    # Adjust bedtime if it's on the next day
    if bedtime <= wake_time:
        bedtime += datetime.timedelta(days=1)

    # Sequential schedule generation
    schedule = []

    # Wake Window: ±15 minutes from wake time
    wake_start = wake_time - datetime.timedelta(minutes=15)
    wake_end = wake_time + datetime.timedelta(minutes=15)
    schedule.append({
        "window": "Wake Window",
        "start": wake_start.strftime('%H:%M'),
        "end": wake_end.strftime('%H:%M'),
        "activity": "Gradually wake up and prepare for the day ahead."
    })

    # Intimacy Window: Optional, directly after Wake Window
    if include_intimacy:
        intimacy_start = wake_end
        intimacy_end = intimacy_start + datetime.timedelta(minutes=30)
        schedule.append({
            "window": "Intimacy Window",
            "start": intimacy_start.strftime('%H:%M'),
            "end": intimacy_end.strftime('%H:%M'),
            "activity": "Ideal time for intimacy or self-pleasure based on hormonal peaks."
        })
        light_start = intimacy_end
    else:
        light_start = wake_end

    # Early Morning Light Exposure
    light_end = light_start + datetime.timedelta(minutes=30)
    schedule.append({
        "window": "Early Morning Light Exposure",
        "start": light_start.strftime('%H:%M'),
        "end": light_end.strftime('%H:%M'),
        "activity": "Expose yourself to bright, natural light and rehydrate."
    })

    # Breakfast
    breakfast_start = light_end
    breakfast_end = breakfast_start + datetime.timedelta(minutes=30)
    schedule.append({
        "window": "Breakfast",
        "start": breakfast_start.strftime('%H:%M'),
        "end": breakfast_end.strftime('%H:%M'),
        "activity": "Start your day with a light, balanced breakfast to boost energy."
    })

    # Morning Productivity
    morning_productivity_start = breakfast_end
    morning_productivity_end = morning_productivity_start + datetime.timedelta(hours=2)
    schedule.append({
        "window": "Morning Productivity",
        "start": morning_productivity_start.strftime('%H:%M'),
        "end": morning_productivity_end.strftime('%H:%M'),
        "activity": "Focus on deep work or creative tasks."
    })

    # Lunch
    lunch_start = morning_productivity_end
    lunch_end = lunch_start + datetime.timedelta(hours=1)
    schedule.append({
        "window": "Lunch",
        "start": lunch_start.strftime('%H:%M'),
        "end": lunch_end.strftime('%H:%M'),
        "activity": "Enjoy a balanced lunch to sustain your energy levels."
    })

    # Afternoon Productivity
    afternoon_productivity_start = lunch_end
    afternoon_productivity_end = afternoon_productivity_start + datetime.timedelta(hours=2)
    schedule.append({
        "window": "Afternoon Productivity",
        "start": afternoon_productivity_start.strftime('%H:%M'),
        "end": afternoon_productivity_end.strftime('%H:%M'),
        "activity": "Engage in strategic tasks or problem-solving."
    })

    # Non-Sleep Deep Rest
    deep_rest_start = afternoon_productivity_end
    deep_rest_base_duration = datetime.timedelta(minutes=20)

    # Calculate total available time
    total_available_time = bedtime - deep_rest_start
    minimum_required_time = (
        deep_rest_base_duration +
        datetime.timedelta(hours=1) +  # Workout
        datetime.timedelta(hours=1) +  # Dinner
        datetime.timedelta(hours=1)    # Evening Wind-Down
    )
    excess_time = max(datetime.timedelta(0), total_available_time - minimum_required_time)
    allocated_nsdr_time = min(deep_rest_base_duration + excess_time, datetime.timedelta(minutes=90))

    deep_rest_end = deep_rest_start + allocated_nsdr_time
    schedule.append({
        "window": "Non-Sleep Deep Rest",
        "start": deep_rest_start.strftime('%H:%M'),
        "end": deep_rest_end.strftime('%H:%M'),
        "activity": "Take a short break, meditate, or nap for up to 90 minutes."
    })

    # Workout Window
    workout_start = deep_rest_end
    workout_end = workout_start + datetime.timedelta(hours=1)
    if workout_end > wake_time + datetime.timedelta(hours=10):
        # Adjust to fit within healthy range relative to wake time
        adjustment = workout_end - (wake_time + datetime.timedelta(hours=10))
        workout_start -= adjustment
        workout_end = workout_start + datetime.timedelta(hours=1)
    schedule.append({
        "window": "Workout",
        "start": workout_start.strftime('%H:%M'),
        "end": workout_end.strftime('%H:%M'),
        "activity": "Perform strength training or cardio to improve health and mood."
    })

    # Dinner
    dinner_start = workout_end
    dinner_end = dinner_start + datetime.timedelta(hours=1)
    if dinner_end > bedtime - datetime.timedelta(hours=2):
        # Ensure Dinner ends at least 2 hours before bedtime
        adjustment = dinner_end - (bedtime - datetime.timedelta(hours=2))
        dinner_start -= adjustment
        dinner_end = dinner_start + datetime.timedelta(hours=1)
    schedule.append({
        "window": "Dinner",
        "start": dinner_start.strftime('%H:%M'),
        "end": dinner_end.strftime('%H:%M'),
        "activity": "Finish your day with a light, nutrient-rich dinner."
    })

    # Evening Wind-Down
    wind_down_start = dinner_end
    wind_down_end = bedtime
    schedule.append({
        "window": "Evening Wind-Down",
        "start": wind_down_start.strftime('%H:%M'),
        "end": wind_down_end.strftime('%H:%M'),
        "activity": "Dim lights, relax, and prepare for bed."
    })

    # Sleep
    schedule.append({
        "window": "Sleep",
        "start": bedtime.strftime('%H:%M'),
        "end": (bedtime + datetime.timedelta(hours=sleep_duration)).strftime('%H:%M'),
        "activity": f"Time to rest. Aim for {sleep_duration} hours of sleep for recovery and well-being."
    })

    # Add durations and suggested activities
    for window in schedule:
        # Calculate duration
        start = datetime.datetime.strptime(window['start'], '%H:%M')
        end = datetime.datetime.strptime(window['end'], '%H:%M')
        duration = end - start
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60
        window['duration'] = f"{hours}h {minutes}m" if hours else f"{minutes}m"

        # Format times to AM/PM
        window['start'] = start.strftime('%I:%M %p')
        window['end'] = end.strftime('%I:%M %p')

        # Add research-backed activities
        window['suggested_activities'] = get_suggested_activities(window['window'])

    return schedule
