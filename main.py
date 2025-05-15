import getpass
import os

from dotenv import load_dotenv

import aiohttp
import logging

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, function_tool, ToolError
from livekit.plugins import (
    noise_cancellation,
    silero
)
from livekit.plugins.openai.stt import STT as OpenAISTT
from livekit.plugins.openai.tts import TTS as OpenAITTS
from livekit.plugins.openai.llm import LLM as OpenAILLM
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from openai import NOT_GIVEN
from pydantic.v1 import BaseSettings
from tavily import TavilyClient

logger = logging.getLogger("assistant-logger")
logger.setLevel(logging.INFO)

load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    weather_api_key: str = ""
    tavily_api_key: str = ""
    stt_api_url: str = ""
    llm_api_url: str = ""
    tts_api_url: str = ""
    tts_api_key: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


async def load_env_variables(settings: Settings) -> None:
    """Load environment variables interactively if not set."""
    if not settings.weather_api_key:
        settings.weather_api_key = getpass.getpass("WEATHER_API_KEY: ")
        os.environ["WEATHER_API_KEY"] = settings.weather_api_key

    if not settings.tavily_api_key:
        settings.tavily_api_key = getpass.getpass("TAVILY_API_KEY: ")
        os.environ["TAVILY_API_KEY"] = settings.tavily_api_key

    if not settings.stt_api_url:
        settings.stt_api_url = getpass.getpass("STT_API_URL: ")
        os.environ["STT_API_URL"] = settings.stt_api_url

    if not settings.llm_api_url:
        settings.llm_api_url = getpass.getpass("LLM_API_URL: ")
        os.environ["LLM_API_URL"] = settings.llm_api_url

    if not settings.tts_api_url:
        settings.tts_api_url = getpass.getpass("TTS_API_URL: ")
        os.environ["TTS_API_URL"] = settings.tts_api_url

    if not settings.tts_api_key:
        settings.tts_api_key = getpass.getpass("TTS_API_KEY: ")
        os.environ["TTS_API_KEY"] = settings.tts_api_key


class Assistant(Agent):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        if not settings.tavily_api_key:
            raise ValueError("Tavily API key is required for web search")
        if not settings.weather_api_key:
            raise ValueError("Weather API key is required for weather search")

        super().__init__(instructions="You are a voice assistant created by Extrawest Company. "
                                      "Your interface with users will be voice. You should use short and concise responses, "
                                      "and avoiding usage of unpronounceable punctuation. "
                                      "You were created as a demo to showcase the capabilities of LiveKit's agents framework.")

    @function_tool()
    async def search_web(self, query: str):
        """
        Performs a web search using the Tavily search engine.

        Args:
            query: The search term or question you want to look up online.
        """

        logger.info(f"WEB Searching for {query}")

        tavily_client = TavilyClient(api_key=self.settings.tavily_api_key)
        search = tavily_client.search(query)

        logger.info(f"WEB Searching result {search}")

        return search

    @function_tool()
    async def get_weather(
            self,
            latitude: str,
            longitude: str,
    ):
        """Called when the user asks about the weather. This function will return the weather for
        the given location. When given a location, please estimate the latitude and longitude of the
        location and do not ask the user for them.

        Args:
            latitude: The latitude of the location
            longitude: The longitude of the location
        """

        logger.info(f"getting weather for {latitude}, {longitude}")
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&lang=en&appid={self.settings.weather_api_key}"
        weather_data = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                logger.info(f"getting weather response: {response}")
                if response.status == 200:
                    weather_data = await response.json()
                else:
                    raise ToolError(f"Failed to get weather data, status code: {response.status}")

        return weather_data


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    settings = Settings()
    await load_env_variables(settings)

    session = AgentSession(
        stt=OpenAISTT(
            base_url=settings.stt_api_url,
            model="Systran/faster-distil-whisper-small.en",
            api_key=NOT_GIVEN,
            language="en"
        ),
        llm=OpenAILLM(
            model="llama3.1:latest",
            base_url=settings.llm_api_url,
            api_key=NOT_GIVEN,
        ),
        tts=OpenAITTS(
            base_url=settings.tts_api_url,
            api_key=settings.tts_api_key,
            model="model_q8f16",
            voice="af_heart",
            response_format="mp3"
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(settings),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))