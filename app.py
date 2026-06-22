import gradio as gr
import os
from retriever import retrieve
from groq import Groq

client = Groq(api_key="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")

def ask_question(question: str):
    if not question or not question.strip():
        return "Please ask a question.", ""
    
    context_chunks = retrieve(question, top_k=5)
    
    context = "\n\n---\n\n".join([
        f"Source: {c['source']}\n{c['text'][:800]}" for c in context_chunks
    ])
    
    system_prompt = "You are a helpful advisor for Truman State University students. Answer ONLY using the provided Truman documents. Cite the source filename. If you don't have enough information, reply: 'I don't have enough information from the available documents.'"
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ],
            temperature=0.3,
            max_tokens=800
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Error: {str(e)}"

    sources = "\n".join(set(c['source'] for c in context_chunks))
    
    return answer, sources

with gr.Blocks(title="Truman IDM RAG") as demo:
    gr.Markdown("# Truman Interdisciplinary Major Maker\nAsk about IDS majors, requirements, and proposals")
    
    with gr.Row():
        inp = gr.Textbox(
            label="Ask a question about Interdisciplinary Majors at Truman",
            placeholder="What are the minimum credit requirements for an IDS major?",
            lines=2
        )
        btn = gr.Button("Ask", variant="primary")
    
    answer_box = gr.Textbox(label="Answer", lines=10)
    sources_box = gr.Textbox(label="Sources Used", lines=4)
    
    btn.click(ask_question, inputs=inp, outputs=[answer_box, sources_box])
    inp.submit(ask_question, inputs=inp, outputs=[answer_box, sources_box])

if __name__ == "__main__":
    print("🚀 Starting Truman IDM RAG...")
    demo.launch()
