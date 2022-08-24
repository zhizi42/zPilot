# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class frame_main
###########################################################################

class frame_main ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"zPilot alpha", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer1.SetMinSize( wx.Size( 500,220 ) )

		bSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.text_state = wx.StaticText( self, wx.ID_ANY, u"未连接游戏", wx.Point( -1,-1 ), wx.Size( 500,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
		self.text_state.Wrap( -1 )

		bSizer1.Add( self.text_state, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.button_doc = wx.Button( self, wx.ID_ANY, u"使用说明", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_doc, 0, wx.ALL, 5 )


		bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_flight_plan = wx.Button( self, wx.ID_ANY, u"飞行计划", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_flight_plan, 0, wx.ALL, 5 )


		bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_connect = wx.Button( self, wx.ID_ANY, u"连接", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_connect, 0, wx.ALL, 5 )


		bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_atc = wx.Button( self, wx.ID_ANY, u"ATC", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_atc.Enable( False )

		bSizer2.Add( self.button_atc, 0, wx.ALL, 5 )


		bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_settings = wx.Button( self, wx.ID_ANY, u"设置", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.button_settings, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.button_doc.Bind( wx.EVT_BUTTON, self.show_doc )
		self.button_flight_plan.Bind( wx.EVT_BUTTON, self.show_flight_plan )
		self.button_connect.Bind( wx.EVT_BUTTON, self.start_connect )
		self.button_atc.Bind( wx.EVT_BUTTON, self.show_atc )
		self.button_settings.Bind( wx.EVT_BUTTON, self.show_settings )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def show_doc( self, event ):
		event.Skip()

	def show_flight_plan( self, event ):
		event.Skip()

	def start_connect( self, event ):
		event.Skip()

	def show_atc( self, event ):
		event.Skip()

	def show_settings( self, event ):
		event.Skip()


###########################################################################
## Class frame_flight_plan
###########################################################################

class frame_flight_plan ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		bSizer10.SetMinSize( wx.Size( 500,200 ) )
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"起飞机场：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer11.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.text_ctrl_dep_airport = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.text_ctrl_dep_airport, 0, wx.ALL, 5 )


		bSizer11.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"降落机场：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer11.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.text_ctrl_arr_airport = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.text_ctrl_arr_airport, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer11, 0, wx.EXPAND, 5 )

		bSizer111 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"机型：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )

		bSizer111.Add( self.m_staticText61, 0, wx.ALL, 5 )

		self.text_ctrl_model = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.text_ctrl_model, 0, wx.ALL, 5 )


		bSizer111.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText71 = wx.StaticText( self, wx.ID_ANY, u"巡航高度：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )

		bSizer111.Add( self.m_staticText71, 0, wx.ALL, 5 )

		self.text_ctrl_alt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.text_ctrl_alt, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer111, 0, wx.EXPAND, 5 )

		bSizer1111 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText611 = wx.StaticText( self, wx.ID_ANY, u"起飞时间：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText611.Wrap( -1 )

		bSizer1111.Add( self.m_staticText611, 0, wx.ALL, 5 )

		self.text_ctrl_dep_time = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1111.Add( self.text_ctrl_dep_time, 0, wx.ALL, 5 )


		bSizer1111.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText711 = wx.StaticText( self, wx.ID_ANY, u"降落时间：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText711.Wrap( -1 )

		bSizer1111.Add( self.m_staticText711, 0, wx.ALL, 5 )

		self.text_ctrl_arr_time = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1111.Add( self.text_ctrl_arr_time, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer1111, 0, wx.EXPAND, 5 )

		bSizer11111 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText7111 = wx.StaticText( self, wx.ID_ANY, u"燃料续航时间：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7111.Wrap( -1 )

		bSizer11111.Add( self.m_staticText7111, 0, wx.ALL, 5 )

		self.text_ctrl_fuel_time = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11111.Add( self.text_ctrl_fuel_time, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer11111, 0, wx.EXPAND, 5 )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer21.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_upload_plan = wx.Button( self, wx.ID_ANY, u"上传飞行计划", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.button_upload_plan, 0, wx.ALL, 5 )


		bSizer21.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_plan_help = wx.Button( self, wx.ID_ANY, u"帮助", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.button_plan_help, 0, wx.ALL, 5 )


		bSizer21.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer10.Add( bSizer21, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer10 )
		self.Layout()
		bSizer10.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.text_ctrl_dep_airport.Bind( wx.EVT_TEXT, self.dep_airport_change )
		self.text_ctrl_arr_airport.Bind( wx.EVT_TEXT, self.arr_airport_change )
		self.text_ctrl_model.Bind( wx.EVT_TEXT, self.model_change )
		self.text_ctrl_alt.Bind( wx.EVT_TEXT, self.alt_change )
		self.text_ctrl_dep_time.Bind( wx.EVT_TEXT, self.dep_time_change )
		self.text_ctrl_arr_time.Bind( wx.EVT_TEXT, self.arr_time_change )
		self.text_ctrl_fuel_time.Bind( wx.EVT_TEXT, self.fuel_time_change )
		self.button_upload_plan.Bind( wx.EVT_BUTTON, self.upload_plan )
		self.button_plan_help.Bind( wx.EVT_BUTTON, self.show_plan_help )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def dep_airport_change( self, event ):
		event.Skip()

	def arr_airport_change( self, event ):
		event.Skip()

	def model_change( self, event ):
		event.Skip()

	def alt_change( self, event ):
		event.Skip()

	def dep_time_change( self, event ):
		event.Skip()

	def arr_time_change( self, event ):
		event.Skip()

	def fuel_time_change( self, event ):
		event.Skip()

	def upload_plan( self, event ):
		event.Skip()

	def show_plan_help( self, event ):
		event.Skip()


###########################################################################
## Class frame_settings
###########################################################################

class frame_settings ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		bSizer3.SetMinSize( wx.Size( 500,300 ) )
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"安装X-Plane插件：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer9.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.dir_picker_game = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer9.Add( self.dir_picker_game, 0, wx.ALL, 5 )

		self.button_install_plugin = wx.Button( self, wx.ID_ANY, u"安装", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.button_install_plugin, 0, wx.ALL, 5 )


		bSizer3.Add( bSizer9, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"服务器名称：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer10.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.text_ctrl_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.text_ctrl_name, 0, wx.ALL, 5 )


		bSizer3.Add( bSizer10, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"服务器地址：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer5.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.text_ctrl_addr = wx.TextCtrl( self, wx.ID_ANY, u"zhizi42.f3322.net", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		bSizer5.Add( self.text_ctrl_addr, 0, wx.ALL, 5 )


		bSizer3.Add( bSizer5, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"呼号：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer6.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.text_ctrl_callsign = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.text_ctrl_callsign, 0, wx.ALL, 5 )


		bSizer3.Add( bSizer6, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.check_box_send_server = wx.CheckBox( self, wx.ID_ANY, u"向服务器发送数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check_box_send_server.SetValue(True)
		bSizer3.Add( self.check_box_send_server, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.check_box_send_game = wx.CheckBox( self, wx.ID_ANY, u"向游戏发送数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check_box_send_game.SetValue(True)
		bSizer3.Add( self.check_box_send_game, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.button_save = wx.Button( self, wx.ID_ANY, u"保存设置", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.button_save, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.button_give = wx.Button( self, wx.ID_ANY, u"捐赠", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.button_give, 0, wx.ALL, 5 )


		bSizer7.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_about = wx.Button( self, wx.ID_ANY, u"关于", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.button_about, 0, wx.ALL, 5 )


		bSizer7.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.button_join = wx.Button( self, wx.ID_ANY, u"加入Q群", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.button_join, 0, wx.ALL, 5 )


		bSizer3.Add( bSizer7, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer3 )
		self.Layout()
		bSizer3.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_close )
		self.button_install_plugin.Bind( wx.EVT_BUTTON, self.install_plugin )
		self.button_save.Bind( wx.EVT_BUTTON, self.save_settings )
		self.button_give.Bind( wx.EVT_BUTTON, self.show_give )
		self.button_about.Bind( wx.EVT_BUTTON, self.show_about )
		self.button_join.Bind( wx.EVT_BUTTON, self.join_group )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def on_close( self, event ):
		event.Skip()

	def install_plugin( self, event ):
		event.Skip()

	def save_settings( self, event ):
		event.Skip()

	def show_give( self, event ):
		event.Skip()

	def show_about( self, event ):
		event.Skip()

	def join_group( self, event ):
		event.Skip()


###########################################################################
## Class frame_give
###########################################################################

class frame_give ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"捐赠", pos = wx.DefaultPosition, size = wx.Size( 720,530 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.bitmap_give = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.bitmap_give, 0, wx.ALL, 5 )


		self.SetSizer( bSizer8 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


