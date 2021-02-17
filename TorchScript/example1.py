import os
import sys
import timeit

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.jit as jit

from torchvision import models
from torch.utils import mkldnn as mkldnn_utils

class MyModel1(nn.Module):

	def __init__(self):

		super(MyModel1, self).__init__()

		self.l1 = nn.Linear(3, 6)
		self.l2 = nn.Linear(6, 3)

	def forward(self, x, y):

		out = self.l1(x)
		out = F.relu(out)
		out = out + y
		out = self.l2(out)
		out = F.relu(out)

		return out

class MyModel2(nn.Module):

	def __init__(self):

		super(MyModel2, self).__init__()

		self.l1 = nn.Linear(3, 6)
		self.l2_1 = nn.Linear(6, 5)
		self.l2_2 = nn.Linear(6, 4)

	def forward(self, x):

		out = self.l1(x)

		if out.sum() > 0:

			out = self.l2_1(F.relu(out))

		else:

			out = self.l2_2(F.relu(out))

		return out

class MyModel3(nn.Module):

	def __init__(self):

		super(MyModel3, self).__init__()

		self.l1 = nn.Linear(3, 1024)

	def forward(self, x):

		out = F.relu(self.l1(x))

		return out

class MyModel4(nn.Module):

	def __init__(self):

		super(MyModel4, self).__init__()

		self.b1 = jit.script(MyModel3())
		self.l1 = nn.Linear(1024, 1024)
		self.l2 = nn.Linear(1024, 1024)
		self.l3 = nn.Linear(1024, 1024)

	def forward(self, x):

		out = self.b1(x)
		out = F.relu(self.l1(out))
		out = F.relu(self.l2(out))
		out = F.relu(self.l3(out))

		return out

def main_1():

	# good case
	input1 = torch.randn(2, 3)
	input2 = torch.randn(2, 6)
	orig_model = MyModel1()
	output1 = orig_model(input1, input2)
	print(output1)

	traced_model = jit.trace(orig_model, (input1, input2))
	print(type(traced_model))
	print(traced_model)
	output2 = traced_model(input1, input2)
	print(output2)

	# bad case
	# input1 = torch.randn(2, 6)
	# input2 = torch.randn(2, 6)
	# orig_model = MyModel1()
	# output1 = orig_model(input1, input2)
	# print(output1)

	# traced_model = jit.trace(orig_model, (input1, input2))
	# output2 = traced_model(input1, input2)
	# print(output2)

	print('=======')
	print(traced_model.graph)
	print('=======')
	print(traced_model.code)

	print('=======')
	print(dir(traced_model))
	print('=======')
	print(traced_model.l1)
	print(traced_model.l1.weight)

def main_2():

	orig_model = MyModel2()

	# case 1
	input1 = torch.randn(2, 3)
	input1 = input1.pow(2) # always positive
	traced_model1 = jit.trace(orig_model, (input1))

	# case 2
	input2 = torch.randn(2, 3)
	input2 = -input2.pow(2) # always negative
	traced_model2 = jit.trace(orig_model, (input2))

	print(orig_model(input1).size(), orig_model(input2).size())
	print(traced_model1(input1).size(), traced_model1(input2).size())
	print(traced_model2(input1).size(), traced_model2(input2).size())

	print(traced_model1.code)
	print('=======')
	print(traced_model2.code)
	print('=======')

	# scripting
	scripted_model = jit.script(orig_model)

	print(orig_model(input1).size(), orig_model(input2).size())
	print(scripted_model(input1).size(), scripted_model(input2).size())
	print(scripted_model.code)

def main_3():

	orig_model = MyModel4()

	input1 = torch.randn(2, 3)
	hybrid_model = jit.trace(orig_model, (input1))

	print(hybrid_model.code)

	# save and load model
	hybrid_model.save('model.zip')
	loaded_model = torch.jit.load('model.zip')

	with torch.no_grad():

		input2 = torch.randn(100000, 3)
		result = orig_model(input2)
		result = orig_model(input2)
		result = orig_model(input2)
		result = orig_model(input2)
		result = hybrid_model(input2)
		result = hybrid_model(input2)
		result = hybrid_model(input2)
		result = hybrid_model(input2)

		# time measurement
		start_time = timeit.default_timer()
		result = orig_model(input2)
		run_time = timeit.default_timer() - start_time

		print('Python: {}'.format(run_time))

		start_time = timeit.default_timer()
		result = hybrid_model(input2)
		run_time = timeit.default_timer() - start_time
		
		print('TorchScript: {}'.format(run_time))

		# using GPU
		input2 = torch.randn(100000, 3).to('cuda')
		orig_model = orig_model.to('cuda')
		hybrid_model = hybrid_model.to('cuda')
		result = orig_model(input2)
		result = orig_model(input2)
		result = orig_model(input2)
		result = orig_model(input2)
		result = hybrid_model(input2)
		result = hybrid_model(input2)
		result = hybrid_model(input2)
		result = hybrid_model(input2)
		
		start_time = timeit.default_timer()
		result = orig_model(input2)
		run_time = timeit.default_timer() - start_time

		print('Python (GPU): {}'.format(run_time))

		start_time = timeit.default_timer()
		result = hybrid_model(input2)
		run_time = timeit.default_timer() - start_time
		
		print('TorchScript (GPU): {}'.format(run_time))

def main_4():

	# check MKL-DNN
	print(*torch.__config__.show().split('\n'), sep = '\n')
	print('=======')

	orig_model = models.resnet101(False)
	input1 = torch.rand(100, 3, 224, 224)

	result = orig_model(input1)
	result = orig_model(input1)
	result = orig_model(input1)
	result = orig_model(input1)

	start_time = timeit.default_timer()
	result = orig_model(input1)
	run_time = timeit.default_timer() - start_time

	print('Python (CPU): {}'.format(run_time))

	orig_model.eval()
	mkldnn_model = mkldnn_utils.to_mkldnn(orig_model)
	input1 = input1.to_mkldnn()
	answer = torch.zeros(100, 1000).to_mkldnn()

	result = mkldnn_model(input1)
	result = mkldnn_model(input1)
	result = mkldnn_model(input1)
	result = mkldnn_model(input1)

	start_time = timeit.default_timer()
	result = mkldnn_model(input1)
	run_time = timeit.default_timer() - start_time

	print('Python (MKL-DNN): {}'.format(run_time))

	# can compute gradient?
	# loss = F.mse_loss(result, answer)
	# loss = (result - answer).pow(2).mean()
	# loss.backward()

if __name__ == '__main__':

	print(sys.version) # tested on 3.8.5
	print(torch.__version__) # tested on 1.7.1

	main_1()
	main_2()
	main_3()
	main_4()
