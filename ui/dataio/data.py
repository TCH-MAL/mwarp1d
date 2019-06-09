
import os
import numpy as np
from scipy.io import savemat


class _MWarp1DData(object):
	
	mode                 = None             #manual or landmark
	
	fname0               = None             #input data file name
	fname1               = None             #output data file name
	ydata_template       = None             #template continuum
	ydata_sources        = None             #source continua
	ydata_sources_warped = None             #warper sources

	def __init__(self):
		pass
	
	
	def __repr__(self):
		s   = '%s (%s)\n' %(self.__class__.__name__, self.mode)
		s  += '   ----- FILES -----\n'
		s  += '   fname0   = %s\n'  %self.fname0
		s  += '   fname1   = %s\n'  %self.fname1
		s  += '   ----- DATA -----\n'
		s  += '   num nodes   = %d\n'  %self.nnodes
		s  += '   num sources = %d\n'  %self.nsources
		return s
	
	@property
	def nnodes(self):
		n = 0 if (self.ydata_template is None) else self.ydata_template.size
		return n

	@property
	def nsources(self):
		n = 0 if (self.ydata_sources is None) else self.ydata_sources.shape[0]
		return n

	
	def _init_other_attributes(self):
		pass
	
	def _parse_input_file(self, s):
		y                         = np.loadtxt(s, delimiter=',')
		self.ydata_template       = y[0]
		self.ydata_sources        = y[1:]
		self.ydata_sources_warped = y[1:].copy()
		self._init_other_attributes()
		
	
	def get_dictionary(self):
		d                         = {}
		d['mode']                 = self.mode
		d['filename0']            = self.fname0
		d['filename1']            = self.fname1
		d['ydata_template']       = self.ydata_template
		d['ydata_sources']        = self.ydata_sources
		d['ydata_sources_warped'] = self.ydata_sources_warped
		return d

	
	
	def save(self):
		np.savez_compressed( self.filenameNPZ, self.get_dictionary() )

	
	def save(self):
		np.savez_compressed( self.fname1, **self.get_dictionary() )

	def set_input_filename(self, s, read=True):
		self.fname0      = s
		if read:
			self._parse_input_file(s)
		
		if self.fname1 is None:
			dir1         = os.path.dirname(s)
			fname1       = 'mwarp1d_results.npz'
			self.fname1  = os.path.join(dir1, fname1)
		

	def set_output_filename(self, s):
		self.fname1      = s
	
	def set_sources(self, y, init_warped=False):
		self.ydata_sources = y
		if init_warped:
			self.set_sources_warped( y.copy() )
	
	def set_sources_warped(self, y):
		self.ydata_sources_warped = y
		
	def set_template(self, y):
		self.ydata_template = y
	
	def write_mat(self, fname):
		savemat(fname, self.get_dictionary())
		
	def write_sources_warped_csv(self, fname):
		np.savetxt(fname, self.ydata_sources_warped, delimiter=',')



class DataLandmarks(_MWarp1DData):
	
	mode                 = 'landmarks'
	landmarks_template   = None
	landmarks_sources    = None
	landmark_labels      = None
	
	def _init_other_attributes(self):
		pass

	def get_dictionary(self):
		d     = super().get_dictionary()
		d['landmarks_template']  = self.landmarks_template
		d['landmarks_sources']   = self.landmarks_sources
		d['landmark_labels']     = self.landmark_labels
		return d
	
	def set_landmark_labels(self, x):
		self.landmark_labels    = x
	def set_template_landmarks(self, x):
		self.landmarks_template = x
	def set_source_landmarks(self, x):
		self.landmarks_sources  = x
	
	
	def write_landmarks_csv(self, fname):
		labels = self.landmark_labels
		lm0    = np.asarray(self.landmarks_template, dtype=str)
		lm1    = np.asarray(self.landmarks_sources, dtype=str)
		# write:
		header = ','.join(labels)
		blanks = ','.join( ['-']*len(labels) )
		with open(fname, 'w') as fid:
			fid.write( header + '\n' )
			fid.write( ','.join(lm0) + '\n' )
			fid.write( blanks + '\n' )
			for a in lm1:
				fid.write( ','.join(a) + '\n' )
	


class DataManual(_MWarp1DData):

	mode                 = 'manual'
	# displacement_fields  = None       #final warp fields

	# def _init_other_attributes(self):
	# 	J,Q              = self.ydata_sources.shape
	# 	self.displacement_fields = np.zeros((J,Q))

	# def get_dictionary(self):
	# 	d     = super().get_dictionary()
	# 	d['displacement_fields']  = self.displacement_fields
	# 	return d

