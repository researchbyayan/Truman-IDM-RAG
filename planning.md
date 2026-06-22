## Domain
Interdisciplinary Major Maker at Truman State University. This system helps students create custom Interdisciplinary Studies (IDS) majors by answering questions about prerequisites, credit requirements, proposal process, sample combinations, and common student experiences. This knowledge is hard to find because official catalogs are long and static, and advising is limited.

## Documents
All PDFs stored in the docs/ folder (Truman Academic Catalog, IDS Major Guidelines, sample 4-year plans, JINS descriptions, etc.). At least 10 documents.

## Chunking Strategy
Chunk size: 500 characters with 100 character overlap.
Reason: IDS documents contain both dense requirement lists and explanatory text. This size keeps specific prerequisites searchable while overlap prevents important rules from being split across chunks.

## Retrieval Approach
Embedding model: all-MiniLM-L6-v2 (via sentence-transformers)
Top-k: 5 chunks per query.
In production I would consider larger models for better accuracy on academic terms, even if slower.

## Evaluation Plan
1. Question: What are the minimum credit requirements for an IDS major at Truman?
   Expected: At least 36 credits, including upper-division requirements.

2. Question: Can I combine Computer Science and Environmental Studies for an IDS major?
   Expected: Yes, possible with proper approval and a clear rationale.

3. Question: What is the process to propose an Interdisciplinary major?
   Expected: Submit a proposal with course list and justification to the IDS committee/advisor.

4. Question: Do JINS seminars count toward IDS credits?
   Expected: Yes, they often count as interdisciplinary credit.

5. Question: What are common challenges with IDS majors at Truman?
   Expected: Approval process, finding advisors, making sure credits count properly.

## Anticipated Challenges
- PDF text extraction issues (headers/footers)
- Requirements spread across multiple documents
- Retrieval missing full context if chunks are poorly split

## AI Tool Plan
- Used AI to generate ingestion and chunking code based on this planning.md
- Used AI to help write grounded generation prompt and Gradio interface
