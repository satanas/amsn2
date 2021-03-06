# -*- coding: utf-8 -*-
#===================================================
# 
# chat_window.py - This file is part of the amsn2 package
#
# Copyright (C) 2008  Wil Alvarez <wil_alejandro@yahoo.com>
#
# This script is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software 
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This script is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License 
# for more details.
#
# You should have received a copy of the GNU General Public License along with 
# this script (see COPYING); if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#===================================================

import gc
import gtk
import cgi
import time
import pango
from htmltextview import *
from amsn2.gui import base
from amsn2.core.views import StringView

class aMSNChatWindow(base.aMSNChatWindow, gtk.Window):
    def __init__(self, amsn_core):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self._amsn_core = amsn_core
        self.child = None
        self.showed = False
        self.set_default_size(550, 450)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("aMSN - Chatwindow")
        
        #leave

    def addChatWidget(self, chat_widget):
        print 'addedChatWidget'
        #if self.child is not None: self.remove(self.child)
        #if self.child is not None: 
        #    self.show_all()
        #    return
        if self.child is None: self.add(chat_widget)
        self.child = chat_widget
        
        self.show_all()
        self.child.entry.grab_focus()


class aMSNChatWidget(base.aMSNChatWidget, gtk.VBox):
    def __init__(self, amsn_conversation, parent):
        gtk.VBox.__init__(self, False, 0)
        
        self._parent = parent
        self._amsn_conversation = amsn_conversation
        self._amsn_core = amsn_conversation._core
        self._theme_manager = self._amsn_core._theme_manager
        self.padding = 4
        self.lastmsg = ''
        self.last_sender = ''
        self.nickstyle = "color:#555555; margin-left:2px"
        self.msgstyle = "margin-left:15px"
        self.infostyle = "margin-left:2px; font-style:italic; color:#6d6d6d"
        
        self.chatheader = aMSNChatHeader()
        
        # Middle
        self.textview = HtmlTextView()
        tscroll = gtk.ScrolledWindow()
        tscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        tscroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        tscroll.add(self.textview)
        
        #self.chat_roster = ChatRoster()
        
        self.middle_box = gtk.HPaned()
        self.middle_box.pack1(tscroll, True, True)
        
        # Bottom
        self.entry = MessageTextView()
        
        escroll = gtk.ScrolledWindow()
        escroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        escroll.set_placement(gtk.CORNER_TOP_LEFT)
        escroll.set_shadow_type(gtk.SHADOW_IN)
        escroll.set_size_request(-1, 40)
        escroll.add(self.entry)
        
        # Register button icons as stock icons
        iconfactory = gtk.IconFactory()
        icons = ['button_smile', 'button_nudge']
        for key in icons:
            type, path = self._theme_manager.get_button(key)
            pixbuf = gtk.gdk.pixbuf_new_from_file(path)
            iconset = gtk.IconSet(pixbuf)
            iconfactory.add(key, iconset)
            iconfactory.add_default()
            del pixbuf
            gc.collect()

        self.button1 = gtk.ToolButton('button_smile')
        self.button2 = gtk.ToolButton('button_nudge')
        self.button3 = gtk.ToggleToolButton(gtk.STOCK_BOLD)
        self.button4 = gtk.ToggleToolButton(gtk.STOCK_ITALIC)
        self.button5 = gtk.ToggleToolButton(gtk.STOCK_UNDERLINE)
        self.button6 = gtk.ToggleToolButton(gtk.STOCK_STRIKETHROUGH)
        self.button7 = gtk.ToolButton(gtk.STOCK_COLOR_PICKER)
        self.button8 = gtk.ToolButton(gtk.STOCK_CLEAR)
        
        bbox = gtk.Toolbar()
        bbox.set_style(gtk.TOOLBAR_ICONS)
        bbox.insert(self.button1, -1)
        bbox.insert(self.button2, -1)
        bbox.insert(gtk.SeparatorToolItem(), -1)
        bbox.insert(self.button3, -1)
        bbox.insert(self.button4, -1)
        bbox.insert(self.button5, -1)
        bbox.insert(self.button6, -1)
        bbox.insert(self.button7, -1)
        bbox.insert(gtk.SeparatorToolItem(), -1)
        bbox.insert(self.button8, -1)
        
        bottom_box = gtk.VBox(False, 0)
        bottom_box.pack_start(bbox, False, False, 0)
        bottom_box.pack_start(escroll, True,True, 0)
        
        self.statusbar = gtk.Statusbar()
        self.statusbar.set_has_resize_grip(False)
        self.statusbar.set_spacing(0)
        
        self.__set_statusbar_text('Welcome to aMSN2')
        
        vpaned = gtk.VPaned()
        vpaned.pack1(self.middle_box, True, True)
        vpaned.pack2(bottom_box, False, True)
        
        self.pack_start(self.chatheader, False, False, self.padding)
        self.pack_start(vpaned, True, True, self.padding)
        self.pack_start(self.statusbar, False, False)
        
        #Connections
        #========
        '''        
        self.entrytextview.connect('focus-in-event', self.chatman.setUrgencyHint, False)
        self.entrytextview.get_buffer().connect("changed",self.__updateTextFormat)
        self.textview.connect("button-press-event", self.__rightClick)
        
        '''
        '''
        self.textview.connect("url-clicked", self.__on_url_clicked)
        
        self.button1.connect("clicked", self.__create_smiles_window)
        self.button3.connect("clicked", 
            self.__on_changed_text_effect, 'bold')
        self.button4.connect("clicked", 
            self.__on_changed_text_effect, 'italic')
        self.button5.connect("clicked", 
            self.__on_changed_text_effect, 'underline')
        self.button6.connect("clicked", 
            self.__on_changed_text_effect, 'strikethrough')
        self.button7.connect("clicked", self.__on_changed_text_color)
        '''
        self.button2.connect("clicked", self.__on_nudge_send)
        self.button8.connect("clicked", self.__on_clear_textview)
        self.entry.connect('mykeypress', self.__on_chat_send)
        self.entry.connect('key-press-event', self.__on_typing_event)
        
    def __clean_string(self, str):
        return cgi.escape(str)
        
    def __on_chat_send(self, entry, event_keyval, event_keymod):
        if (event_keyval == gtk.keysyms.Return):
            buffer = entry.get_buffer()
            start, end = buffer.get_bounds()
            msg = buffer.get_text(start, end)
            entry.clear()
            entry.grab_focus()
            if (msg == ''): return False
        
        strv = StringView()
        strv.appendText(msg)
        self._amsn_conversation.sendMessage(strv)
        
    def __on_clear_textview(self, widget):
        buffer = self.textview.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        buffer.delete(start, end)
        
    def __on_typing_event(self, widget, event):
        self._amsn_conversation.sendTypingNotification()
        
    def __on_nudge_send(self, widget):
        self.__print_info('Nudge sent')
        self._amsn_conversation.sendNudge()
    
    def __print_chat(self, nick, msg, sender):
        html = '<div>'
        if (self.last_sender != sender):
            html += '<span style="%s">%s</span><br/>' % (self.nickstyle, 
                nick)
        html += '<span style="%s">[%s] %s</span></div>' % (self.msgstyle,
            time.strftime('%X'), msg)
        
        self.textview.display_html(html)
        self.textview.scroll_to_bottom()
        
    def __print_info(self, msg):
        html = '<div><span style="%s">%s</span></div>' % (self.infostyle, msg)
        self.textview.display_html(html)
        self.textview.scroll_to_bottom()
        
    def __set_statusbar_text(self, msg):
        context = self.statusbar.get_context_id('msg')
        self.statusbar.pop(context)
        self.statusbar.push(context, msg)
        
    def onMessageReceived(self, messageview):
        text = messageview.toStringView().toHtmlString()
        text = self.__clean_string(text)
        nick, msg = text.split('\n', 1)
        nick = str(nick.replace('\n', '<br/>'))
        msg = str(msg.replace('\n', '<br/>'))
        sender = messageview.sender.toString()
        
        self.__print_chat(nick, msg, sender)
        
        self.last_sender = sender
        
    def onUserJoined(self, contact):
        print "%s joined the conversation" % (contact,)
        self.__print_info("%s joined the conversation" % (contact,))

    def onUserLeft(self, contact):
        print "%s left the conversation" % (contact,)
        self.__print_info("%s left the conversation" % (contact,))

    def onUserTyping(self, contact):
        print "%s is typing" % (contact,)
        #self.__set_statusbar_text("%s is typing" % (contact,))

    def nudge(self):
        self.__print_info('Nudge received')


class aMSNChatHeader(gtk.EventBox):
    def __init__(self, cview=None):
        gtk.EventBox.__init__(self)
        
        self.buddy_icon = gtk.Image()
        self.title = gtk.Label()
        self.dp = gtk.Image()
        self.title_color = gtk.gdk.color_parse('#dadada')
        self.psm_color = '#999999'
        
        self.title.set_use_markup(True)
        self.title.set_justify(gtk.JUSTIFY_LEFT)
        self.title.set_ellipsize(pango.ELLIPSIZE_END)
        self.title.set_alignment(xalign=0, yalign=0.5)
        self.title.set_padding(xpad=2, ypad=2)
        
        self.dp.set_size_request(50,50)
        
        hbox = gtk.HBox(False,0)
        hbox.pack_start(self.buddy_icon, False,False,0)
        hbox.pack_start(self.title, True,True,0)
        hbox.pack_start(self.dp, False,False,0)
        
        self.modify_bg(gtk.STATE_NORMAL, self.title_color)
        self.add(hbox)
        
        self.update(cview)
        
    def update(self, cview):
        if cview is None:
            nickname = 'Me'
            psm = 'Testing aMSN'
        
        title = '<span size="large"><b>%s</b></span>' % (nickname, )
        
        if(psm != ''): 
            title += '\n<span size="small" foreground="%s">%s</span>' % ( 
            self.psm_color, psm)
        
        self.title.set_markup(title)
        