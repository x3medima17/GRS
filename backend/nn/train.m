warning('off','all');


data = load('data.txt');

m = size(data,1);
n = size(data,2) -1;

X = data(:,1:n);
y = data(:,n+1);
size(data);

input_layer_size = n;
hidden_layer_size = 40;
num_labels = 10;


Theta1 = rand(hidden_layer_size,input_layer_size+1);
Theta2 = rand(hidden_layer_size,hidden_layer_size+1);
Theta2 = rand(num_labels,hidden_layer_size+1);

hidden_layer_size;
num_labels;
size(Theta1);
size(Theta2);

nn_params = [Theta1(:) ; Theta2(:)];
initial_nn_params = nn_params;
lambda = 0;	


J = nnCostFunction(nn_params, input_layer_size, hidden_layer_size, ...
                   num_labels, X, y, lambda);

options = optimset('MaxIter',1000);
costFunction = @(p) nnCostFunction(p, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, lambda);
[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

N = input_layer_size;
H = hidden_layer_size;
K = num_labels;

Theta1 = reshape(nn_params(1:H*(N+1)),H,N+1);
Theta2 = reshape(nn_params(H*(N+1)+1:end),K,H+1);
% Theta2 = reshape(nn_params(H*(N+1)+1:H*(N+1) + H*(H+1)), H,H+1);

% Theta3 = reshape(nn_params(H*(N+1)+1 + H*(H+1):end),K,H+1);

pred = predict(Theta1,Theta2,X);
fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y)) * 100);

x = [0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0];
pred = predict(Theta1,Theta2,x)
