import strawberry


@strawberry.type
class WorkoutExerciseSet:
    reps: int
    weight: float


@strawberry.input
class WorkoutExerciseSetInput:
    reps: int
    weight: float
