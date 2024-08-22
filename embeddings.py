

from transformers import AutoTokenizer, AutoModel
import torch
from datasets import Dataset
import numpy as np

movies = ["SM900 White Wired Gaming Mouse with Honeycomb Shell,12800 DPI,7 Programmable Buttons,Lightweight Gaming Mice Ergonomic Computer Mouse Gaming for Windows/PC/Mac/Laptop Gamer. 【6 Levels Adjustable Dpi】SM900 is a powerful gaming mouse with excellent performance,It supports 6 levels adjustment DPI up to 12800.According user's preference setup different DPI , suitable for games, office and many occasions.", "Hanes Men's T-Shirt, Beefy-T Heavyweight Cotton Crewneck Tee, 1 or 2 Pack, Available in Tall Sizes: HANES QUALITY - Men’s tees are made with a high-density stitch count, double-needle stitching, and shoulder-to-shoulder taping.", "SUREWAY Men's 10 in Pull On Western Square Toe Work Boots for Men Soft Toe,Comfortable Durable Premium Leather,Superior Oil/Slip Resistant,Rubber Sole,Embroidered: 【Digging into every detail of boots & 12 months Manufacture Guarantee】:At SUREWAY,we carefully design every aspect of this square toe boots to provide you with ultimate comfort and durability.Our commitment is to deliver high-quality work boots that exceed customer expectations.We highly value every customer and offer a 12 months warranty to address any concerns or hesitations.Get prepared to be amazed by the exceptional level of quality,craftsmanship,and comfort found in our work boots/shoes."]



device = torch.device("cuda")

model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
model = AutoModel.from_pretrained(model_ckpt)
model.to(device)

def get_embeddings(text):
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    inputs.to(device)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    model_output = model(**inputs)
    embeddings = model_output.last_hidden_state[:, 0]
    return embeddings

movie_embeddings = [get_embeddings(movie) for movie in movies]
np_embeddings = [embedding.cpu().detach().numpy() for embedding in movie_embeddings]
#np_embeddings = Dataset.from_dict({"embeddings": np_embeddings})

#np_embeddings.add_faiss_index(column="embeddings")
#Dataset.add_faiss_index_from_external_arrays(external_arrays=np_embeddings, index_name="embeddings", device=device)

input = "Gift for a friend that likes horseback riding"
input_embedding = get_embeddings(input).cpu().detach().numpy()
for i in range(len(np_embeddings)):
    print("Para el valor", i, movies[i])
    #print(np.dot(input_embedding/(np.linalg.norm(input_embedding)), (np_embeddings[i].T)/(np.linalg.norm(np_embeddings[i]))))
    print(np.linalg.norm(input_embedding-np_embeddings[i]))
""" scores, samples = np_embeddings.get_nearest_examples("embeddings", input_embedding, k=2)
print(movies[samples[0]])
print(scores, samples) """