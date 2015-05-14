warning('off','all');


data = load('dataNN.dat');

m = size(data,1);
n = size(data,2) -1;

X = data(:,1:n);
y = data(:,n+1);
size(data);

input_layer_size = n;
hidden_layer_size = round(n*3/2);
num_labels = max(y);

input_layer_size
hidden_layer_size
num_labels

Theta1 = rand(hidden_layer_size,input_layer_size+1);
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

options = optimset('MaxIter',200);
costFunction = @(p) nnCostFunction(p, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, lambda);
[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

pred = predict(Theta1, Theta2, X);


fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y)) * 100);

save Theta1.dat Theta1
save Theta2.dat Theta2 
