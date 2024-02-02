class Adapter:
    def __init__(self):
        pass

    def createFAQ(self, text):
        self.preprocessInput()
        self.callAPI()
        self.preparePrompt()
        self.postprocessOutput()

    def preprocessInput(self):
        pass

    def preparePrompt(self):
        pass

    def callAPI(self):
        pass

    def postprocessOutput(self):
        pass


class Jurassic2Chat:
    """
    https://docs.ai21.com/reference/j2-chat-api
    """
    def __init__(self):
        pass


class Jurassic2Complete:
    """
    https://docs.ai21.com/reference/j2-complete-api-ref
    """
    def __init__(self):
        pass


class CohereCommand:
    """
    https://docs.cohere.com/reference/generate
    """
    def __init__(self):
        pass


class GeminiPro:
    """
    https://cloud.google.com/vertex-ai/docs/generative-ai/pricing?hl=de
    """
    def __init__(self):
        pass


class Palm2:
    """
    https://cloud.google.com/vertex-ai/docs/generative-ai/pricing?hl=de
    """
    def __init__(self):
        pass


class GPT_Neo:
    """
    https://goose.ai/docs/api
    """
    def __init__(self):
        pass


class GPT_J:
    """
    https://goose.ai/docs/api
    """
    def __init__(self):
        pass


class Fairseq:
    """
    https://goose.ai/docs/api
    """
    def __init__(self):
        pass


class GPT_NeoX:
    """
    https://goose.ai/docs/api
    """
    def __init__(self):
        pass


class Llama2:
    """
    https://cloud.google.com/model-garden?hl=de
    """
    def __init__(self):
        pass


class Tii_Falcon:
    """
    https://cloud.google.com/model-garden?hl=de
    """
    def __init__(self):
        pass


class GPT35_Turbo:
    """
    https://platform.openai.com/docs/introduction
    """
    def __init__(self):
        pass


class GPT4:
    """
    https://platform.openai.com/docs/introduction
    """
    def __init__(self):
        pass


class GPT4_Turbo:
    """
    https://platform.openai.com/docs/introduction
    """
    def __init__(self):
        pass
