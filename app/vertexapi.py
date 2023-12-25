from vertexai.language_models import ChatModel, InputOutputTextPair
from google.cloud import aiplatform
from typing import Optional
import vertexai
import google.auth


class VertexAPI(object):
    ''' Vertex AI API '''
    def __init__(self, 
                location: Optional[str] = None,
                experiment: Optional[str] = None,
                staging_bucket: Optional[str] = None,
                encryption_spec_key_name: Optional[str] = None,
                service_account: Optional[str] = None,
                ):
        
        self.credentials, self.project = self.authenticate()

        aiplatform.init(
            project=self.project,
            location=location,
            experiment=experiment,
            staging_bucket=staging_bucket,
            credentials=self.credentials,
            encryption_spec_key_name=encryption_spec_key_name,
            service_account=service_account,
        )
        vertexai.init(project=self.project, location=location)

    def authenticate(self):
        return google.auth.default()  

    def start_chat_session(self, context_prompt, temperature: float=0.6, max_output_tokens: int = 500, top_p: float = 0.8, top_k: int = 40) -> str:
        chat_model = ChatModel.from_pretrained("chat-bison@001")
        parameters = {
            "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
            "max_output_tokens": max_output_tokens,  # Token limit determines the maximum amount of text output.
            "top_p": top_p,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
            "top_k": top_k,  # A top_k of 1 means the selected token is the most probable among all tokens.
        }

        self.chat_session = chat_model.start_chat(
            context=context_prompt,
            # ,examples=[
            #     InputOutputTextPair(
            #         input_text="How many moons does Mars have?",
            #         output_text="The planet Mars has two moons, Phobos and Deimos.",
            #     ),
            # ],
            **parameters
        )

    def get_completion(self, user_question) -> str:
        response = self.chat_session.send_message(user_question)
        print(f"Response from Model: {response.text}")
        return response.text
