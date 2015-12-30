#!/usr/bin/env python
#
# by Kendall Tristan Weaver <kendalltweaver@gmail.com>
# for Peppermint OS

import os
import pygtk
pygtk.require("2.0")
import gtk

global iconplace
iconplace = str("/usr/share/pixmaps/ice.png")

class IconSel(gtk.FileSelection):

    def file_ok_sel(self, w):
        global iconplace
        iconplace = str(self.filew.get_filename())
        print iconplace
        self.filew.destroy()

    def __init__(self):
        self.filew = gtk.FileSelection("File selection")
        self.filew.ok_button.connect("clicked", self.file_ok_sel)
        self.filew.cancel_button.connect("clicked",
                                         lambda w: self.filew.destroy())

        self.filew.set_filename("/usr/share/pixmaps/ice.png")

        self.filew.show()

class Prism(gtk.Window):

    def destroy(self, widget):
        gtk.main_quit()

    def filesel(self, widget):
        IconSel()

    def menu(self, widget):
        global locmenu
        global menuloc
        locmenu = widget.get_active_text()
        print locmenu
        if str(locmenu) == str("Accessories"):
            menuloc = str("Utility;")
        elif str(locmenu) == str("Games"):
            menuloc = str("Game;")
        elif str(locmenu) == str("Graphics"):
            menuloc = str("Graphics;")
        elif str(locmenu) == str("Internet"):
            menuloc = str("Network;")
        elif str(locmenu) == str("Office"):
            menuloc = str("Office;")
        elif str(locmenu) == str("Other"):
            menuloc = str("")
        elif str(locmenu) == str("Sound & Video"):
            menuloc = str("AudioVideo;")
        elif str(locmenu) == str("System Tools"):
            menuloc = str("System;")
        print menuloc

    def icondl(self, widget):
        global appurl
        appurl = url.get_text()
        url1 = appurl.replace ( 'http://', '' )
        url2 = url1.replace ( '/', ' ' )
        url3 = url2.split()
        url4 = str(url3[0]) + str("/favicon.ico")
        os.system("if [ -f /tmp/favicon.png ]; then rm /tmp/favicon.ico; fi")
        os.system("wget -O /tmp/favicon.png " + str(url4))
        global iconplace
        iconplace = "/tmp/favicon.png"

    def applicate(self, widget):

        #Get the necessary variables
        global appurl
        appurl = url.get_text()
        print appurl
        global appname
        appname = name.get_text()
        print appname
        global dirname
        dirname = appname.lower().replace ( ' ', '.' )
        print dirname
        global desktop
        desktop = dirname.replace( '.', '-' )
        print desktop
        print iconplace

        if str(iconplace) == str("/tmp/favicon.png"):
            icondest = str("/usr/lib/peppermint/prism/" + str(dirname) + "@prism.app/icons/default/webapp.png")
        else:
            icondest = str(iconplace)

        #Make the directory
        if not os.path.exists('$HOME/.local/share/ice/'):
            os.system("mkdir -p $HOME/.local/share/ice/")

        #Create the .desktop file
        os.system("touch $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"[Desktop Entry]\" > $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"Version=1.0\" >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"Name=" + str(appname) + "\" >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \'Exec=chromium-browser --app=\"" + str(appurl) + "\"\' >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"Terminal=false\" >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"X-MultipleArgs=false\" >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"Type=Application\" >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"Icon=$HOME/.local/share/ice/" + str(desktop) + ".png\" >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"Categories=GTK;" + str(menuloc) + "\" >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"MimeType=text/html;text/xml;application/xhtml_xml;\" >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"StartupWMClass=Chromium\" >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")
        os.system("echo \"StartupNotify=true\" >> $HOME/.local/share/applications/" + str(desktop) + ".desktop")

        #Copy the icon
        os.system("cp --force " + str(iconplace) + " $HOME/.local/share/ice/" + str(desktop) + ".png")

        #Close the window after creating files
        gtk.main_quit()

    def __init__(self):
        super(Prism, self).__init__()

        #Default window parameters
        self.set_size_request(400, 300)
        self.set_title("Ice")
        self.connect("destroy", self.destroy)
        self.set_position(gtk.WIN_POS_CENTER)

        #URL and Name boxes and functions
        global url
        url = gtk.Entry()
        url.set_text("Enter Complete URL Here")
        global appurl
        appurl = url.get_text()
        global name
        name = gtk.Entry()
        name.set_text("Enter Name Here")
        global appname
        appname = name.get_text()

        #Apply and Close buttons and functions
        apply1 = gtk.Button(stock=gtk.STOCK_APPLY)
        apply1.connect("clicked", self.applicate)
        close1 = gtk.Button(stock=gtk.STOCK_CANCEL)
        close1.connect("clicked", self.destroy)

        #ComboBox for selecting menu location
        where = gtk.combo_box_new_text()
        where.connect("changed", self.menu)
        where.append_text("Accessories")
        where.append_text("Games")
        where.append_text("Graphics")
        where.append_text("Internet")
        where.append_text("Office")
        where.append_text("Other")
        where.append_text("Sound & Video")
        where.append_text("System Tools")
        where.set_active(3)

        label3 = gtk.Label("Where in the menu?")

        #Icon selection button and function
        iconlab = gtk.Label("Select an icon for your app:")
        iconsel = gtk.Button("Select Icon")
        iconsel.connect("clicked", self.filesel)
        webconlab = gtk.Label("Or try to use the site icon:")
        webconsel = gtk.Button("Download Icon")
        webconsel.connect("clicked", self.icondl)

        #The rest of the window layout
        label1 = gtk.Label(' Welcome to Ice, a framework for creating\n    simple to use launchers for webapps.')
        label2 = gtk.Label("")

        applyclose = gtk.HBox()
        applyclose.pack_start(apply1)
        applyclose.pack_start(close1)

        hbox4 = gtk.HBox()
        hbox4.pack_start(label3)
        hbox4.pack_start(where)

        hbox2 = gtk.HBox()
        hbox2.pack_start(label2)
        hbox2.pack_start(applyclose)

        hbox1 = gtk.HBox(5, 0)
        hbox1.pack_start(iconlab)
        hbox1.pack_start(iconsel)

        hbox3 = gtk.HBox(5, 0)
        hbox3.pack_start(webconlab)
        hbox3.pack_start(webconsel)

        vbox1 = gtk.VBox(0, 10)
        vbox1.pack_start(label1)
        vbox1.pack_start(url)
        vbox1.pack_start(name)
        vbox1.pack_start(hbox4)
        vbox1.pack_start(hbox1)
        vbox1.pack_start(hbox3)
        vbox1.pack_start(hbox2)

        hbox = gtk.HBox(10, 10)
        hbox.pack_start(vbox1, False, False, 10)

        #Add the widgets and show the window
        self.add(hbox)
        self.show_all()

if __name__ == "__main__":
    Prism()
    gtk.main()
