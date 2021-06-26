from django.http import JsonResponse

from account.models import User
from blog.models import ArticlePage, Category


def tagify_query(request):
	all_articles = ArticlePage.objects.live().public()
	authors = list([user.first_name + ' ' + user.last_name for user in User.objects.filter(is_staff=True)])
	tags = list(dict.fromkeys(all_articles.values_list('tags__name', flat=True)))
	articles = list(all_articles.values_list('title', flat=True))
	categories = list(Category.objects.all().values_list('name', flat=True))
	return JsonResponse({
		'articles': articles,
		'authors': authors,
		'categories': categories,
		'tags': tags,
	})
