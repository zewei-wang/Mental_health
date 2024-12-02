from django_cron import CronJobBase, Schedule
from datetime import date
import random
from .models import DailyChallenge, ChallengeTemplate
from users.models import User
import logging

logger = logging.getLogger(__name__)

class GenerateDailyChallengesCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'gamification.generate_daily_challenges'

    def do(self):
        logger.info("Starting GenerateDailyChallengesCronJob...")
        users = User.objects.all()
        challenge_templates = ChallengeTemplate.objects.all()

        for user in users:
            if DailyChallenge.objects.filter(user=user, date_assigned=date.today()).exists():
                logger.info(f"Challenge already exists for user {user.username}.")
                continue

            if challenge_templates.exists():
                challenge_template = random.choice(challenge_templates)
                DailyChallenge.objects.create(
                    user=user,
                    task=challenge_template.task,
                    date_assigned=date.today()
                )
                logger.info(f"Challenge created for user {user.username} with task: {challenge_template.task}")
