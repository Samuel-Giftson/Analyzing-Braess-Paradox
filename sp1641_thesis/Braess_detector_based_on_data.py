import torch
import torch.nn.functional as F
import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.model_selection import train_test_split
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv, global_add_pool


#CUSTOM CLASSES IMPORTS
from store_data_for_machine_learning_model import GetDataForGNN

number_of_nodes = 10
my_store_data_for_machine_learning_model_object = GetDataForGNN()
X, y = my_store_data_for_machine_learning_model_object.get_data(number_of_nodes)

# Assuming X is a list of flattened adjacency matrices (1D arrays) and y is the corresponding labels
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert the list of csr_matrices to dense numpy arrays and then to PyTorch tensors
X_train = torch.tensor([matrix.toarray() for matrix in X_train], dtype=torch.float32)
X_test = torch.tensor([matrix.toarray() for matrix in X_test], dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

# Define a simple Graph Neural Network (GNN) model
class GNN(torch.nn.Module):
    def __init__(self):
        super(GNN, self).__init__()
        self.conv1 = GCNConv(10, 64)  # Adjust input size to match the number of nodes (assuming 10 nodes)
        self.conv2 = GCNConv(64, 32)
        self.fc = torch.nn.Linear(32, 1)

    def forward(self, x, edge_index, batch):
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = global_add_pool(x, batch)
        x = self.fc(x)
        return torch.sigmoid(x)

# Instantiate the GNN model
model = GNN()

# Define a simple graph structure (you need to adapt this to your specific use case)
# Replace this with the actual structure of your graphs
# The assumption here is that your graphs have 10 nodes
edge_index = torch.tensor([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                           [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]], dtype=torch.long)
data = Data(x=X_train, edge_index=edge_index, y=y_train)

# Set up the training loop
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

def train():
    model.train()
    optimizer.zero_grad()
    out = model(data.x, data.edge_index, None)
    loss = F.binary_cross_entropy(out, data.y.view(-1, 1))
    loss.backward()
    optimizer.step()
    return loss.item()

# Training loop
for epoch in range(100):
    loss = train()
    print(f'Epoch {epoch + 1}, Loss: {loss:.4f}')

# Evaluation
model.eval()
with torch.no_grad():
    pred = model(X_test, edge_index, None)
    pred_labels = (pred > 0.5).float()

accuracy = accuracy_score(y_test, pred_labels.numpy())
roc_auc = roc_auc_score(y_test, pred.numpy())

print(f"Accuracy: {accuracy}")
print(f"ROC AUC: {roc_auc}")
print("\nClassification Report:")
print(classification_report(y_test, pred_labels.numpy()))
