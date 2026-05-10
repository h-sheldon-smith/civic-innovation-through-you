from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from machina.apps.forum.models import Forum
from machina.core.db.models import get_model
from idea_suggestion.models import Idea
from common.choices import Topic_Options


DEMO_USERS = [
    {
        "username": "maria_reyes",
        "email": "maria.reyes@example.com",
        "first_name": "Maria",
        "last_name": "Reyes",
        "password": "demopass123",
    },
    {
        "username": "james_okafor",
        "email": "james.okafor@example.com",
        "first_name": "James",
        "last_name": "Okafor",
        "password": "demopass123",
    },
    {
        "username": "priya_singh",
        "email": "priya.singh@example.com",
        "first_name": "Priya",
        "last_name": "Singh",
        "password": "demopass123",
    },
    {
        "username": "derek_thornton",
        "email": "derek.thornton@example.com",
        "first_name": "Derek",
        "last_name": "Thornton",
        "password": "demopass123",
    },
]

# (forum_name, subject, body)
DEMO_POSTS = [
    (
        "Parks & Green Spaces",
        "Can we get more benches along Riverside Trail?",
        "I walk the Riverside Trail every morning and the stretch between Oak Ave and "
        "Main St has no seating whatsoever. Older residents and families with young kids "
        "really struggle on warm days. Would love to see 4-5 benches added along that half-mile. "
        "Anyone else feel the same? Would be happy to help organize a petition.",
        "maria_reyes",
    ),
    (
        "Parks & Green Spaces",
        "Dog-friendly zones in Centennial Park – thoughts?",
        "A lot of us bring dogs to Centennial Park, but there's no clearly marked off-leash area. "
        "Dogs end up in the picnic areas which upsets families. Could we designate the northwest "
        "corner as a dog-friendly zone with signage? Happy to coordinate with Parks & Rec.",
        "james_okafor",
    ),
    (
        "Transportation & Infrastructure",
        "Dangerous intersection at 4th & Maple – needs a light",
        "The intersection at 4th St and Maple Ave has had three near-misses in the past month that "
        "I've personally witnessed. There's no traffic signal and visibility is blocked by the new "
        "apartment building. I've filed a report with the city but wanted to rally community support "
        "here. Please share your experiences if you've had issues there too.",
        "derek_thornton",
    ),
    (
        "Transportation & Infrastructure",
        "Bike lane proposal for downtown corridor",
        "With more people commuting by bike post-pandemic, I think it's time to push for a protected "
        "bike lane on Commerce St from University Ave down to the waterfront. Other cities our size "
        "have seen significant safety improvements with similar infrastructure. Linking the city's "
        "own traffic study below. Who would use this route?",
        "priya_singh",
    ),
    (
        "Community Events",
        "Summer block party – looking for co-organizers!",
        "I'd like to organize a block party for the Elm Street neighborhood this July. Last year's "
        "event on Oak had great turnout and I want to bring the same energy to our block. Looking "
        "for a few people to help with logistics, food coordination, and permits. Reply here or "
        "message me directly if you're interested!",
        "maria_reyes",
    ),
    (
        "Housing & Development",
        "Concerned about the proposed zoning change on Lakeview Dr",
        "The planning commission is reviewing a request to rezone the vacant lot at 820 Lakeview Dr "
        "from R-1 to R-3 (multi-family). I understand the need for more housing, but the road "
        "infrastructure there can't handle the projected increase in traffic. Has anyone else "
        "reviewed the traffic impact report? The public comment period closes in two weeks.",
        "derek_thornton",
    ),
    (
        "Local Government",
        "How do I find the agenda for next week's city council meeting?",
        "New to being civically engaged and I want to attend the council meeting next Tuesday to "
        "speak during public comment. Where do I find the agenda and how early do I need to sign up "
        "to speak? Any tips from folks who've done this before would be really appreciated.",
        "james_okafor",
    ),
    (
        "Health & Community Services",
        "Free mental health resources available downtown – sharing info",
        "Wanted to share that the Community Wellness Center on 2nd Ave now offers free walk-in "
        "counseling on Wednesdays from 10am–2pm. No insurance required. I know a lot of us have "
        "been struggling and this resource doesn't get nearly enough visibility. Pass it along!",
        "priya_singh",
    ),
]

# (username, subject_line, location, topic, message)
DEMO_IDEAS = [
    (
        "maria_reyes",
        "Solar-powered lighting for Riverside Trail",
        "Riverside Trail, Downtown",
        Topic_Options.PARKS,
        "The Riverside Trail is beautiful but completely dark after sunset, making it unsafe for "
        "evening walkers and cyclists. I'd like to propose installing solar-powered LED lights "
        "along the 2-mile stretch. Similar installations in neighboring cities cost roughly $80k "
        "and pay for themselves in 4 years through energy savings. This would also support "
        "evening community events and improve accessibility for residents who can only use the "
        "trail after work.",
    ),
    (
        "james_okafor",
        "Youth coding bootcamp at the public library",
        "Central Public Library, 100 Main St",
        Topic_Options.CHILD,
        "I work in software and I'm willing to volunteer my time to run a free 6-week coding "
        "bootcamp for teens (ages 13-18) at the public library. We'd cover web basics, Python "
        "fundamentals, and a final project. All I'd need from the city is a reserved computer lab "
        "on Saturday mornings and some light promotion through the library's newsletter. I can "
        "bring two other volunteer instructors. This addresses the digital skills gap and gives "
        "kids a real head start.",
    ),
    (
        "priya_singh",
        "Dedicated senior shuttle service between residential areas and grocery stores",
        "Citywide",
        Topic_Options.SENIOR,
        "Many seniors in our community don't drive and the current bus routes don't serve the main "
        "grocery store clusters reliably. I propose a twice-weekly shuttle service specifically for "
        "seniors, running a fixed route between the three largest senior residential areas and the "
        "two main grocery store clusters. Could be operated through a contract with an existing "
        "transport provider or through volunteers. Reduces isolation, improves nutrition, and keeps "
        "seniors independent longer.",
    ),
    (
        "derek_thornton",
        "Pothole tracking app integration with city 311 system",
        "Citywide",
        Topic_Options.TRANSPORT,
        "Residents currently have no easy way to report potholes that feeds directly into the DPW "
        "work queue. I'd like to propose integrating a simple photo-based pothole reporting feature "
        "into the existing 311 app, with automatic GPS tagging and status updates when the issue "
        "is resolved. This reduces redundant reports, helps the city prioritize repairs by density "
        "of complaints, and builds public trust through transparency. Several open-source solutions "
        "exist that could be adapted at low cost.",
    ),
    (
        "maria_reyes",
        "Community mural program for downtown underpasses",
        "Downtown underpasses, Commerce St corridor",
        Topic_Options.ART,
        "The concrete underpasses along Commerce St are a blight — covered in graffiti and "
        "intimidating at night. I propose a juried mural program inviting local artists to submit "
        "designs that celebrate our city's history and diversity. The city provides surface prep "
        "and anti-graffiti coating; artists receive a small honorarium. Three pilot underpasses "
        "would be transformed in year one. This approach has worked remarkably well in cities like "
        "Philadelphia and Detroit and turns a liability into a civic asset.",
    ),
    (
        "priya_singh",
        "Expand free Wi-Fi hotspots to all public parks",
        "All city parks",
        Topic_Options.PLAN,
        "Only 2 of our 11 city parks currently offer free Wi-Fi. Expanding coverage to all parks "
        "would benefit students doing homework, remote workers who want to work outdoors, and "
        "residents without reliable home internet. Modern mesh networking equipment means this "
        "could be deployed cost-effectively by piggybacking on existing fiber runs to park "
        "facilities. I'd estimate $15k per park for hardware and installation. The equity "
        "implications alone make this worth prioritizing.",
    ),
]


class Command(BaseCommand):
    help = "Create demo user accounts, forum posts, and idea submissions for testing and demonstration"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Skip records that already exist instead of reporting them.",
        )

    def handle(self, *args, **options):
        skip_existing = options["skip_existing"]

        Topic = get_model("forum_conversation", "Topic")
        Post = get_model("forum_conversation", "Post")

        users = self._create_users(skip_existing)
        self._create_forum_posts(users, Topic, Post, skip_existing)
        self._create_ideas(users, skip_existing)

    # ------------------------------------------------------------------ #
    # Users                                                                #
    # ------------------------------------------------------------------ #

    def _create_users(self, skip_existing):
        self.stdout.write("\n--- Users ---")
        users = {}
        for data in DEMO_USERS:
            username = data["username"]
            if User.objects.filter(username=username).exists():
                if not skip_existing:
                    self.stdout.write(self.style.WARNING(f'  Skipped  "{username}" (already exists)'))
                users[username] = User.objects.get(username=username)
                continue

            user = User.objects.create_user(
                username=username,
                email=data["email"],
                password=data["password"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            users[username] = user
            self.stdout.write(self.style.SUCCESS(f'  Created  "{username}"'))

        return users

    # ------------------------------------------------------------------ #
    # Forum posts                                                          #
    # ------------------------------------------------------------------ #

    def _create_forum_posts(self, users, Topic, Post, skip_existing):
        self.stdout.write("\n--- Forum posts ---")
        for forum_name, subject, body, username in DEMO_POSTS:
            try:
                forum = Forum.objects.get(name=forum_name)
            except Forum.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f'  Skipped  "{subject[:50]}" — forum "{forum_name}" not found '
                        f'(run create_forums first)'
                    )
                )
                continue

            poster = users.get(username)
            if poster is None:
                self.stdout.write(self.style.WARNING(f'  Skipped  "{subject[:50]}" — user "{username}" unavailable'))
                continue

            if Topic.objects.filter(forum=forum, subject=subject).exists():
                if not skip_existing:
                    self.stdout.write(self.style.WARNING(f'  Skipped  "{subject[:50]}" (already exists)'))
                continue

            slug = slugify(subject)
            unique_slug = slug
            suffix = 1
            while Topic.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}-{suffix}"
                suffix += 1

            topic = Topic.objects.create(
                forum=forum,
                poster=poster,
                subject=subject,
                slug=unique_slug,
                type=Topic.TOPIC_POST,
                status=Topic.TOPIC_UNLOCKED,
                approved=True,
            )

            post = Post.objects.create(
                topic=topic,
                poster=poster,
                subject=subject,
                content=body,
                approved=True,
            )

            # Wire up the first/last post references Machina expects
            topic.first_post = post
            topic.last_post = post
            topic.posts_count = 1
            topic.save(update_fields=["first_post", "last_post", "posts_count"])

            Forum.objects.filter(pk=forum.pk).update(
                direct_posts_count=Forum.objects.get(pk=forum.pk).direct_posts_count + 1,
                direct_topics_count=Forum.objects.get(pk=forum.pk).direct_topics_count + 1,
                last_post=post,
            )

            self.stdout.write(self.style.SUCCESS(f'  Created  "{subject[:60]}"'))

    # ------------------------------------------------------------------ #
    # Ideas                                                                #
    # ------------------------------------------------------------------ #

    def _create_ideas(self, users, skip_existing):
        self.stdout.write("\n--- Idea submissions ---")
        for username, subject_line, location, topic, message in DEMO_IDEAS:
            poster = users.get(username)
            if poster is None:
                self.stdout.write(self.style.WARNING(f'  Skipped  "{subject_line[:50]}" — user "{username}" unavailable'))
                continue

            if Idea.objects.filter(resident=poster, subject_line=subject_line).exists():
                if not skip_existing:
                    self.stdout.write(self.style.WARNING(f'  Skipped  "{subject_line[:50]}" (already exists)'))
                continue

            Idea.objects.create(
                resident=poster,
                subject_line=subject_line,
                location=location,
                topic=topic,
                message=message,
            )
            self.stdout.write(self.style.SUCCESS(f'  Created  "{subject_line[:60]}"'))

        self.stdout.write("\nDone.")
