# Document Classification Web API

## Identifying the Problem & Goal

It all started with the realization that document classification, especially with messy and unstructured PDFs, required a powerful solution. Traditional models like Random Forest just couldn't handle the complexity of document layouts. That's why I decided to choose LayoutLM v2, a deep learning model specially designed for document understanding. Its promise of tackling intricate PDF structures made it the obvious choice over simpler models.
## Training: Elevating Accuracy with LayoutLM v2

I spend most of my time preparing dataset & experimenting with different models. I gathered a dataset of 27 diverse PDFs that were shared with me. The decision to go deep with LayoutLM v2 was a good decision. The model achieved an impressive accuracy rate of 96%, proving its ability in handling the nuances of messy PDFs.
## Dockerization & Deployment

The next logical step was to deploy the trained model into a user-friendly API. It encapsulates all the nitty-gritty details, making life easier for developers. 
But why stop there? I decided to take it a step further and deploy the API on AWS EC2 instances. This cloud-based setup not only provided scalability but also ensured a robust and reliable deployment. It was a move that would make the Document Classification API even more accessible and dependable.

## Key Feature

Predictive Accuracy: By leveraging the LayoutLM v2 model, the API ensures high accuracy in predicting document categories.

## Endpoints

1) Health Check
<br>Endpoint: ```/health```
<br>Method: ```GET```
<br>Description: A quick health check endpoint to verify the operational status of the API.
<br> Response Example: ```{"status":"OK"}```
2) Document Classification
<br>Endpoint: ```/upload_pdf```
<br>Method: ```POST```
<br>Description: Accepts PDF files for classification. The API predicts the document category and returns the result.
<br>Request Parameters:
file (multipart file): The input PDF file. 
<br> Response Example: ```{"filename": "document.pdf", "predicted_label": "Financial Report"}```

## Source Code

<br>GitHub: https://github.com/jenapss/pdf_classification
<br>Custom Trained LayoutLMv2 OCR Model:
https://drive.google.com/drive/folders/17oVK2tqNd1byc0kJx4FFw4nxEJnBFal_?usp=share_link

## AWS EC2 container endpoint
[http://16.170.218.27:80/upload_pdf](http://16.170.218.27:80/upload_pdf)
<br>[http://16.170.218.27:80/health](http://16.170.218.27:80/health)

Try this command
```
curl -X POST -F "file=@<path_to_your_pdf_file>" http://16.170.218.27:80/upload_pdf
```
Health check
```
curl -X GET http://16.170.218.27:80/health
```
## Setup Instructions for Local deployment

To deploy this app locally, follow these steps:

1) Download the model file "model.safetensors" (807 MB) from the Google Drive folder. You can download it manually or with CLI command shown below
2) Place the downloaded file into the "OCRmodel" folder of the repository.
```
FILEID="1-5utW7IaP--o-b2Yyrv4TqMfcTOl3tvV"
FILENAME="model.safetensors"
# run below command under OCRmodel dir
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=${FILEID}' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=${FILEID}" -O ${FILENAME} && rm -rf /tmp/cookies.txt
```
3) clone this repo ```git clone https://github.com/jenapss/pdf_classification``` and ```cd``` into cloned repo
4) Build the Docker container.
 <br>  a) ```docker build -t <image_name>:<tag> .```
 <br>  b) ```docker run -p <host-port>:<container-port> <image_name>:<tag>```

## Some Recommendations & Ideas
Some PDFs contain too many pages that are not that much needed to make classification. By some additional preprocessing step, before sending POST requests with PDFs, we could keep only up to 3 pages of PDFs. This way we can increase inference time because it directly affects upload/download time.


