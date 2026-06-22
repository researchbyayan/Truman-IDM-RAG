import gradio as gr
from retriever import retrieve
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_question(question: str):
    # Retrieve relevant chunks
    context_chunks = retrieve(question, top_k=5)
    
    context = "\n\n".join([
        f"Source: {c['source']}\n{c['text']}" for c in context_chunks
    ])
    
    # Strong grounding prompt
    system_prompt = """You are a helpful assistant for Truman State University students.
Answer ONLY using the provided context from official Truman documents.
Always cite the source file(s). If the answer is not in the context, say: 
"I don't have enough information from the available documents.""""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        temperature=0.3,
    )
    
    answer = response.choices[0].message.content
    sources = [c['source'] for c in context_chunks]
    
    return answer, "\n".join(set(sources))

# Gradio Interface
with gr.Blocks(title="Truman IDM RAG") as demo:
    gr.Markdown("# Truman Interdisciplinary Major Maker\nAsk questions about IDS majors")
    
    with gr.Row():
        question = gr.Textbox(label="Your Question", placeholder="What are the credit requirements for IDS major?")
        ask_btn = gr.Button("Ask")
    
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=3)
    
    ask_btn.click(ask_question, inputs=question, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
