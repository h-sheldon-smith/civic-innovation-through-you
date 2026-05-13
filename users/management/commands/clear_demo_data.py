from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from machina.apps.forum.models import Forum
from machina.core.db.models import get_model
from idea_suggestion.models import Idea

from .create_demo_data import DEMO_USERS, DEMO_POSTS, DEMO_IDEAS


class Command(BaseCommand):
    help = "Remove demo users, forum posts, and idea submissions created by create_demo_data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Skip the confirmation prompt.",
        )

    def handle(self, *args, **options):
        if not options["yes"]:
            confirm = input(
                "This will delete all demo data (users, posts, ideas). Continue? [y/N] "
            )
            if confirm.strip().lower() != "y":
                self.stdout.write("Aborted.")
                return

        Topic = get_model("forum_conversation", "Topic")

        self._clear_ideas()
        self._clear_forum_posts(Topic)
        self._clear_users()

        self.stdout.write("\nDone.")

    def _clear_ideas(self):
        self.stdout.write("\n--- Idea submissions ---")
        for username, subject_line, *_ in DEMO_IDEAS:
            deleted, _ = Idea.objects.filter(
                resident__username=username, subject_line=subject_line
            ).delete()
            if deleted:
                self.stdout.write(self.style.SUCCESS(f'  Deleted  "{subject_line[:60]}"'))
            else:
                self.stdout.write(self.style.WARNING(f'  Missing  "{subject_line[:60]}"'))

    def _clear_forum_posts(self, Topic):
        self.stdout.write("\n--- Forum posts ---")
        for forum_name, subject, *_ in DEMO_POSTS:
            try:
                forum = Forum.objects.get(name=forum_name)
            except Forum.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Skipped  "{subject[:50]}" — forum "{forum_name}" not found'))
                continue

            topic = Topic.objects.filter(forum=forum, subject=subject).first()
            if topic is None:
                self.stdout.write(self.style.WARNING(f'  Missing  "{subject[:60]}"'))
                continue

            # Decrement forum counters before deleting
            Forum.objects.filter(pk=forum.pk).update(
                direct_posts_count=max(0, forum.direct_posts_count - 1),
                direct_topics_count=max(0, forum.direct_topics_count - 1),
            )

            topic.delete()
            self.stdout.write(self.style.SUCCESS(f'  Deleted  "{subject[:60]}"'))

    def _clear_users(self):
        self.stdout.write("\n--- Users ---")
        for data in DEMO_USERS:
            username = data["username"]
            deleted, _ = User.objects.filter(username=username).delete()
            if deleted:
                self.stdout.write(self.style.SUCCESS(f'  Deleted  "{username}"'))
            else:
                self.stdout.write(self.style.WARNING(f'  Missing  "{username}"'))
