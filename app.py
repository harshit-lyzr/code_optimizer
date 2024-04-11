import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Lyzr Code Optimizer",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Lyzr Code Optimizer🧑🏼‍💻")
st.markdown("### Welcome to the Lyzr Code Optimizer!")
st.markdown("Lyzr Code Optimizer is curated to optimize code and reduce time complexity!!!")

code = st.text_area("Enter your Code: ", height=300,placeholder=f"""print("Hello World!!!")
""")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)


def code_optimization(code):
    optimizer_agent = Agent(
        role="maths expert",
        prompt_persona=f"Your task is to Optimize the given Code and improve the code."
    )

    prompt = f"""find complexity and Optimize a {code} to improve its time complexity and reduce the number of operations performed,
     while ensuring the output remains sorted correctly.
    [!Important] Only give code and what optimized and How?

    Give Output As Below:
    Code
    What is Optimized?
    How it's Optimized?

    """

    optimization_task = Task(
        name="Maths Problem Solver",
        model=open_ai_text_completion_model,
        agent=optimizer_agent,
        instructions=prompt,
    )

    output = LinearSyncPipeline(
        name="Code Optimization Pipline",
        completion_message="Optimization completed",
        tasks=[
            optimization_task
        ],
    ).run()

    answer = output[0]['task_output']

    return answer


if st.button("Optimize"):
    solution = code_optimization(code)
    st.markdown(solution)

with st.expander("ℹ️ - About this App"):
    st.markdown("""
    This app uses Lyzr Automata Agent Optimize your code. For any inquiries or issues, please contact Lyzr.

    """)
    st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width=True)
    st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width=True)
    st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width=True)
    st.link_button("Slack",
                   url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw',
                   use_container_width=True)