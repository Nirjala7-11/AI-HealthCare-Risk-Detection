#Token handling
import os
hf_token = os.getenv("HF_TOKEN")

#Model handling
model = AutoModelForCasualLM.from_pretrained(
  "google/gemma-2b-it",
  token=hf_token
)

#Device handling
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

#Input handling
inputs = tokenizer(input_text, return_tensors="pt")
inputs = {k: v.to(device) for k, v in inputs.item()}

#Gradio UI
with gr.Blocks() as demo:
    
    gr.Markdown("#AI Healthcare Risk Detection System")
    gr.Markdown("### Enter patient vitals to analyze health risk and get AI-powered insights")

    with gr.Row():
        heart_rate = gr.Slider(40, 150, label="Heart Rate (bpm)")
        spo2 = gr.Slider(70, 100, label="SpO2 (%)")
        temperature = gr.Slider(95, 105, label="Temperature (°F)")

    submit_btn = gr.Button("Analyze Patient")
    clear_btn = gr.Button("Clear")
    score_display = gr.Markdown()

    output = gr.Markdown(label="Medical Report")

    submit_btn.click(
        fn=analyze_patient,
        inputs=[heart_rate, spo2, temperature],
        outputs=[score_display, output],
        show_progress=True
    )
    clear_btn.click(
        fn=lambda: ("", "", "", ""),
        inputs=[],
        outputs=[heart_rate, spo2, temperature, output]
    )
    gr.Examples(
        examples=[
            [120,88,102],
            [80,97,98],
            [110,90,101]
        ],
        inputs=[heart_rate, spo2, temperature]
    )
    gr.Markdown("Disclaimer: This AI tool is for educational purposes only and not a substitute for professional medical advice.")

demo.launch()
