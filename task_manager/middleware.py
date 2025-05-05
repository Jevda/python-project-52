class ForceDefaultLanguageMiddleware:
    """
    Игнорирует HTTP_ACCEPT_LANGUAGE заголовки из браузера.
    Это принуждает Django всегда использовать LANGUAGE_CODE из settings.py
    в качестве языка по умолчанию.

    ВАЖНО: Должен быть установлен *ДО* LocaleMiddleware
    в настройке MIDDLEWARE.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Полностью удаляем HTTP_ACCEPT_LANGUAGE из запроса
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']

        response = self.get_response(request)
        return response
