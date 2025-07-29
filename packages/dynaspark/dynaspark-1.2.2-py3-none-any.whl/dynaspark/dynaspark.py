import requests
from urllib.parse import quote, urlencode
from io import BytesIO

class DynaSpark:
    """A client for interacting with the DynaSpark API."""
    
    def __init__(self, api_key="TH3_API_KEY"):
        """Initialize the DynaSpark client.
        
        Args:
            api_key (str, optional): API key for authentication. Defaults to free API key.
        """
        self.api_key = api_key
        self.base_url = "https://dynaspark.onrender.com"
        self.headers = {
            "User-Agent": "DynaSpark-Python-Client",
            "Accept": "application/json"
        }

    def generate_response(self, user_input, **kwargs):
        """Generate a text response using DynaSpark's text generation API.
        
        Args:
            user_input (str): The input text to generate a response for.
            **kwargs: Optional parameters for text generation or text-to-speech.
                - model (str): Model to use for generation
                - seed (int): Random seed for reproducibility
                - temperature (float): Controls randomness (0.0 to 3.0)
                - top_p (float): Controls diversity (0.0 to 1.0)
                - presence_penalty (float): Penalizes repeated tokens (-2.0 to 2.0)
                - frequency_penalty (float): Penalizes frequent tokens (-2.0 to 2.0)
                - json (bool): Whether to return JSON response
                - system (str): Custom system prompt
                - stream (bool): Whether to stream the response
                - private (bool): Whether to keep the generation private
                - referrer (str): Referrer information
                - voice (str): Voice for text-to-speech (alloy, echo, fable, onyx, nova, shimmer)
        
        Returns:
            dict: A dictionary containing the text_url for generation.
        
        Raises:
            DynaSparkError: If the API request fails.
        """
        # Construct the URL with the user input and optional parameters
        params = {"api_key": self.api_key, "user_input": user_input}
        params.update(kwargs)
        
        response = requests.get(f"{self.base_url}/api/generate_response", params=params, headers=self.headers)
        
        if response.status_code != 200:
            raise DynaSparkError(f"API request failed: {response.text}")
        
        return response.json()

    def generate_image(self, prompt, width=768, height=768, model=None, 
                      nologo=None, seed=None, wm=None):
        """
        Generate an image using DynaSpark's image generation API.
        
        Args:
            prompt (str): The prompt to generate an image for
            width (int, optional): Image width (64-2048, default: 768)
            height (int, optional): Image height (64-2048, default: 768)
            model (str, optional): Model to use (flux, turbo, gptimage)
            nologo (bool, optional): Whether to exclude the watermark
            seed (int, optional): Random seed for reproducibility
            wm (str, optional): Custom watermark text
            
        Returns:
            str: URL to the generated image
        """
        endpoint = f"{self.base_url}/api/generate_image"
        params = {
            'user_input': prompt,
            'api_key': self.api_key
        }
        
        # Add optional parameters if provided
        optional_params = {
            'width': width,
            'height': height,
            'model': model,
            'nologo': nologo,
            'seed': seed,
            'wm': wm
        }
        
        # Add non-None optional parameters
        params.update({k: v for k, v in optional_params.items() if v is not None})
        
        response = requests.get(endpoint, params=params)
        
        if response.status_code == 200:
            return response.json().get('image_url')
        else:
            response.raise_for_status()

    def get_text(self, prompt, model=None, seed=None, temperature=None, 
                top_p=None, presence_penalty=None, frequency_penalty=None,
                json=False, system=None, stream=False, private=None, referrer=None,
                voice=None):
        """
        Directly get text generation from the text endpoint.
        
        Args:
            prompt (str): The prompt to generate text for
            model (str, optional): The model to use for generation
            seed (int, optional): Random seed for reproducibility
            temperature (float, optional): Controls randomness (0.0 to 3.0)
            top_p (float, optional): Controls diversity via nucleus sampling (0.0 to 1.0)
            presence_penalty (float, optional): Penalizes repeated tokens (-2.0 to 2.0)
            frequency_penalty (float, optional): Penalizes frequent tokens (-2.0 to 2.0)
            json (bool, optional): Whether to return JSON response
            system (str, optional): Custom system prompt
            stream (bool, optional): Whether to stream the response
            private (bool, optional): Whether to keep the generation private
            referrer (str, optional): Referrer information
            voice (str, optional): Voice to use for text-to-speech (alloy, echo, fable, onyx, nova, shimmer)
            
        Returns:
            str or bytes: The generated text response or audio data if using text-to-speech
        """
        # Construct the URL
        text_url = f"https://dynaspark.onrender.com/text/{quote(prompt)}"
        
        # Add optional parameters
        params = {
            'model': model,
            'seed': seed,
            'temperature': temperature,
            'top_p': top_p,
            'presence_penalty': presence_penalty,
            'frequency_penalty': frequency_penalty,
            'json': json,
            'system': system,
            'stream': stream,
            'private': private,
            'referrer': referrer,
            'voice': voice
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        if params:
            text_url += f"?{urlencode(params)}"
            
        response = requests.get(text_url)
        
        if response.status_code == 200:
            if model == 'openai-audio':
                return response.content  # Return audio data as bytes
            elif json:
                return response.json()
            return response.text
        else:
            response.raise_for_status()

    def text_to_speech(self, text, voice='alloy'):
        """
        Convert text to speech using DynaSpark's text-to-speech API.
        
        Args:
            text (str): The text to convert to speech
            voice (str, optional): Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            
        Returns:
            bytes: The generated audio data in MP3 format
        """
        valid_voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        if voice not in valid_voices:
            raise ValueError(f"Invalid voice. Must be one of: {', '.join(valid_voices)}")
            
        return self.get_text(text, model='openai-audio', voice=voice)

    def save_audio(self, audio_data, filename):
        """
        Save audio data to a file.
        
        Args:
            audio_data (bytes): The audio data to save
            filename (str): The name of the file to save to
            
        Returns:
            str: The path to the saved file
        """
        if not filename.endswith('.mp3'):
            filename += '.mp3'
            
        with open(filename, 'wb') as f:
            f.write(audio_data)
        return filename