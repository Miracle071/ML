Objective

Develop a new solution capable of extracting product information from furniture store websites.

Input

You will receive a list of URLs from various furniture store websites. While most URLs will contain product information, some may not, and others may be dysfunctional. You can access the list of URLs via the following link: URL list file.

Output
The expected output is a single-page website where users can submit a URL and view a list of product names extracted from that URL. You have the flexibility to present the results creatively—for example, by identifying the most popular product or aggregating products across the entire site to showcase the strengths of your solution.

Guidelines
A recommended approach for this extraction task involves creating a Named Entity Recognition (NER) model specifically trained to identify the 'PRODUCT' entity:

Gather training data by crawling approximately 100 pages from the provided list of URLs and extracting text from them.

Annotate sample products within these texts.

Train a new model using the labeled examples.

Use the model to extract product names from new, unseen pages.

It is suggested to leverage the Transformer architecture from either the sparknlp library or Hugging Face's transformers library for this task.

Evaluation Criteria
While there are multiple ways to demonstrate the effectiveness of your solution, the following criteria are essential for a successful project:

Provide a detailed explanation of your thought process, outlining how your solution works, alternative approaches considered, and the rationale behind your chosen method.

Ensure your code is well-structured. Even as a Proof of Concept (PoC), prioritize clarity, robustness, conciseness, and ease of collaboration.

Clearly present your outputs, including relevant metrics, to showcase the real-world applicability of your solution.

Free web hosting may be used to deploy the website.

Note
The provided guidelines are flexible, and you are encouraged to explore any tools or solutions you deem suitable—especially if they enhance the project's quality or novelty.

