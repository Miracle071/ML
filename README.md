Objective

Develop a new solution capable of extracting product information from Furniture Stores' websites.

Input

You will receive a list of URLs from various furniture stores' websites. While most URLs will contain product information, some may not, and others may be dysfunctional. You can access the list of URLs from the following link: URL list file.

Output

The expected output is a single-page website where the URL can be submitted and a list of product names extracted from the URL displayed. You have the flexibility to present the results creatively, such as identifying the most popular product or aggregating products from the entire site to showcase the strengths of your solution.

Guidelines

A recommended approach for this extraction task involves creating a Named Entity Recognition (NER) model specifically tailored to identify the entity 'PRODUCT':

1. Gather training data by crawling approximately 100 pages from the provided list of URLs and extracting text from them.

2. Tag sample products within these texts.

3. Train a new model using the annotated examples.

4. Utilize the model to extract product names from new, unseen pages.

It is suggested to leverage the Transformer architecture from either the sparknlp library or the transformers library by Hugging Face for this task.

Evaluation Criteria

While there are multiple ways to demonstrate the effectiveness of your solution, the following criteria are essential for a successful project:

Provide a detailed explanation of your thought process, outlining how your solution operates, alternative approaches considered, and the rationale behind your chosen method.

Ensure that your code is well-structured. While this is a Proof of Concept (PoC), strive for clarity, robustness, conciseness, and ease of collaboration.

Clearly present your outputs, including relevant metrics, to showcase the potential real-world applicability of your solution.

Free web hosting can be used to deploy the website.

Note

The provided guidelines are flexible, and you are encouraged to explore any tools or solutions you deem suitable, especially if they enhance the project's quality or novelty.

