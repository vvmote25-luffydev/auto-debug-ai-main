import gradio as gr
from agents.tools import autonomous_debug
import json


def run_debug(endpoint, method):
    result = autonomous_debug(endpoint, method)

    logs = "\n".join(result["logs"])

    if result["ai_analysis"]:
        ai_output = json.dumps(result["ai_analysis"], indent=2)
    else:
        ai_output = "No AI analysis needed (API succeeded)."

    return logs, ai_output


with gr.Blocks() as demo:
    gr.Markdown("# 🚀 AutoDebug AI - Autonomous API Debugging Agent")

    with gr.Row():
        endpoint = gr.Textbox(label="API Endpoint", placeholder="https://api.example.com/users")
        method = gr.Dropdown(["GET", "POST"], label="HTTP Method", value="GET")

    debug_button = gr.Button("Debug API")

    logs_output = gr.Textbox(label="Execution Logs", lines=10)
    ai_output = gr.Textbox(label="AI Analysis Output", lines=20)

    debug_button.click(
        run_debug,
        inputs=[endpoint, method],
        outputs=[logs_output, ai_output]
    )

demo.launch()