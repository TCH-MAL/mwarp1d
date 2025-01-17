#!/usr/bin/env python

import sys,os
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from dataio import DataLandmark,DataManual
from panel_main import MainPanel
from panel_landmarks import LandmarksPanel
from panel_manual import ManualPanel
from widgets import MenuBar


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, argv):
		super().__init__()
		fnameUI  = os.path.join( os.path.dirname(__file__), 'main.ui' )
		uic.loadUi(fnameUI, self)
		self.dir0            = None
		
		# self.centralWidget = QtWidgets.QWidget(self)
		# self.setCentralWidget(self.centralWidget)
		
		
		
		
		self.label0.setVisible(False)
		self.label1.setVisible(False)
		self.label2.setVisible(False)
		
		self.panel_main      = MainPanel(self)
		self.panel_landmarks = LandmarksPanel(self)
		self.panel_manual    = ManualPanel(self)
		self.setMenuBar( MenuBar(self) )
		# self.panel_main      = MainPanel(self)
		# self.panel_landmarks = LandmarksPanel(self)
		# self.panel_manual    = ManualPanel(self)
		# self.setMenuBar( MenuBar(self) )
		self._set_panel(0)
		
		self.hlayout0.addWidget( self.panel_main )
		self.hlayout1.addWidget( self.panel_landmarks )
		self.hlayout2.addWidget( self.panel_manual )
		
		self.hlayout0.layout()
		
		
		# self.setFixedSize(1300, 850)
		# self.setFixedSize(1300, 400)
		
		self._parse_commandline_inputs(argv)
		
		
		self.panel_landmarks.template_locked.connect( self.on_template_locked )
		self.panel_manual.curve_selected.connect( self.on_manual_curve_selected )
		self.panel_manual.warp_applied.connect( self.on_warp_applied )
		self.panel_manual.warp_cancelled.connect( self.on_warp_cancelled )
		self.panel_manual.warp_initiated.connect( self.on_warp_initiated )
		
		
		
		
		

	
	def _parse_commandline_inputs(self, argv):
		argv     = argv[1:]
		narg     = len(argv)
		mode     = None
		
		if narg==0:
			pass
			
		elif narg==1:
			self.panel_main.on_drop( [argv[0]] )
		
		elif narg==2:
			fnameCSV      = argv[0]
			mode          = argv[1]
			fnameNPZ      = os.path.join( os.path.dirname(fnameCSV), 'mwarp1d.npz' )
			self.panel_main.on_drop( [fnameCSV]  )
		
		elif narg==3:
			fnameCSV      = argv[0]
			mode          = argv[1]
			fnameNPZ      = argv[2]
			self.panel_main.on_drop( [fnameCSV]  )
			self.panel_main.set_fname_results( fnameNPZ )
			
		
		
		if mode is not None:
			if mode == 'landmark':
				self.panel_main.on_button_landmarks()
				# data = DataLandmark()
				# self.panel_landmarks.set_data(data)
				# self._set_panel(1)
			elif mode == 'manual':
				self.panel_main.on_button_manual()
			# 	data = DataManual()
			# 	self.panel_manual.set_data(data)
			# 	self._set_panel(2)
			# data.set_input_filename( fnameCSV )
			# data.set_output_filename( fnameNPZ )
			# data.save()


		

	def _set_panel(self, ind):
		self.stackedWidget.setCurrentIndex(ind)
		if ind==0:
			self.menuBar().set_main_panel_menu()
		elif ind==1:
			self.menuBar().set_landmarks_panel_menu()
		elif ind==2:
			self.menuBar().set_manual_panel_menu()
		

	def go_back_to_main_panel(self):
		self._set_panel(0)

	
	
	def get_results_filename(self, fname0, fname1=None):
		if fname1 is None:
			dir0   = os.path.dirname(fname0)
			fname1 = os.path.join(dir0, 'mwarp1d.npz')
		return fname1
		
	
	def on_template_locked(self, locked):
		self.menuBar().update_template_locked(locked)
	
	def on_manual_curve_selected(self, ind):
		self.menuBar().update_manual_curve_selected(ind)
	
	def on_warp_applied(self):
		self.menuBar().update_warp_applied()
	def on_warp_cancelled(self):
		self.menuBar().update_warp_cancelled()
	def on_warp_initiated(self):
		self.menuBar().update_warp_initiated()
	
	
	
	def set_default_directory(self, dir0=None):
		self.dir0  = dir0
	
	def start_landmark_mode(self, template, sources, fname0, fname1=None):
		fname1 = self.get_results_filename(fname0, fname1)
		data   = DataLandmark()
		data.set_input_filename( fname0, read=False )
		data.set_output_filename( fname1 )
		data.set_template(template)
		data.set_sources(sources, init_warped=True)
		data.save()
		self.panel_landmarks.set_data(data)
		self._set_panel(1)
		



	def start_manual_mode(self, template, sources, fname0, fname1=None):
		fname1 = self.get_results_filename(fname0, fname1)
		data   = DataManual()
		data.set_input_filename( fname0, read=False )
		data.set_output_filename( fname1 )
		data.set_template(template)
		data.set_sources(sources, init_warped=True)
		data.save()
		self.panel_manual.set_data(data)
		self._set_panel(2)
		
		
	def start_npz(self, data):
		if data.mode == 'landmark':
			self.panel_landmarks.set_data(data, prewarped=True)
			self._set_panel(1)
		else:
			self.panel_manual.set_data(data, prewarped=True)
			self._set_panel(2)
		
		

class MainApplication(QtWidgets.QApplication):
	def __init__(self, *args):
		self.setApplicationName("Appname")
		super().__init__(*args)
		# style = QtWidgets.QStyleFactory.create('Fusion')
		# self.setStyle(style)



if __name__ == '__main__':
	app    = MainApplication(sys.argv)
	app.setApplicationName("mwarp1d")
	window = MainWindow( sys.argv )
	window.move(0, 0)
	window.show()
	sys.exit(app.exec_())
	
	
	
	
