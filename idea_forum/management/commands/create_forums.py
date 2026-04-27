from django.core.management.base import BaseCommand
from django.utils.text import slugify
from machina.apps.forum.models import Forum


FORUMS = [
    ("Arts & Culture",                  "Discuss local arts, cultural events, and creative community initiatives."),
    ("Business",                        "Share ideas and discuss topics related to local business and economic development."),
    ("Childcare & Youth Programs",      "Talk about childcare resources, after-school programs, and youth services."),
    ("Construction",                    "Discuss ongoing and planned construction projects in the community."),
    ("Community Events",                "Coordinate and share information about upcoming community events."),
    ("Local Government",                "Engage with local government topics, policies, and civic decisions."),
    ("Health & Community Services",     "Share resources and discuss health services and community support programs."),
    ("Housing & Development",           "Talk about housing availability, affordability, and development projects."),
    ("Parks & Green Spaces",            "Discuss parks, trails, green spaces, and outdoor recreation."),
    ("Urban Planning",                  "Share ideas about city planning, zoning, and the future of the community."),
    ("Public Safety",                   "Discuss public safety concerns, emergency services, and neighborhood watch topics."),
    ("Senior Services",                 "Share resources and discuss programs and services for senior community members."),
    ("Transportation & Infrastructure", "Talk about roads, transit, biking, and infrastructure improvements."),
    ("Volunteering Opportunities",      "Find and share local volunteering opportunities and community service projects."),
]


class Command(BaseCommand):
    help = "Create the default set of community forums"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Skip forums whose name already exists instead of reporting them.",
        )

    def handle(self, *args, **options):
        skip_existing = options["skip_existing"]
        created_count = 0
        skipped_count = 0

        for name, description in FORUMS:
            slug = slugify(name)

            if Forum.objects.filter(name=name).exists():
                if not skip_existing:
                    self.stdout.write(self.style.WARNING(f'  Skipped  "{name}" (already exists)'))
                skipped_count += 1
                continue

            # Machina slugs must be unique; append a suffix if a slug collision occurs
            # without a name collision (e.g. "Arts & Culture" vs "Arts and Culture").
            unique_slug = slug
            suffix = 1
            while Forum.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}-{suffix}"
                suffix += 1

            Forum.objects.create(
                name=name,
                slug=unique_slug,
                description=description,
                type=Forum.FORUM_POST,
            )
            self.stdout.write(self.style.SUCCESS(f'  Created  "{name}"'))
            created_count += 1

        self.stdout.write(
            f"\nDone. {created_count} forum(s) created, {skipped_count} skipped."
        )
