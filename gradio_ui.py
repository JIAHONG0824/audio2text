import gradio as gr
import openai

def transcribe(filename, key):
    openai.api_key = key
    audio_file = open(filename.name, "rb")
    transcript_txt = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcript_txt

def openai_api(prompt, key):
    openai.api_key = key
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def transcribe_and_download(file, key):
    if file is not None:
        txt_content = transcribe(file, key)
        txt_path = "transcribe.txt"
        with open(txt_path, "w") as txt_file:
            txt_file.write(txt_content)
        return txt_content, txt_path
    return "", None

def transcribe_and_summary(text, key):
    if text:
        prompt = "請扮演文書處理專家，幫我把「會議逐字稿」作「重點摘錄」，逐字稿如下：" + text
        summary = openai_api(prompt, key)
        txt_path = "summary.txt"
        with open(txt_path, "w") as txt_file:
            txt_file.write(summary)
        return summary, txt_path
    return "", None

with gr.Blocks() as demo:
    gr.Markdown("音頻轉文字，並擷取重點")
    with gr.Tab("請依順序操作"):
        with gr.Row():
            file_input = gr.File(label="第一步：請上傳檔案")
            api_key_input = gr.Textbox(label="第二步：請輸入OpenAI API金鑰", placeholder="OpenAI API Key")
            submit_button = gr.Button("第三步：開始轉譯")
            file_output_txt = gr.File(label="第四步：下載逐字稿(Optional)")
        with gr.Row():
            content = gr.Textbox(label="第五步：檢視轉譯逐字稿", value="轉譯逐字稿")
            submit2_button = gr.Button("第六步：開始重點摘錄")
            summary = gr.Textbox(label="第七步：輸出重點摘錄", value="重點摘錄")
            file_output2_txt = gr.File(label="第八步：下載重點摘錄(Optional)")

    submit_button.click(
        transcribe_and_download,
        inputs=[file_input, api_key_input],
        outputs=[content, file_output_txt]
    )
    submit2_button.click(
        transcribe_and_summary,
        inputs=[content, api_key_input],
        outputs=[summary, file_output2_txt]
    )
