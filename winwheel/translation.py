from modeltranslation.translator import translator, TranslationOptions
from .models import WinwheelSection


class WinwheelSectionOptions(TranslationOptions):
	fields = ('txt_result_title', 'txt_result_text',)


translator.register(WinwheelSection, WinwheelSectionOptions)
