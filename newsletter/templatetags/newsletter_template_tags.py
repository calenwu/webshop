from django import template
from newsletter.models import NewsletterCampaign


register = template.Library()


@register.simple_tag()
def get_campaign_active() -> bool:
	return len(NewsletterCampaign.objects.filter(active=True)) > 0
