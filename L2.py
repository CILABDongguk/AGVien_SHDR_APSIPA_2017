import caffe
import numpy as np

class L2Loss(caffe.Layer):

	def setup(self, bottom, top):
		if len(bottom) != 2:
			raise Exception("Need two inputs to compute distance.")

	def reshape(self, bottom, top):
		if bottom[0].count != bottom[1].count:
			raise Exception("Inputs muse have the same dimension.")
		self.diff = np.zeros_like(bottom[0].data, dtype = np.float32)
		top[0].reshape(1)

	def forward(self, bottom, top):
		self.diff[...] = bottom[0].data - bottom[1].data
		top[0].data[...] = np.sum(self.diff ** 2) / bottom[0].num / 2.

	def backward(self, top, propagate_down, bottom):
		for i in range(2):
			if not propagate_down[i]:
				continue
			if i == 0:
				sign = 1
			else:
				sign = -1
			
			bottom[i].diff[...] = sign * (self.diff) / bottom[i].num


