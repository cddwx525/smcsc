#!/usr/bin/env python
# coding=utf-8

from wx.lib.pubsub import pub
import wx

from serial import Serial
import serial.tools.list_ports

from smcsc_thread import smcsc_thread
from smcsc_frame import smcsc_frame


class smcsc_app(wx.App):
    def OnInit(self):
        # Serial create.
        self.ser = Serial()
        self.thread = smcsc_thread(self.ser)


        # Main frame.
        m_com_choices = []
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) > 0:
            for port in port_list:
                m_com_choices.append(port[0])
        else:
            m_com_choices = []

        frame_title = u"Step motor control system client"

        self.frame = smcsc_frame(self.ser, frame_title, m_com_choices)
        self.frame.Show()

        # Create a pubsub receiver
        pub.subscribe(self.frame.on_recieve_area_update, 'update')

        #print 'Have shown.'
        return True

    def OnExit(self):
        self.thread.stop()
        print "[smcsc_app\t] serial_thread exit."
