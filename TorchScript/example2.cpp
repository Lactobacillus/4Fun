#include <iostream>
#include <torch/torch.h>
#include <torch/script.h>
#include <chrono>

int main(int argc, const char * argv[]){

	torch::jit::script::Module my_torch_model;
	my_torch_model = torch::jit::load(argv[1]);

	std::vector<torch::jit::IValue> inputs;
	inputs.push_back(torch::rand({100000, 3}));
	torch::Tensor pred = my_torch_model.forward(inputs).toTensor();
	pred = my_torch_model.forward(inputs).toTensor();
	pred = my_torch_model.forward(inputs).toTensor();
	pred = my_torch_model.forward(inputs).toTensor();

	auto start = std::chrono::high_resolution_clock::now();
	pred = my_torch_model.forward(inputs).toTensor();
	auto finish = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> elapsed = finish - start;

	std::cout << "TorchScript (C++): " << elapsed.count() << std::endl;

}