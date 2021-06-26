"""
from django.utils.translation import gettext_lazy as _
from graphene_django.types import DjangoObjectType
from .models import WinwheelSection, WinwheelParameter
from newsletter.models import Subscriber
import graphene
import random


class WinwheelSectionType(DjangoObjectType):
	class Meta:
		model = WinwheelSection


class WinwheelParameterType(DjangoObjectType):
	class Meta:
		model = WinwheelParameter


class WinwheelSectionWinner(graphene.ObjectType):
	display_text = graphene.String()
	result_title = graphene.String()
	result_text = graphene.String()
	coupon_code = graphene.String()


class SpinWinwheel(graphene.Mutation):
	display_text = graphene.String()
	result_title = graphene.String()
	result_text = graphene.String()
	coupon_code = graphene.String()

	class Arguments:
		email = graphene.String(required=True)

	def mutate(self, info, email):
		if Subscriber.objects.filter(email=email):
				raise Exception(str(_('You already spinned the wheel')))
		else:
			winwheel = WinwheelSection.objects.all()
			pool = {}
			index = 0
			for winwheel_section in winwheel:
				for x in range(winwheel_section.percentage_of_winning):
					pool[index] = winwheel_section
					index += 1
			winner = pool[random.randint(0, 100)]
			Subscriber.objects.create(email=email)
			return WinwheelSectionWinner(
				display_text=winner.txt_display_text,
				result_title=winner.txt_result_title,
				result_text=winner.txt_result_text,
				coupon_code=winner.coupon.code)


class Query(object):
	all_winwheel_sections = graphene.List(WinwheelSectionType)
	all_winwheel_parameters = graphene.List(WinwheelParameterType)

	def resolve_all_winwheel_sections(self, info, **kwargs):
		return WinwheelSection.objects.all()

	def resolve_all_winwheel_parameters(self, info, **kwargs):
		return WinwheelParameter.objects.all()


class Mutation(graphene.ObjectType):
	spin_winwheel = SpinWinwheel.Field()
"""