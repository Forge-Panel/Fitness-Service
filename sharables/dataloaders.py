from strawberry.dataloader import DataLoader
from models import User, Exercise, Workout, WorkoutExercise


user_loader = DataLoader(load_fn=User.read_ids)
exercise_loader = DataLoader(load_fn=Exercise.read_ids)
workout_loader = DataLoader(load_fn=Workout.read_ids)
workout_exercise_loader = DataLoader(load_fn=WorkoutExercise.read_ids)
