import torch

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10

# Create random Tensors to hold inputs and outputs
x = torch.randn(N, D_in)
y = torch.randn(N, D_out)

# Use the nn package to define our model as a sequence of layers. nn.Sequential
# is a Module which contains other Modules, and applies them in sequence to
# produce its output. Each Linear Module computes output from input using a
# linear function, and holds internal Tensors for its weight and bias.
model = torch.nn.Sequential(
    torch.nn.Linear(D_in, H),
    torch.nn.ReLU(),
    torch.nn.Linear(H, D_out),
)

# The nn package also contains definitions of popular loss functions; in this
# case we will use Mean Squared Error (MSE) as our loss function.
loss_fn = torch.nn.MSELoss(reduction='sum')


# without optim

# learning_rate = 1e-4
# for t in range(500):
#     # Forward pass: compute predicted y by passing x to the model. Module objects
#     # override the __call__ operator so you can call them like functions. When
#     # doing so you pass a Tensor of input data to the Module and it produces
#     # a Tensor of output data.
#     y_pred = model(x)
    
#     # Compute and print loss. We pass Tensors containing the predicted and true
#     # values of y, and the loss function returns a Tensor containing the
#     # loss.
#     loss = loss_fn(y_pred, y)
#     if t % 100 == 99:
#         print(t, loss.item())
        
#     # Zero the gradients before running the backward pass.
#     model.zero_grad()
    
#     '''
#     In PyTorch, we need to set the gradients to zero before starting to do backpropragation
#     because PyTorch accumulates the gradients on subsequent backward passes.
#     This is convenient while training RNNs.
#     So, the default action is to accumulate (i.e. sum) the gradients on every loss.backward() call.
#     Because of this, when you start your training loop,
#     ideally you should zero out the gradients so that you do the parameter update correctly.
#     Else the gradient would point in some other direction
#     than the intended direction towards the minimum (or maximum, in case of maximization objectives).
#     '''
    
#     # Backward pass: compute gradient of the loss with respect to all the learnable
#     # parameters of the model. Internally, the parameters of each Module are stored
#     # in Tensors with requires_grad=True, so this call will compute gradients for
#     # all learnable parameters in the model.
#     loss.backward()
    
#     # Update the weights using gradient descent. Each parameter is a Tensor, so
#     # we can access its gradients like we did before.
#     with torch.no_grad():
#         # temporarily sets all require_grad to False
#         '''
#         To prevent tracking history (and using memory),
#         you can also wrap the code block in with torch.no_grad()
#         This can be particularly helpful when evaluating a model
#         because the model may have trainable parameters with requires_grad=True,
#         but for which we don’t need the gradients.
#         '''
#         for param in model.parameters():
#             param -= learning_rate * param.grad


# with optim

optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
for t in range(500):
    # Forward pass: compute predicted y by passing x to the model.
    y_pred = model(x)
    
    # Compute and print loss.
    loss = loss_fn(y_pred, y)
    if t % 100 == 99:
        print(t, loss.item())
    
    # Before the backward pass, use the optimizer object to zero all of the
    # gradients for the variables it will update (which are the learnable
    # weights of the model). This is because by default, gradients are
    # accumulated in buffers( i.e, not overwritten) whenever .backward()
    # is called. Checkout docs of torch.autograd.backward for more details.
    optimizer.zero_grad()
    
    # Backward pass: compute gradient of the loss with respect to model
    # parameters
    loss.backward()
    
    # Calling the step function on an Optimizer makes an update to its
    # parameters
    optimizer.step()
    
    
    # where is the gradients calculated at loss.backward() stored?
    # how can optimizer.step() access them?