from gcloudc.tests import TestCase
from .models import Site, Page
from django.db.models import Case, When, IntegerField, Q


class AnnotationTests(TestCase):

    def test_when_case_annotation(self):
        FIRST = 0
        SECOND = 1
        THIRD = 2
        FORTH = 3

        def run_query(hostname, port):
            return Site.objects.annotate(
                match=Case(
                    When(hostname=hostname, port=port, then=FIRST),
                    When(
                        hostname=hostname, is_default_site=True, then=SECOND
                    ),
                    When(is_default_site=True, then=THIRD),
                    default=FORTH,
                    output_field=IntegerField(),
                )
            ).filter(Q(hostname=hostname) | Q(is_default_site=True)).order_by("match").select_related("root_page")

        self.assertEqual(Site.objects.count(), 0)

        page = Page.objects.create()

        Site.objects.create(hostname="example.com", port=80, is_default_site=True, root_page=page)
        Site.objects.create(hostname="example.com", port=443, root_page=page)
        Site.objects.create(hostname="example.org", port=80, root_page=page)
        Site.objects.create(hostname="example.org", port=443, root_page=page)

        sites = run_query("example.com", 80)

        self.assertEqual(sites.count(), 2)
        self.assertEqual(sites[0].port, 80)
        self.assertEqual(sites[0].match, FIRST)
        self.assertEqual(sites[1].port, 443)
        self.assertEqual(sites[1].match, FORTH)
