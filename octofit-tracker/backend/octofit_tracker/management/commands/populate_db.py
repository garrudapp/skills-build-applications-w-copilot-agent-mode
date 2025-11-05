from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        # Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Users (super heroes)
        heroes = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': marvel},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': dc},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': dc},
        ]
        user_objs = []
        for h in heroes:
            user = User.objects.create(**h)
            user_objs.append(user)

        # Activities
        Activity.objects.create(user=user_objs[0], type='Running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=user_objs[1], type='Cycling', duration=45, date=timezone.now().date())
        Activity.objects.create(user=user_objs[2], type='Swimming', duration=60, date=timezone.now().date())
        Activity.objects.create(user=user_objs[3], type='Yoga', duration=20, date=timezone.now().date())

        # Workouts
        w1 = Workout.objects.create(name='Hero HIIT', description='High intensity for heroes')
        w2 = Workout.objects.create(name='Power Yoga', description='Yoga for super strength')
        w1.suggested_for.set([user_objs[0], user_objs[1]])
        w2.suggested_for.set([user_objs[2], user_objs[3]])

        # Leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=80)

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
